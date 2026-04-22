from flask import Flask, render_template, jsonify, request, send_file
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from forecasting_utils import (
    BASE_DF as raw_df, 
    POP_DF as pop_df, 
    generate_safe_forecast, 
    calculate_per_capita, 
    get_anomaly_status, 
    get_state_risk
)

app = Flask(__name__)

# Data Integrity: Remove any rows where State, District, or Category contains "Total"
# This prevents double aggregation if the raw data had summary rows.
df = raw_df[
    ~raw_df['State/UT'].str.contains('Total', case=False, na=False) &
    ~raw_df['District'].str.contains('Total', case=False, na=False) &
    ~raw_df['Crime Category'].str.contains('Total', case=False, na=False)
].copy()

# Categorization for filtering
IPC_HEADS = [
    'Arson', 'Assault on Women', 'Attempt to Murder', 'Burglary', 'Cheating', 
    'Child Abuse', 'Counterfeiting', 'Cruelty by Husband', 'Culpable Homicide', 
    'Dowry Deaths', 'Extortion', 'Forgery', 'Grievous Hurt', 'Human Trafficking', 
    'Kidnapping & Abduction', 'Murder', 'Rape', 'Riots', 'Robbery', 
    'Sexual Harassment', 'Theft'
]
SLL_HEADS = ['Corruption Cases', 'Cyber Crimes', 'Financial Fraud', 'Possession of Drugs']

def filter_df_by_type(input_df, crime_type):
    if crime_type == 'ipc':
        return input_df[input_df['Crime Category'].isin(IPC_HEADS)]
    elif crime_type == 'sll':
        return input_df[input_df['Crime Category'].isin(SLL_HEADS)]
    return input_df

# State Name Normalization Mapping for GeoJSON alignment
norm_map = {
    "Andaman and Nicobar": "Andaman & Nicobar Islands",
    "Andaman & Nicobar Islands": "Andaman & Nicobar Islands",
    "Dadra and Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
    "Daman and Diu": "Dadra & Nagar Haveli and Daman & Diu",
    "Dadra & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Orissa": "Odisha",
    "Uttaranchal": "Uttarakhand",
    "NCT of Delhi": "Delhi",
    "Pondicherry": "Puducherry"
}

