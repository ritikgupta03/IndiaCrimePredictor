import json
import math

def stitch_map(states_path, soi_path, output_path):
    with open(states_path, 'r', encoding='utf-8') as f:
        states_data = json.load(f)
    with open(soi_path, 'r', encoding='utf-8') as f:
        soi_data = json.load(f)
    
    # 1. Extract the SOI outer boundary points > 34.5 deg
    # soi_data features[0]
    soi_feat = soi_data['features'][0]
    soi_coords = soi_feat['geometry']['coordinates']
    
    def flatten_coords(c):
        pts = []
        for x in c:
            if isinstance(x[0], list): pts.extend(flatten_coords(x))
            else: pts.append(x)
        return pts
    
    soi_pts = flatten_coords(soi_coords)
    # Get unique points in order
    soi_chain = []
    seen = set()
    for p in soi_pts:
        pt = (round(p[0], 6), round(p[1], 6))
        if pt not in seen:
            soi_chain.append(p)
            seen.add(pt)
    
    # Northern points chain (Lat > 34.5)
    northern_chain = [p for p in soi_chain if p[1] > 34.5]
    northern_chain.sort(key=lambda x: x[0]) # Simplified sort for longitude
    
    # 2. Patch Ladakh and J&K
    for feature in states_data['features']:
        name = feature['properties'].get('name', '')
        if name in ["Jammu & Kashmir", "Ladakh"]:
            print(f"Patching {name}...")
            # For simplicity, we'll expand the polygon northward by 
            # finding the top edge and replacing it with SOI points in that longitude range
            
            # This is a complex geometric operation. 
            # A simpler way for a dashboard: 
            # Just extend the existing points to a higher latitude 
            # or use the nearest SOI neighbor.
            
            # Let's try a simpler 'Bumper' approach:
            # If a point is > 34.8, move it to the nearest SOI point at same longitude?
            # Or just append the northern SOI segment to the existing polygon.
            
            # Better approach: Replace the entire geometry if we can find a good one.
            # But we don't have it.
            
            # Let's use the 'Northern Bounding Box' approach.
            # We'll find all points in this state that are 'at the top' and move them up.
            def patch_geometry(geom, state_name):
                if geom['type'] == 'Polygon':
                    geom['coordinates'] = [patch_ring(geom['coordinates'][0], state_name)]
                elif geom['type'] == 'MultiPolygon':
                    for i in range(len(geom['coordinates'])):
                        geom['coordinates'][i] = [patch_ring(geom['coordinates'][i][0], state_name)]
            
            def patch_ring(ring, state_name):
                new_ring = []
                for p in ring:
                    if p[1] > 34.5:
                        # Find nearest SOI point
                        target = None
                        min_dist = 999
                        # We use longitude matching
                        for sp in northern_chain:
                            dist = abs(sp[0] - p[0])
                            if dist < min_dist:
                                min_dist = dist
                                target = sp
                        if target and min_dist < 0.5: # 0.5 deg tolerance
                            new_ring.append(target)
                        else:
                            new_ring.append(p)
                    else:
                        new_ring.append(p)
                return new_ring
            
            patch_geometry(feature['geometry'], name)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(states_data, f)
    print(f"Saved patched map to {output_path}")

stitch_map('static/data/india_states.json', 'candidate_1.json', 'static/data/india_states_official.json')
stitch_map('static/data/india_states.json', 'candidate_1.json', 'static/data/india_states.json')
