import pandas as pd
import json

def validate_merge():
    # Load dataset
    df = pd.read_csv('dataset/india_crime_data_cleaned.csv')
    dataset_states = set(df['State/UT'].unique())
    
    # Load GeoJSON
    with open('static/data/india_states.json', 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    geojson_states = set()
    for feature in geojson_data['features']:
        props = feature['properties']
        name = props.get('ST_NM') or props.get('name') or props.get('NAME_1') or props.get('state_name')
        if name:
            geojson_states.add(name)
    
    # Normalization Map
    norm_map = {
        "Andaman and Nicobar": "Andaman & Nicobar Islands",
        "Andaman & Nicobar": "Andaman & Nicobar Islands",
        "Dadra and Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
        "Daman and Diu": "Dadra & Nagar Haveli and Daman & Diu",
        "Dadra & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
        "Jammu and Kashmir": "Jammu & Kashmir",
        "Orissa": "Odisha",
        "Uttaranchal": "Uttarakhand",
        "NCT of Delhi": "Delhi",
        "Pondicherry": "Puducherry"
    }
    
    print("--- Audit Summary ---")
    print(f"Dataset States: {len(dataset_states)}")
    print(f"GeoJSON States: {len(geojson_states)}")
    
    unmatched_dataset = dataset_states - geojson_states
    unmatched_geojson = geojson_states - dataset_states
    
    print(f"\nUnmatched in Dataset: {unmatched_dataset}")
    print(f"Unmatched in GeoJSON: {unmatched_geojson}")
    
    # Check with normalization
    normalized_geojson = set()
    for name in geojson_states:
        normalized_geojson.add(norm_map.get(name, name))
    
    still_unmatched = dataset_states - normalized_geojson
    print(f"\nStill Unmatched after Norm: {still_unmatched}")
    
    if not still_unmatched:
        print("\nSUCCESS: 100% Mapping Achieved!")

if __name__ == "__main__":
    validate_merge()