def get_dynamic_risks(year, use_per_capita=False):
    """Calculate risks using Quantile Classification"""
    temp_df = df[df['Year'] == year].copy()
    if use_per_capita:
        pop_year = pop_df[pop_df['Year'] == year]
        temp_df = temp_df.merge(pop_year[['State/UT', 'Population']], on='State/UT')
        temp_df['Rate'] = (temp_df['Number of Cases'] / temp_df['Population']) * 100000
        state_metrics = temp_df.groupby('State/UT')['Rate'].sum().sort_values()
    else:
        state_metrics = temp_df.groupby('State/UT')['Number of Cases'].sum().sort_values()
    
    q_low = state_metrics.quantile(0.3)
    q_high = state_metrics.quantile(0.7)
    
    risks = {}
    for state, val in state_metrics.items():
        if val >= q_high: risks[state] = "High"
        elif val >= q_low: risks[state] = "Medium"
        else: risks[state] = "Low"
    return risks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    try:
        year = int(request.args.get('year', 2025))
        use_per_capita = request.args.get('per_capita', 'false').lower() == 'true'
        crime_type = request.args.get('crime_type', 'all').lower()
        
        yearly_raw = df[df['Year'] == year].copy()
        yearly_df = filter_df_by_type(yearly_raw, crime_type)
        
        if yearly_df.empty:
            return jsonify({"error": "No data for this filter/year"}), 404

        total_crimes = int(yearly_df['Number of Cases'].sum())
        
        # Simple National Forecast proxy (Filtered)
        current_filtered_df = filter_df_by_type(df, crime_type)
        # Use a high-volume state as proxy for trend shape
        state_df = current_filtered_df[current_filtered_df['State/UT'] == 'Uttar Pradesh'].groupby('Year')['Number of Cases'].sum().reset_index()
        
        # Stability: Simple estimate if forecast needs it
        forecast_val = total_crimes * 1.02 # Proxy for now or call utility with filtered df
        
        # Charts
        cat_dist = yearly_df.groupby('Crime Category')['Number of Cases'].sum().to_dict()
        yearly_trend = current_filtered_df.groupby('Year')['Number of Cases'].sum().to_dict()
        
        if use_per_capita:
            pop_year = pop_df[pop_df['Year'] == year]
            merged = yearly_df.merge(pop_year[['State/UT', 'Population']], on='State/UT')
            merged['Rate'] = (merged['Number of Cases'] / merged['Population']) * 100000
            top_states = merged.groupby('State/UT')['Rate'].sum().sort_values(ascending=False).head(10).to_dict()
        else:
            top_states = yearly_df.groupby('State/UT')['Number of Cases'].sum().sort_values(ascending=False).head(10).to_dict()
        
        # State Risks for Map (Filtered)
        # We need to compute state risks based on the FILTERED data
        state_data = yearly_df.groupby('State/UT')['Number of Cases'].sum()
        if use_per_capita:
            pop_year = pop_df[pop_df['Year'] == year]
            merged_risk = yearly_df.merge(pop_year[['State/UT', 'Population']], on='State/UT')
            merged_risk['Rate'] = (merged_risk['Number of Cases'] / merged_risk['Population']) * 100000
            state_data = merged_risk.groupby('State/UT')['Rate'].sum()
            
        q_low = state_data.quantile(0.33)
        q_high = state_data.quantile(0.66)
        
        state_risks = {}
        for s in df['State/UT'].unique():
            val = state_data.get(s, 0)
            if val >= q_high: state_risks[s] = "High"
            elif val >= q_low: state_risks[s] = "Medium"
            else: state_risks[s] = "Low"

        return jsonify({
            'kpis': {
                'total_crimes': total_crimes,
                'forecast': {"count": int(forecast_val), "growth": 2.0, "trend": "Stable"},
                'per_capita_active': use_per_capita,
                'crime_type': crime_type
            },
            'charts': {
                'category_distribution': cat_dist,
                'top_states': top_states,
                'yearly_trend': yearly_trend
            },
            'state_risks': state_risks,
            'insights': f"Total {crime_type.upper()} crime volume recorded in {year} is {total_crimes:,} cases.",
            'recommendations': [
                {"title": "Resource Allocation", "text": "Focus on high-volume zones identified in the map."},
                {"title": "Data Governance", "text": "Absolute count reflects unique category aggregation only."}
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/state_analysis')
def get_state_analysis():
    try:
        raw_state = request.args.get('state')
        year = int(request.args.get('year', 2025))
        use_per_capita = request.args.get('per_capita', 'false').lower() == 'true'
        crime_type = request.args.get('crime_type', 'all').lower()
        
        if not raw_state:
            return jsonify({"error": "State parameter is required"}), 400
            
        state = norm_map.get(raw_state, raw_state)
        # Apply filter to full df for state historicals
        filtered_df = filter_df_by_type(df, crime_type)
        state_df = filtered_df[filtered_df['State/UT'] == state].sort_values('Year')
        
        if state_df.empty:
            return jsonify({
                "error": f"No {crime_type.upper()} data found for {state}. Try changing the filter.",
                "state": state
            }), 404
            
        current_year_df = state_df[state_df['Year'] == year]
        current_cases = int(current_year_df['Number of Cases'].sum()) if not current_year_df.empty else 0
        
        # Historical Data
        historical = {}
        for y in sorted(state_df['Year'].unique()):
            cases = int(state_df[state_df['Year'] == y]['Number of Cases'].sum())
            historical[int(y)] = calculate_per_capita(cases, state, y) if use_per_capita else cases

        # Simple Forecast (Based on filtered history if possible)
        forecast = []
        if len(historical) >= 2:
            X = np.array(list(historical.keys())).reshape(-1, 1)
            y = np.array(list(historical.values()))
            model = LinearRegression().fit(X, y)
            for i in range(1, 4):
                f_year = int(year + i)
                val = max(0, int(model.predict([[f_year]])[0]))
                forecast.append({
                    "year": f_year, 
                    "yhat": val, 
                    "upper": int(val*1.15), 
                    "lower": int(val*0.85)
                })

        return jsonify({
            'state': state,
            'selected_year_cases': calculate_per_capita(current_cases, state, year) if use_per_capita else current_cases,
            'historical': historical,
            'forecast': forecast,
            'risk_level': "High" if (current_cases > state_df['Number of Cases'].mean() if not state_df.empty else False) else "Medium",
            'is_anomaly': get_anomaly_status(state, year),
            'predicted_growth_rate': round(((forecast[0]['yhat'] - historical[year]) / historical[year] * 100), 2) if forecast and historical.get(year) and historical[year] > 0 else 0,
            'predicted_trend': "Increase" if (forecast[0]['yhat'] > historical.get(year, 0) if forecast and historical else False) else "Stable",
            'confidence': "High" if len(historical) > 5 else "Medium",
            'categories': state_df[state_df['Year'] == year].groupby('Crime Category')['Number of Cases'].sum().to_dict(),
            'districts': state_df[state_df['Year'] == year].groupby('District')['Number of Cases'].sum().sort_values(ascending=False).head(10).to_dict()
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict')
def predict_trend():
    try:
        year = int(request.args.get('year', 2025))
        crime_type = request.args.get('crime_type', 'all').lower()
        states = df['State/UT'].unique()
        
        filtered_df = filter_df_by_type(df, crime_type)
        
        agg_forecast = {}
        # Prediction for National Trend
        # Group by Year first to get global trend
        nat_historical = filtered_df.groupby('Year')['Number of Cases'].sum().reset_index().sort_values('Year')
        
        if len(nat_historical) >= 3:
            X = nat_historical['Year'].values.reshape(-1, 1)
            y = nat_historical['Number of Cases'].values
            model = LinearRegression().fit(X, y)
            for i in range(1, 4):
                f_year = int(year + i)
                val = max(0, int(model.predict([[f_year]])[0]))
                agg_forecast[f_year] = {
                    'yhat': val,
                    'upper': int(val * 1.1),
                    'lower': int(val * 0.9)
                }
        return jsonify(agg_forecast)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/export/pdf')
def export_pdf():
    try:
        current_year = 2025
        crime_type = request.args.get('crime_type', 'all').lower()
        filtered_df = filter_df_by_type(df, crime_type)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Title Page
        p.setFont("Helvetica-Bold", 20)
        p.drawString(100, 750, "India Crime Intelligence & Risk Report")
        p.line(100, 745, 520, 745)
        
        p.setFont("Helvetica", 10)
        p.drawString(100, 730, f"Analysis Period: 2015 - 2025")
        p.drawString(100, 715, f"Methodology: {crime_type.upper()} Categorical Analysis")
        p.drawString(100, 700, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. Executive Intelligence (National Level)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 660, f"1. {crime_type.upper()} Strategic Overview")
        p.setFont("Helvetica", 11)
        
        total_crimes = int(filtered_df[filtered_df['Year'] == current_year]['Number of Cases'].sum())
        
        # National Forecast Proxy (Using UP as baseline for national trend shape)
        f_nat = generate_safe_forecast("Uttar Pradesh", current_year, horizon=1)
        yhat = f_nat[0]['yhat'] if f_nat else 0
        upper = f_nat[0]['upper'] if f_nat else 0
        lower = f_nat[0]['lower'] if f_nat else 0
        
        p.drawString(120, 640, f"- Latest {crime_type.upper()} Volume ({current_year}): {total_crimes:,} cases")
        p.drawString(120, 620, f"- Stabilized Forecast ({current_year + 1}): {yhat:,} (Est. Range: {lower:,} - {upper:,})")
        
        # 2. Key Jurisdiction Risk Assessment
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 580, "2. High-Risk Jurisdiction Analysis")
        y_pos = 560
        p.setFont("Helvetica", 10)
        
        high_risk_states = []
        for state in df['State/UT'].unique():
            if get_state_risk(state, current_year) == "High":
                high_risk_states.append(state)
        
        high_risk_states = sorted(high_risk_states)[:12]
        
        p.drawString(120, y_pos, "Jurisdictions Identified with Elevated Risk Levels:")
        y_pos -= 20
        for i in range(0, len(high_risk_states), 2):
            row = high_risk_states[i:i+2]
            p.drawString(140, y_pos, " • " + "   • ".join(row))
            y_pos -= 15
        
        # 3. Forecast Trajectory (3-Year Outlook)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y_pos - 20, "3. Multi-Year Tactical Projection")
        y_pos -= 40
        p.setFont("Helvetica", 11)
        
        outlook = generate_safe_forecast("Uttar Pradesh", current_year, horizon=3)
        for entry in outlook:
            p.drawString(120, y_pos, f"• {entry['year']}: {entry['yhat']:,} cases (Est. Range: {entry['lower']:,} - {entry['upper']:,})")
            y_pos -= 20

        # Footer
        p.setFont("Helvetica-Oblique", 8)
        p.drawString(100, 50, "Classification: Stabilized Intelligence Report - Engine: LinReg-v1.2")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='India_Crime_Intelligence_Report.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": f"PDF Generation Failed: {str(e)}"}), 500

@app.route('/api/export/csv')
def export_csv():
    csv_path = 'dataset/india_crime_data.csv'
    df.to_csv(csv_path, index=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
