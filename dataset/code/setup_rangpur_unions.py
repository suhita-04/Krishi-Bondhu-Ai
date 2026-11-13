# File: setup_rangpur_unions.py
import pandas as pd
import numpy as np

def generate_rangpur_536_unions():
    print("--- Generating Master List of 536 Unions with Land Elevation & Crop Suitability ---")
    
    rangpur_districts = [
        {"District": "Rangpur", "Lat": 25.7439, "Lon": 89.2752, "Unions": 76, "River_Basin": "Teesta", "Base_Elev_m": 34.0,
         "Famous_Specialty": "Haribhanga_Mango_&_Vegetables",
         "Upazilas": ["Rangpur Sadar", "Badarganj", "Gangachara", "Kaunia", "Mithapukur", "Pirgachha", "Pirganj", "Taraganj"]},
        {"District": "Dinajpur", "Lat": 25.6217, "Lon": 88.6354, "Unions": 103, "River_Basin": "Atrai_Punarbhaba", "Base_Elev_m": 39.0,
         "Famous_Specialty": "Bedana_Litchi_&_High_Value_Crops",
         "Upazilas": ["Dinajpur Sadar", "Birampur", "Birganj", "Biral", "Bochaganj", "Chirirbandar", "Phulbari", "Ghoraghat", "Hakimpur", "Kaharole", "Khansama", "Nawabganj", "Parbatipur"]},
        {"District": "Kurigram", "Lat": 25.8054, "Lon": 89.6361, "Unions": 72, "River_Basin": "Brahmaputra_Dharla", "Base_Elev_m": 24.0,
         "Famous_Specialty": "Char_Sweet_Gourd_Chili_&_Mustard",
         "Upazilas": ["Kurigram Sadar", "Bhurungamari", "Char Rajibpur", "Chilmari", "Phulbari", "Nageshwari", "Rajarhat", "Raomari", "Ulipur"]},
        {"District": "Gaibandha", "Lat": 25.3288, "Lon": 89.5280, "Unions": 81, "River_Basin": "Brahmaputra_Teesta", "Base_Elev_m": 25.5,
         "Famous_Specialty": "Banana_Chili_&_Maize",
         "Upazilas": ["Gaibandha Sadar", "Fulchhari", "Gobindaganj", "Palashbari", "Sadullapur", "Saghata", "Sundarganj"]},
        {"District": "Nilphamari", "Lat": 25.9317, "Lon": 88.8560, "Unions": 60, "River_Basin": "Teesta", "Base_Elev_m": 41.0,
         "Famous_Specialty": "Potato_Brinjal_&_Maize",
         "Upazilas": ["Nilphamari Sadar", "Dimla", "Domar", "Jaldhaka", "Kishoreganj", "Saidpur"]},
        {"District": "Panchagarh", "Lat": 26.3411, "Lon": 88.5541, "Unions": 43, "River_Basin": "Mahananda_Karatoa", "Base_Elev_m": 62.0,
         "Famous_Specialty": "Malta_Orange_Watermelon_&_Vegetables",
         "Upazilas": ["Panchagarh Sadar", "Atwari", "Boda", "Debiganj", "Tetulia"]},
        {"District": "Thakurgaon", "Lat": 26.0336, "Lon": 88.4616, "Unions": 56, "River_Basin": "Tangon", "Base_Elev_m": 50.0,
         "Famous_Specialty": "Mango_Orchard_Wheat_&_Vegetables",
         "Upazilas": ["Thakurgaon Sadar", "Baliadangi", "Haripur", "Pirganj", "Ranisankail"]},
        {"District": "Lalmonirhat", "Lat": 25.9923, "Lon": 89.2847, "Unions": 45, "River_Basin": "Teesta_Dharla", "Base_Elev_m": 31.0,
         "Famous_Specialty": "Maize_Vegetables_&_Char_Crops",
         "Upazilas": ["Lalmonirhat Sadar", "Aditmari", "Hatibandha", "Kaliganj", "Patgram"]}
    ]
    
    np.random.seed(2026)
    records = []
    union_counter = 1
    
    # Upazilas specifically renowned for High Land Orchards (Mango/Litchi/Orange)
    orchard_upazilas = [
        "Mithapukur", "Badarganj", "Pirganj", "Dinajpur Sadar", "Biral", "Birganj", 
        "Chirirbandar", "Baliadangi", "Ranisankail", "Tetulia", "Panchagarh Sadar", "Gobindaganj"
    ]
    # Upazilas with extensive Char / Riverine sandy-loam land
    char_upazilas = [
        "Char Rajibpur", "Chilmari", "Raomari", "Fulchhari", "Sundarganj", 
        "Gangachara", "Kaunia", "Dimla", "Hatibandha", "Kaliganj"
    ]
    
    for dist in rangpur_districts:
        n_unions = dist["Unions"]
        upazilas = dist["Upazilas"]
        for i in range(n_unions):
            upazila = upazilas[i % len(upazilas)]
            u_lat = round(dist["Lat"] + np.random.uniform(-0.18, 0.18), 4)
            u_lon = round(dist["Lon"] + np.random.uniform(-0.18, 0.18), 4)
            elev_m = round(dist["Base_Elev_m"] + np.random.uniform(-5.0, 8.0), 1)
            
            # Determine Land Elevation Type, Soil Texture, and Best Agricultural Use
            if upazila in orchard_upazilas or (elev_m >= 40.0 and i % 3 == 0):
                land_type = "High_Land_Vita"
                soil_texture = "Reddish_Loamy_Doash"
                drainage = "Excellent_Well_Drained"
                best_use = "Fruit_Orchard_&_Winter_Vegetables"
                orchard_suitability = "Highly_Suitable (Mango/Litchi/Papaya/Malta)"
                veg_suitability = "Highly_Suitable"
            elif upazila in char_upazilas or (elev_m < 26.0 and i % 3 == 0):
                land_type = "Char_Alluvial_Land"
                soil_texture = "Sandy_Loam_Beles_Doash"
                drainage = "Seasonal_Flood_Prone"
                best_use = "Char_Vegetables_Pumpkin_Chili_&_Oilseeds"
                orchard_suitability = "Not_Suitable_Flood_Risk"
                veg_suitability = "Suitable_For_Creeper_Veg_&_Chili"
            elif i % 2 == 0:
                land_type = "Medium_High_Land"
                soil_texture = "Fertile_Loamy_Doash"
                drainage = "Good_Irrigated_Vegetable_Bed"
                best_use = "Intensive_Vegetables_Potato_&_Pulses"
                orchard_suitability = "Moderately_Suitable (Banana/Papaya)"
                veg_suitability = "Optimal_All_Season_Vegetables"
            else:
                land_type = "Medium_Low_Land"
                soil_texture = "Clay_Loam_Etel_Doash"
                drainage = "Moderate_Water_Retaining"
                best_use = "Cereal_Grain_&_Pulse_Oilseed_Rotation"
                orchard_suitability = "Low_Suitability_Waterlogging_Risk"
                veg_suitability = "Suitable_In_Rabi_Winter_Only"

            records.append({
                "Union_ID": f"RNG_U{str(union_counter).zfill(3)}",
                "Division": "Rangpur",
                "District": dist["District"],
                "Upazila": upazila,
                "Union_Name": f"{upazila}_Union_{i // len(upazilas) + 1}",
                "Lat": u_lat,
                "Lon": u_lon,
                "Elevation_m": elev_m,
                "Land_Elevation_Type": land_type,
                "Soil_Texture": soil_texture,
                "Drainage_And_Irrigation": drainage,
                "Orchard_Suitability": orchard_suitability,
                "Vegetable_Suitability": veg_suitability,
                "Recommended_Farming_Pattern": best_use,
                "Regional_Specialty": dist["Famous_Specialty"],
                "River_Basin": dist["River_Basin"]
            })
            union_counter += 1
            
    df_unions = pd.DataFrame(records)
    df_unions.to_csv("rangpur_536_unions.csv", index=False)
    print(f"Success! Saved {len(df_unions)} unions with topography & suitability to 'rangpur_536_unions.csv'.")
    return df_unions

if __name__ == "__main__":
    generate_rangpur_536_unions()