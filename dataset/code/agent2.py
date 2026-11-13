import os
import requests
import pandas as pd
import time

def fetch_nasa_monthly(lat, lon, parameters):
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    payload = {
        "parameters": parameters,
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": "1981",
        "end": "2026",
        "format": "JSON"
    }
    try:
        r = requests.get(url, params=payload, timeout=30)
        if r.status_code == 200:
            params_data = r.json()['properties']['parameter']
            df = pd.DataFrame(params_data)
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'YearMonth'}, inplace=True)
            # Remove annual average rows (ending with '13')
            df = df[~df['YearMonth'].str.endswith('13')]
            return df
    except Exception as e:
        print(f"API Error: {e}")
    return pd.DataFrame()

def build_agent2_monthly_master():
    print("=== Building Agent 2: Thermal & Drought Stress (Monthly Master) ===")
    if not os.path.exists("rangpur_536_unions.csv"):
        print("Error: rangpur_536_unions.csv not found.")
        return
        
    df_unions = pd.read_csv("rangpur_536_unions.csv")
    parameters = "T2M,PRECTOTCORR,GWETTOP"
    all_rows = []
    
    for index, row in df_unions.iterrows():
        print(f"[{index+1}/{len(df_unions)}] Fetching Monthly Agent 2 for: {row['Union_Name']}")
        df_union = fetch_nasa_monthly(row['Lat'], row['Lon'], parameters)
        
        if not df_union.empty:
            df_union.insert(0, 'Union_ID', row['Union_ID'])
            df_union.insert(1, 'Union_Name', row['Union_Name'])
            df_union.insert(2, 'Upazila', row['Upazila'])
            df_union.insert(3, 'District', row['District'])
            df_union.insert(4, 'Lat', row['Lat'])
            df_union.insert(5, 'Lon', row['Lon'])
            all_rows.append(df_union)
        time.sleep(0.1)
        
    if all_rows:
        master_df = pd.concat(all_rows, ignore_index=True)
        master_df.replace(-999, pd.NA, inplace=True)
        master_df.ffill(inplace=True)
        
        master_df.to_csv("agent2_536_unions_MONTHLY_master.csv", index=False)
        master_df.to_json("agent2_536_unions_MONTHLY_master.json", orient="records", indent=4)
        print("Success! Saved 'agent2_536_unions_MONTHLY_master.csv'.")

if __name__ == "__main__":
    build_agent2_monthly_master()
