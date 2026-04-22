document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    const yearSelect = document.getElementById('yearSelect');
    const stateSelect = document.getElementById('stateSelect');
    const crimeTypeSelect = document.getElementById('crimeTypeSelect');
    let indiaGeoJson = null;
    let map = null;
    let geoLayer = null;
    let perCapita = false;

    // Initialize Map - Political Style (Light)
    map = L.map('map', { zoomControl: false }).setView([23.5937, 78.9629], 5);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CartoDB'
    }).addTo(map);
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');
    const body = document.body;

    function updateThemeUI(isLight) {
        if (isLight) {
            body.classList.add('light-mode');
            body.classList.remove('dark-mode');
            themeIcon.innerText = '☀️';
            themeText.innerText = 'Light';
        } else {
            body.classList.add('dark-mode');
            body.classList.remove('light-mode');
            themeIcon.innerText = '🌙';
            themeText.innerText = 'Dark';
        }
        // Force charts to re-render with new theme colors if needed
        if (yearSelect.value) loadDashboard(yearSelect.value);
    }

    const savedTheme = localStorage.getItem('theme') || 'dark';
    updateThemeUI(savedTheme === 'light');

    themeToggle.addEventListener('click', () => {
        const isLight = body.classList.contains('light-mode');
        const newTheme = isLight ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
        updateThemeUI(newTheme === 'light');
    });

    // Filter Listeners
    if (crimeTypeSelect) { // Added check for crimeTypeSelect
        crimeTypeSelect.addEventListener('change', () => {
            loadDashboard(yearSelect.value);
            if (stateSelect.value) loadStateAnalysis(stateSelect.value, yearSelect.value);
        });
    }

    yearSelect.addEventListener('change', () => {
        loadDashboard(yearSelect.value);
        if (stateSelect.value) loadStateAnalysis(stateSelect.value, yearSelect.value);
    });

    stateSelect.addEventListener('change', () => { // Added stateSelect change listener
        if (stateSelect.value) loadStateAnalysis(stateSelect.value, yearSelect.value);
    });

    // Metric Toggle Listeners
    document.querySelectorAll('input[name="metricType"]').forEach(input => {
        input.addEventListener('change', (e) => {
            perCapita = e.target.id === 'metricPerCapita';
            loadDashboard(yearSelect.value);
            if (stateSelect.value) loadStateAnalysis(stateSelect.value, yearSelect.value);
        });
    });

    async function loadDashboard(year) {
        try {
            const crimeType = crimeTypeSelect.value;
            const res = await fetch(`/api/stats?year=${year}&per_capita=${perCapita}&crime_type=${crimeType}`);
            const data = await res.json();

            // Populate State Select if empty
            if (stateSelect.options.length <= 1) {
                const states = Object.keys(data.charts.top_states).sort();
                // Get all states from geojson later or just top states for now
                // Better: get all from the risks mapping
                Object.keys(data.state_risks).sort().forEach(state => {
                    const opt = document.createElement('option');
                    opt.value = state;
                    opt.innerText = state;
                    stateSelect.appendChild(opt);
                });
            }

            // Update KPI Insights Banner only
            document.getElementById('insightText').innerText = data.insights;

            // Render Policy Recommendations
            const recommendationContainer = document.getElementById('policyRecommendations');
            recommendationContainer.innerHTML = '';
            data.recommendations.forEach(rec => {
                const col = document.createElement('div');
                col.className = 'col-md-4';
                col.innerHTML = `
                    <div class="p-4 rounded-4 bg-white bg-opacity-5 border border-white border-opacity-10 h-100 transition-hover">
                        <h6 class="fw-bold text-warning mb-2">${rec.title}</h6>
                        <p class="text-muted mb-0" style="font-size: 0.9rem;">${rec.text}</p>
                    </div>
                `;
                recommendationContainer.appendChild(col);
            });

            // Render Category Chart (Chart.js)
            const catCtx = document.getElementById('categoryChart').getContext('2d');
            if (window.catChartInstance) window.catChartInstance.destroy();
            window.catChartInstance = new Chart(catCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(data.charts.category_distribution),
                    datasets: [{
                        data: Object.values(data.charts.category_distribution),
                        backgroundColor: ['#f97316', '#fb923c', '#fbbf24', '#fcd34d', '#4ade80', '#22c55e', '#16a34a', '#3b82f6', '#06b6d4', '#8b5cf6', '#d946ef', '#ec4899']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: body.classList.contains('light-mode') ? '#1e293b' : '#94a3b8'
                            }
                        }
                    }
                }
            });

            // Render Top States List
            const stateList = document.getElementById('topStatesList');
            stateList.innerHTML = '';
            Object.entries(data.charts.top_states).forEach(([state, count], idx) => {
                const div = document.createElement('div');
                div.className = 'list-item d-flex justify-content-between align-items-center';
                div.innerHTML = `<span>${idx + 1}. <b>${state}</b></span> <span class="badge bg-opacity-10 bg-info text-info">${count.toLocaleString()}</span>`;
                stateList.appendChild(div);
            });

            // Map interaction (Choropleth)
            if (indiaGeoJson) {
                updateMapColors(data.charts.top_states, data.state_risks);
            }

            // Trend Chart with Forecast (Plotly)
            renderTrendChart(data.charts.yearly_trend);

        } catch (e) { console.error('Error loading dashboard:', e); }
    }

    async function loadStateAnalysis(state, year) {
        if (!state) return;
        try {
            const crimeType = crimeTypeSelect.value;
            const res = await fetch(`/api/state_analysis?state=${state}&year=${year}&per_capita=${perCapita}&crime_type=${crimeType}`);
            const data = await res.json();

            if (!data || data.error) {
                // If it's a 404/Missing Data error, show it gracefully
                document.getElementById('stateIntelligenceSection').classList.add('d-none');
                alert(data.error || 'Data not available for this selection.');
                return;
            }

            document.getElementById('stateIntelligenceSection').classList.remove('d-none');
            document.getElementById('analysisStateName').innerText = state;
            document.getElementById('analysisYear').innerText = year;
            document.getElementById('stateRiskStatus').innerText = data.risk_level || 'Low';
            document.getElementById('stateCasesSelected').innerText = (data.selected_year_cases || 0).toLocaleString();

            // New Forecast Indicators
            document.getElementById('forecastYearLabel').innerText = parseInt(year) + 1;
            const growth = data.predicted_growth_rate || 0;
            document.getElementById('statePredictedRate').innerText = (growth >= 0 ? '+' : '') + growth + '%';
            document.getElementById('statePredictedRate').className = `fw-bold ${growth >= 0 ? 'text-danger' : 'text-success'}`;

            const trendEl = document.getElementById('stateTrendIndicator');
            trendEl.innerText = `Trend: ${data.predicted_trend || 'Stable'}`;
            trendEl.className = `badge p-2 px-3 ${data.predicted_trend === 'Increase' ? 'bg-danger text-white' : (data.predicted_trend === 'Decrease' ? 'bg-success text-white' : 'bg-warning text-dark')}`;

            const confEl = document.getElementById('stateConfidenceIndicator');
            confEl.innerText = `Confidence: ${data.confidence || 'Medium'}`;
            confEl.className = `badge p-2 px-3 ${data.confidence === 'High' ? 'bg-success text-white' : 'bg-info text-white'}`;

            const nextYear = parseInt(year) + 1;
            const forecastEntry = (data.forecast || []).find(f => f.year === nextYear);
            const forecastVal = forecastEntry ? forecastEntry.yhat : 0;
            document.getElementById('statePredictionNext').innerText = forecastVal.toLocaleString();

            // Populate Category Table
            const catTable = document.getElementById('stateCategoryTableBody');
            catTable.innerHTML = '';
            const categories = data.categories || {};
            Object.entries(categories).sort((a, b) => b[1] - a[1]).forEach(([cat, count]) => {
                const share = data.selected_year_cases ? ((count / data.selected_year_cases) * 100).toFixed(1) : 0;
                catTable.innerHTML += `<tr><td class="border-0 py-1 text-white-50 small">${cat}</td><td class="border-0 py-1 text-end small">${count.toLocaleString()}</td><td class="border-0 py-1 text-end small"><span class="badge bg-opacity-10 bg-info text-info p-1 px-2" style="font-size: 0.7rem">${share}%</span></td></tr>`;
            });

            // Populate District Table
            const distTable = document.getElementById('districtTableBody');
            if (distTable) {
                distTable.innerHTML = '';
                const districts = data.districts || {};
                Object.entries(districts).forEach(([dist, count]) => {
                    const shortDist = dist.includes('_Dist_') ? 'Dist ' + dist.split('_Dist_')[1] : dist;
                    distTable.innerHTML += `<tr><td class="border-0 py-1 text-white-50 small">${shortDist}</td><td class="border-0 py-1 text-end small fw-bold">${count.toLocaleString()}</td></tr>`;
                });
            }

            // Local Trend Chart (Professional CI Band)
            const histYears = Object.keys(data.historical);
            const histValues = Object.values(data.historical);
            const lastYear = histYears[histYears.length - 1];
            const lastVal = histValues[histValues.length - 1];

            const forecastYears = data.forecast.map(d => d.year);
            const yhat = data.forecast.map(d => d.yhat);
            const upper = data.forecast.map(d => d.upper);
            const lower = data.forecast.map(d => d.lower);

            const traceHist = {
                x: histYears, y: histValues,
                type: 'scatter', mode: 'lines+markers', name: 'Historical',
                line: { shape: 'spline', color: '#0ea5e9', width: 3 },
                marker: { color: histYears.map((y, i) => (y == year && data.is_anomaly) ? '#ef4444' : '#0ea5e9'), size: 8 }
            };

            // Shaded CI Band
            const traceLower = {
                x: [lastYear, ...forecastYears],
                y: [lastVal, ...lower],
                type: 'scatter', fill: null, mode: 'lines', line: { width: 0 }, showlegend: false, hoverinfo: 'none'
            };
            const traceUpper = {
                x: [lastYear, ...forecastYears],
                y: [lastVal, ...upper],
                type: 'scatter', fill: 'tonexty', fillcolor: 'rgba(245, 158, 11, 0.15)',
                mode: 'lines', line: { width: 0 }, name: '95% Confidence', hoverinfo: 'none'
            };

            const tracePred = {
                x: [lastYear, ...forecastYears],
                y: [lastVal, ...yhat],
                type: 'scatter', mode: 'lines+markers', name: 'AI Forecast',
                line: { dash: 'dash', color: '#f59e0b', width: 3 }
            };

            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#94a3b8' }, margin: { t: 10, b: 30, l: 50, r: 10 },
                xaxis: { gridcolor: 'rgba(255,255,255,0.05)', tickfont: { size: 10 } },
                yaxis: { gridcolor: 'rgba(255,255,255,0.05)', tickfont: { size: 10 } },
                showlegend: false
            };
            Plotly.newPlot('statePlotlyTrend', [traceLower, traceUpper, traceHist, tracePred], layout);

        } catch (e) { console.error('Error loading state analysis:', e); }
    }

    async function renderTrendChart(history) {
        const crimeType = crimeTypeSelect.value;
        const forecastRes = await fetch(`/api/predict?year=${yearSelect.value}&crime_type=${crimeType}`);
        const forecast = await forecastRes.json();

        const histYears = Object.keys(history);
        const histValues = Object.values(history);
        const lastYear = histYears[histYears.length - 1];
        const lastVal = histValues[histValues.length - 1];

        const forecastYears = Object.keys(forecast);
        const yhat = Object.values(forecast).map(d => d.yhat);
        const upper = Object.values(forecast).map(d => d.upper);
        const lower = Object.values(forecast).map(d => d.lower);

        const traceHist = {
            x: histYears, y: histValues,
            type: 'scatter', mode: 'lines+markers', name: 'Historical',
            line: { shape: 'spline', color: '#0ea5e9', width: 3 },
            marker: { size: 8 }
        };

        const traceLower = {
            x: [lastYear, ...forecastYears],
            y: [lastVal, ...lower],
            type: 'scatter', fill: null, mode: 'lines', line: { width: 0 }, showlegend: false, hoverinfo: 'none'
        };
        const traceUpper = {
            x: [lastYear, ...forecastYears],
            y: [lastVal, ...upper],
            type: 'scatter', fill: 'tonexty', fillcolor: 'rgba(245, 158, 11, 0.12)',
            mode: 'lines', line: { width: 0 }, name: '95% Uncertainty', hoverinfo: 'none'
        };

        const tracePred = {
            x: [lastYear, ...forecastYears],
            y: [lastVal, ...yhat],
            type: 'scatter', mode: 'lines+markers', name: 'AI Forecast',
            line: { dash: 'dash', color: '#f59e0b', width: 3 }
        };

        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: body.classList.contains('light-mode') ? '#1e293b' : '#94a3b8' },
            margin: { t: 30, b: 30, l: 60, r: 10 },
            xaxis: { gridcolor: body.classList.contains('light-mode') ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)', tickfont: { size: 10 } },
            yaxis: { gridcolor: body.classList.contains('light-mode') ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)', tickfont: { size: 10 } },
            legend: { orientation: 'h', x: 0, y: 1.1, font: { size: 10 } },
            hovermode: 'x unified'
        };

        Plotly.newPlot('plotlyTrend', [traceLower, traceUpper, traceHist, tracePred], layout);
    }

    function updateMapColors(stateStats, risks) {
        if (geoLayer) map.removeLayer(geoLayer);

        geoLayer = L.geoJson(indiaGeoJson, {
            style: (feature) => {
                const props = feature.properties;
                const stateName = props.ST_NM || props.state_name || props.NAME_1 || props.name;
                const risk = risks[stateName] || 'Low';

                return {
                    fillColor: risk === 'High' ? '#f43f5e' : (risk === 'Medium' ? '#f59e0b' : '#10b981'),
                    weight: 1.5,
                    opacity: 1,
                    color: 'white', // Clear Political Borders
                    fillOpacity: 0.8,
                    className: 'state-polygon'
                };
            },
            onEachFeature: (feature, layer) => {
                const props = feature.properties;
                const stateName = props.ST_NM || props.state_name || props.NAME_1 || props.name;
                const risk = risks[stateName] || 'Low';
                const count = stateStats[stateName] || 0;

                // Enhanced Political Tooltip (Light)
                layer.bindTooltip(`
                    <div class="px-3 py-2">
                        <div class="fw-bold text-dark border-bottom border-dark border-opacity-10 mb-2" style="font-size: 1.1rem">${stateName}</div>
                        <div class="small text-muted">${perCapita ? 'Per 100k Rate' : 'Total Volume'}: <span class="text-dark fw-bold">${count.toLocaleString()}</span></div>
                        <div class="small text-muted">Risk Intelligence: <span class="badge ${risk === 'High' ? 'bg-danger' : (risk === 'Medium' ? 'bg-warning text-dark' : 'bg-success')} py-1 px-2 mt-1" style="font-size: 0.7rem">${risk}</span></div>
                    </div>
                `, { sticky: true, className: 'political-tooltip', opacity: 1 });

                layer.on({
                    mouseover: (e) => {
                        const l = e.target;
                        l.setStyle({
                            fillOpacity: 0.85,
                            weight: 3,
                            color: '#fff'
                        });
                        l.bringToFront();
                    },
                    mouseout: (e) => {
                        geoLayer.resetStyle(e.target);
                    },
                    click: (e) => {
                        stateSelect.value = stateName;
                        const event = new Event('change');
                        stateSelect.dispatchEvent(event);
                        map.fitBounds(e.target.getBounds());
                    }
                });
            }
        }).addTo(map);

        // Auto-fit bounds on first load
        if (indiaGeoJson) {
            map.fitBounds(geoLayer.getBounds(), { padding: [20, 20] });
        }
    }

    // Load GeoJSON and Start
    fetch('/static/data/india_states.json')
        .then(res => res.json())
        .then(json => {
            indiaGeoJson = json;
            loadDashboard(2025);
        })
        .catch(err => {
            console.error('GeoJSON Load Error:', err);
            loadDashboard(2025); // Fallback to load metrics even if map fails
        })
        .finally(() => {
            setTimeout(() => {
                loader.style.opacity = '0';
                setTimeout(() => loader.style.display = 'none', 500);
            }, 1000);
        });
});
