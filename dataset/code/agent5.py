# File: agent5.py
import os
import requests
import pandas as pd
import numpy as np
from setup_rangpur_unions import generate_rangpur_536_unions

def get_bangladesh_season(month):
    if month in [3, 4, 5, 6]:
        return "Kharif-1 (Pre-Monsoon/Summer)"
    elif month in [7, 8, 9, 10]:
        return "Kharif-2 (Monsoon)"
    else:
        return "Rabi (Winter)"

def fetch_world_bank_cpi(start_year=1980, end_year=2026):
    """Fetches historical CPI inflation data for Bangladesh from World Bank API."""
    url = "http://api.worldbank.org/v2/country/BD/indicator/FP.CPI.TOTL"
    payload = {"date": f"{start_year}:{end_year}", "format": "json", "per_page": 100}
    cpi_dict = {}
    try:
        r = requests.get(url, params=payload, timeout=20)
        if r.status_code == 200:
            for d in r.json()[1]:
                if d["value"] is not None:
                    cpi_dict[int(d["date"])] = float(d["value"])
    except Exception as e:
        print(f"World Bank CPI API warning, using calibrated curve: {e}")
        
    all_years = list(range(start_year, end_year + 1))
    df_cpi = pd.DataFrame({"Year": all_years})
    df_cpi["CPI"] = df_cpi["Year"].map(cpi_dict)
    
    if df_cpi["CPI"].isna().all():
        df_cpi["CPI"] = [15.0 * (1.068 ** (y - 1980)) for y in all_years]
    else:
        df_cpi["CPI"] = df_cpi["CPI"].interpolate(method="linear").bfill()
        last_valid_idx = df_cpi["CPI"].last_valid_index()
        for idx in range(last_valid_idx + 1, len(df_cpi)):
            df_cpi.loc[idx, "CPI"] = df_cpi.loc[idx - 1, "CPI"] * 1.07
            
    return df_cpi

def build_agent5_rangpur_economics():
    print("=== Building Agent 5: Comprehensive Crop, Vegetable & Fruit Orchard Economics (1980-2026) ===")
    
    if os.path.exists("rangpur_536_unions.csv"):
        df_unions = pd.read_csv("rangpur_536_unions.csv")
    else:
        df_unions = generate_rangpur_536_unions()

    df_cpi = fetch_world_bank_cpi(1980, 2026)
    ref_cpi_2026 = df_cpi.loc[df_cpi["Year"] == 2026, "CPI"].values[0]

    # Comprehensive Catalog of 22 Crops in Rangpur Division across 4 Categories:
    # 1. Fruit_Orchard (ফল ও বাগান ফসল - উঁচু জমির জন্য)
    # 2. Vegetable (সবজি জাতীয় ফসল - ভালো সেচ ও নিষ্কাশন যুক্ত মাঝারি-উঁচু বা চর জমির জন্য)
    # 3. Pulse_Oilseed (ডাল ও তেলবীজ - মাটির স্বাস্থ্য ও নাইট্রোজেন পুনরুদ্ধারের জন্য)
    # 4. Cereal_And_Cash (দানা ও অর্থকরী ফসল)
    rangpur_crops = [
        # --- FRUIT ORCHARDS & HIGH-LAND FRUITS (ফল জাতীয় ফসল) ---
        {"Crop": "Haribhanga_Mango", "Category": "Fruit_Orchard", "Suitable_Land": "High_Land_Vita",
         "Drainage_Need": "Excellent_Well_Drained", "Best_Districts": ["Rangpur", "Thakurgaon", "Dinajpur"],
         "Planting_Months": [6, 7, 8], "Harvest_Months": [6, 7],
         "Water_Need": "Low", "Nitrogen_Effect": "Organic_Canopy_Cover", "Yield_kg_ha": 11500, "Base_Cost_BDT": 180000, "Irrigation_Share": 0.08, "Price_2026_BDT_kg": 65.0, "Demand_Index": 98,
         "Agronomy_Note": "Best for flood-free High Land (Vita/Danga); famous in Mithapukur/Badarganj; huge annual orchard ROI"},
        
        {"Crop": "Dinajpur_Bedana_Litchi", "Category": "Fruit_Orchard", "Suitable_Land": "High_Land_Vita",
         "Drainage_Need": "Excellent_Well_Drained", "Best_Districts": ["Dinajpur", "Rangpur", "Thakurgaon", "Panchagarh"],
         "Planting_Months": [6, 7, 8], "Harvest_Months": [5, 6],
         "Water_Need": "Low", "Nitrogen_Effect": "Organic_Canopy_Cover", "Yield_kg_ha": 7500, "Base_Cost_BDT": 195000, "Irrigation_Share": 0.09, "Price_2026_BDT_kg": 120.0, "Demand_Index": 99,
         "Agronomy_Note": "Premium orchard choice for well-drained High Land loamy soil; zero waterlogging tolerance"},
        
        {"Crop": "Red_Lady_Papaya", "Category": "Fruit_Orchard", "Suitable_Land": "High_Or_Medium_High_Land",
         "Drainage_Need": "Well_Drained_Irrigated", "Best_Districts": ["Rangpur", "Dinajpur", "Nilphamari", "Gaibandha"],
         "Planting_Months": [2, 3, 4, 9, 10], "Harvest_Months": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 35000, "Base_Cost_BDT": 210000, "Irrigation_Share": 0.14, "Price_2026_BDT_kg": 25.0, "Demand_Index": 91,
         "Agronomy_Note": "Year-round high cash flow on high/medium-high land with strict drainage"},
        
        {"Crop": "Sagar_Banana_Kola", "Category": "Fruit_Orchard", "Suitable_Land": "High_Or_Medium_High_Land",
         "Drainage_Need": "Well_Drained_Irrigated", "Best_Districts": ["Gaibandha", "Rangpur", "Dinajpur", "Bogura"],
         "Planting_Months": [1, 2, 9, 10], "Harvest_Months": [8, 9, 10, 11, 12],
         "Water_Need": "Medium", "Nitrogen_Effect": "Organic_Residue_Add", "Yield_kg_ha": 28000, "Base_Cost_BDT": 175000, "Irrigation_Share": 0.15, "Price_2026_BDT_kg": 24.0, "Demand_Index": 92,
         "Agronomy_Note": "Ideal for medium-high land; intercropping with winter vegetables boosts profit"},
        
        {"Crop": "BARI_Malta_Orange", "Category": "Fruit_Orchard", "Suitable_Land": "High_Land_Vita",
         "Drainage_Need": "Excellent_Well_Drained", "Best_Districts": ["Panchagarh", "Thakurgaon", "Dinajpur"],
         "Planting_Months": [5, 6, 7], "Harvest_Months": [9, 10, 11],
         "Water_Need": "Low", "Nitrogen_Effect": "Organic_Canopy_Cover", "Yield_kg_ha": 10000, "Base_Cost_BDT": 165000, "Irrigation_Share": 0.10, "Price_2026_BDT_kg": 80.0, "Demand_Index": 94,
         "Agronomy_Note": "Thrives in slightly acidic, high-elevation well-drained soils of Panchagarh & Thakurgaon"},
        
        {"Crop": "Watermelon_Tormuj", "Category": "Fruit_Orchard", "Suitable_Land": "Char_Alluvial_Land",
         "Drainage_Need": "Sandy_Loam_Well_Drained", "Best_Districts": ["Panchagarh", "Kurigram", "Lalmonirhat", "Thakurgaon"],
         "Planting_Months": [1, 2], "Harvest_Months": [4, 5],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 32000, "Base_Cost_BDT": 140000, "Irrigation_Share": 0.16, "Price_2026_BDT_kg": 18.0, "Demand_Index": 95,
         "Agronomy_Note": "High-profit short-duration fruit for sandy-loam & riverine char lands"},

        # --- VEGETABLES (সবজি জাতীয় ফসল - ভালো সেচ ও নিষ্কাশন যুক্ত জমির জন্য) ---
        {"Crop": "Potato_Alu", "Category": "Vegetable", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Rangpur", "Nilphamari", "Dinajpur", "Thakurgaon", "Lalmonirhat"],
         "Planting_Months": [11, 12], "Harvest_Months": [2, 3],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 24000, "Base_Cost_BDT": 165000, "Irrigation_Share": 0.14, "Price_2026_BDT_kg": 22.0, "Demand_Index": 95,
         "Agronomy_Note": "Premier winter cash vegetable for irrigated sandy-loam/loamy soils"},
        
        {"Crop": "Winter_Summer_Tomato", "Category": "Vegetable", "Suitable_Land": "High_Or_Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Dinajpur", "Rangpur", "Nilphamari", "Kurigram"],
         "Planting_Months": [10, 11, 5, 6], "Harvest_Months": [1, 2, 3, 8, 9],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 28000, "Base_Cost_BDT": 185000, "Irrigation_Share": 0.16, "Price_2026_BDT_kg": 26.0, "Demand_Index": 94,
         "Agronomy_Note": "Very high ROI on well-irrigated, well-drained raised beds"},
        
        {"Crop": "Brinjal_Begun", "Category": "Vegetable", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Rangpur", "Gaibandha", "Kurigram", "Nilphamari"],
         "Planting_Months": [9, 10, 11, 2, 3], "Harvest_Months": [12, 1, 2, 3, 5, 6, 7],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 25000, "Base_Cost_BDT": 150000, "Irrigation_Share": 0.15, "Price_2026_BDT_kg": 28.0, "Demand_Index": 93,
         "Agronomy_Note": "Multi-harvest vegetable ideal for farmers with reliable irrigation & drainage"},
        
        {"Crop": "Cauliflower_Cabbage", "Category": "Vegetable", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Rangpur", "Dinajpur", "Nilphamari", "Thakurgaon"],
         "Planting_Months": [9, 10, 11], "Harvest_Months": [12, 1, 2],
         "Water_Need": "Medium", "Nitrogen_Effect": "Organic_Residue_Add", "Yield_kg_ha": 26000, "Base_Cost_BDT": 145000, "Irrigation_Share": 0.15, "Price_2026_BDT_kg": 20.0, "Demand_Index": 91,
         "Agronomy_Note": "Fast 75-day winter vegetable; leaves field free early for Kharif-1 Mungbean/Maize"},
        
        {"Crop": "Green_Chili_Morich", "Category": "Vegetable", "Suitable_Land": "Char_Or_Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Gaibandha", "Kurigram", "Lalmonirhat", "Rangpur"],
         "Planting_Months": [10, 11, 2, 3], "Harvest_Months": [1, 2, 3, 4, 5, 6],
         "Water_Need": "Low", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 9500, "Base_Cost_BDT": 130000, "Irrigation_Share": 0.12, "Price_2026_BDT_kg": 65.0, "Demand_Index": 97,
         "Agronomy_Note": "High-value spice/vegetable for both irrigated loamy land and sandy char lands"},
        
        {"Crop": "Pointed_Bitter_Gourd", "Category": "Vegetable", "Suitable_Land": "High_Or_Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Rangpur", "Gaibandha", "Dinajpur", "Nilphamari"],
         "Planting_Months": [11, 12, 1, 2], "Harvest_Months": [3, 4, 5, 6, 7, 8],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 18000, "Base_Cost_BDT": 135000, "Irrigation_Share": 0.14, "Price_2026_BDT_kg": 32.0, "Demand_Index": 90,
         "Agronomy_Note": "Potol & Korola on trellis (Macha) give continuous weekly cash income for 6 months"},
        
        {"Crop": "Sweet_Gourd_Pumpkin", "Category": "Vegetable", "Suitable_Land": "Char_Alluvial_Land",
         "Drainage_Need": "Sandy_Loam_Well_Drained", "Best_Districts": ["Kurigram", "Gaibandha", "Lalmonirhat", "Rangpur"],
         "Planting_Months": [10, 11, 12], "Harvest_Months": [2, 3, 4, 5],
         "Water_Need": "Low", "Nitrogen_Effect": "Restorative_Cover", "Yield_kg_ha": 22000, "Base_Cost_BDT": 75000, "Irrigation_Share": 0.08, "Price_2026_BDT_kg": 16.0, "Demand_Index": 88,
         "Agronomy_Note": "Champion sandbar (Char) crop in Teesta/Brahmaputra basins; minimal water & fertilizer cost"},

        # --- PULSES & OILSEEDS (ডাল ও তেলবীজ - মাটির নাইট্রোজেন ও স্বাস্থ্য রক্ষাকারী) ---
        {"Crop": "Mustard_Sorisha", "Category": "Pulse_Oilseed", "Suitable_Land": "Medium_High_Or_Low_Land",
         "Drainage_Need": "Moderate_Seasonal", "Best_Districts": ["Dinajpur", "Rangpur", "Kurigram", "Gaibandha", "Thakurgaon"],
         "Planting_Months": [10, 11], "Harvest_Months": [1, 2],
         "Water_Need": "Low", "Nitrogen_Effect": "Restorative", "Yield_kg_ha": 1650, "Base_Cost_BDT": 42000, "Irrigation_Share": 0.07, "Price_2026_BDT_kg": 90.0, "Demand_Index": 92,
         "Agronomy_Note": "75-85 day low-water oilseed; fits neatly between Aman Rice and Boro/Mungbean"},
        
        {"Crop": "Lentil_Mosur", "Category": "Pulse_Oilseed", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Moderate_Seasonal", "Best_Districts": ["Rangpur", "Dinajpur", "Thakurgaon", "Panchagarh", "Nilphamari"],
         "Planting_Months": [10, 11], "Harvest_Months": [2, 3],
         "Water_Need": "Low", "Nitrogen_Effect": "High_Nitrogen_Fixing", "Yield_kg_ha": 1400, "Base_Cost_BDT": 38000, "Irrigation_Share": 0.05, "Price_2026_BDT_kg": 115.0, "Demand_Index": 93,
         "Agronomy_Note": "Fixes atmospheric nitrogen (40-60 kg N/ha) and saves 75% irrigation water vs Boro rice"},
        
        {"Crop": "Mungbean_Mug", "Category": "Pulse_Oilseed", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Moderate_Seasonal", "Best_Districts": ["Rangpur", "Dinajpur", "Thakurgaon", "Kurigram"],
         "Planting_Months": [2, 3], "Harvest_Months": [5, 6],
         "Water_Need": "Low", "Nitrogen_Effect": "High_Nitrogen_Fixing", "Yield_kg_ha": 1250, "Base_Cost_BDT": 36000, "Irrigation_Share": 0.06, "Price_2026_BDT_kg": 105.0, "Demand_Index": 89,
         "Agronomy_Note": "Short-duration Kharif-1 legume; green biomass enriches soil organic matter before Aman"},

        # --- CEREALS & CASH CROPS (দানা ও অর্থকরী ফসল) ---
        {"Crop": "Boro_Rice", "Category": "Cereal_Grain", "Suitable_Land": "Medium_Low_Land",
         "Drainage_Need": "Flooded_Paddy_Retaining", "Best_Districts": ["Rangpur", "Dinajpur", "Nilphamari", "Gaibandha", "Kurigram"],
         "Planting_Months": [12, 1, 2], "Harvest_Months": [4, 5],
         "Water_Need": "High", "Nitrogen_Effect": "Depleting", "Yield_kg_ha": 4800, "Base_Cost_BDT": 92000, "Irrigation_Share": 0.36, "Price_2026_BDT_kg": 34.0, "Demand_Index": 95,
         "Agronomy_Note": "High water demand (3000+ liters/kg); unsuitable for dry High Land or low-moisture zones"},
        
        {"Crop": "Aman_Rice", "Category": "Cereal_Grain", "Suitable_Land": "Medium_Low_Land",
         "Drainage_Need": "Flooded_Paddy_Retaining", "Best_Districts": ["Dinajpur", "Rangpur", "Naogaon", "Kurigram", "Gaibandha"],
         "Planting_Months": [7, 8], "Harvest_Months": [11, 12],
         "Water_Need": "Medium", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 3700, "Base_Cost_BDT": 64000, "Irrigation_Share": 0.09, "Price_2026_BDT_kg": 36.0, "Demand_Index": 94,
         "Agronomy_Note": "Rain-fed monsoon staple crop; low irrigation cost"},
        
        {"Crop": "Maize_Bhutta", "Category": "Cereal_Grain", "Suitable_Land": "Medium_High_Or_Char_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Lalmonirhat", "Dinajpur", "Thakurgaon", "Nilphamari", "Kurigram"],
         "Planting_Months": [11, 12, 1], "Harvest_Months": [4, 5],
         "Water_Need": "Medium", "Nitrogen_Effect": "Moderate_Depleting", "Yield_kg_ha": 8800, "Base_Cost_BDT": 96000, "Irrigation_Share": 0.16, "Price_2026_BDT_kg": 28.0, "Demand_Index": 92,
         "Agronomy_Note": "High-yielding feed grain; profitable alternative to Boro rice & Tobacco in northern chars"},
        
        {"Crop": "Wheat_Gom", "Category": "Cereal_Grain", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Moderate_Seasonal", "Best_Districts": ["Thakurgaon", "Dinajpur", "Panchagarh", "Rangpur"],
         "Planting_Months": [11, 12], "Harvest_Months": [3, 4],
         "Water_Need": "Low", "Nitrogen_Effect": "Neutral", "Yield_kg_ha": 3500, "Base_Cost_BDT": 58000, "Irrigation_Share": 0.12, "Price_2026_BDT_kg": 42.0, "Demand_Index": 87,
         "Agronomy_Note": "Requires only 2-3 light irrigations in cool northern winters"},
        
        {"Crop": "Jute_Paat", "Category": "Cash_Crop", "Suitable_Land": "Medium_Low_Or_Char_Land",
         "Drainage_Need": "Moderate_Seasonal", "Best_Districts": ["Kurigram", "Gaibandha", "Lalmonirhat", "Rangpur", "Nilphamari"],
         "Planting_Months": [3, 4], "Harvest_Months": [7, 8],
         "Water_Need": "High", "Nitrogen_Effect": "Organic_Leaf_Drop_Add", "Yield_kg_ha": 2650, "Base_Cost_BDT": 72000, "Irrigation_Share": 0.08, "Price_2026_BDT_kg": 64.0, "Demand_Index": 84,
         "Agronomy_Note": "Deep roots break hardpan and shed leaves enrich soil prior to Aman rice"},
        
        {"Crop": "Tobacco_Tamak", "Category": "Cash_Crop", "Suitable_Land": "Medium_High_Land",
         "Drainage_Need": "Good_Irrigated_Vegetable_Bed", "Best_Districts": ["Lalmonirhat", "Nilphamari", "Rangpur"],
         "Planting_Months": [10, 11, 12], "Harvest_Months": [3, 4],
         "Water_Need": "Medium", "Nitrogen_Effect": "Severe_Depletion", "Yield_kg_ha": 2200, "Base_Cost_BDT": 115000, "Irrigation_Share": 0.22, "Price_2026_BDT_kg": 145.0, "Demand_Index": 72,
         "Agronomy_Note": "WARNING: Severely depletes soil fertility & organic matter; replace with Maize/Vegetables/Potato"}
    ]

    print("Generating 1980-2026 monthly economics across all 22 crops (Grains, Pulses, Vegetables, Fruits)...")
    np.random.seed(2026)
    records = []
    districts = df_unions["District"].unique()

    for year in range(1980, 2027):
        cpi_val = df_cpi.loc[df_cpi["Year"] == year, "CPI"].values[0]
        inf_factor = cpi_val / ref_cpi_2026
        
        for month in range(1, 13):
            season_name = get_bangladesh_season(month)
            
            for dist in districts:
                for c in rangpur_crops:
                    # Regional comparative advantage: higher yield & price realization in specialization districts
                    is_specialty_dist = dist in c["Best_Districts"]
                    regional_yield_boost = 1.08 if is_specialty_dist else 0.96
                    regional_price_mod = 1.04 if is_specialty_dist else 0.98

                    # Seasonal price dynamics
                    if month in c["Harvest_Months"]:
                        seasonal_price_mod = 0.92
                        activity_status = "Peak_Harvest_Market_Supply"
                    elif month in c["Planting_Months"]:
                        seasonal_price_mod = 1.08
                        activity_status = "Active_Planting_Window"
                    else:
                        seasonal_price_mod = 1.03
                        activity_status = "Growing_Or_Off_Season"

                    noise = np.random.uniform(0.96, 1.04)
                    market_price = round(c["Price_2026_BDT_kg"] * inf_factor * seasonal_price_mod * regional_price_mod * noise, 2)
                    
                    prod_cost = round(c["Base_Cost_BDT"] * inf_factor * np.random.uniform(0.97, 1.03), 2)
                    irrigation_cost = round(prod_cost * c["Irrigation_Share"], 2)
                    expected_yield = round(c["Yield_kg_ha"] * regional_yield_boost * np.random.uniform(0.94, 1.06), 1)
                    
                    revenue = round(expected_yield * market_price, 2)
                    net_profit = round(revenue - prod_cost, 2)
                    profit_margin_pct = round((net_profit / max(prod_cost, 1)) * 100, 2)

                    records.append({
                        "Division": "Rangpur",
                        "District": dist,
                        "Year": year,
                        "Month": month,
                        "Season": season_name,
                        "Crop": c["Crop"],
                        "Crop_Category": c["Category"],
                        "Suitable_Land_Elevation": c["Suitable_Land"],
                        "Required_Drainage_System": c["Drainage_Need"],
                        "District_Suitability_Rank": "Top_Recommended_Zone" if is_specialty_dist else "Standard_Zone",
                        "Crop_Activity_Status": activity_status,
                        "Water_Requirement": c["Water_Need"],
                        "Soil_Nitrogen_Impact": c["Nitrogen_Effect"],
                        "Market_Price_BDT_per_kg": market_price,
                        "Expected_Yield_kg_per_ha": expected_yield,
                        "Irrigation_Cost_BDT_per_ha": irrigation_cost,
                        "Total_Production_Cost_BDT_per_ha": prod_cost,
                        "Gross_Revenue_BDT_per_ha": revenue,
                        "Net_Profit_BDT_per_ha": net_profit,
                        "Profit_Margin_Percent": profit_margin_pct,
                        "Market_Demand_Index": c["Demand_Index"],
                        "Agronomy_Recommendation_Note": c["Agronomy_Note"],
                        "Data_Source": "WorldBank_CPI_DAE_DAM_Horticulture_Sim"
                    })

    df_agent5 = pd.DataFrame(records)
    df_agent5 = df_agent5.dropna().sort_values(by=["District", "Year", "Month", "Crop_Category", "Crop"]).reset_index(drop=True)
    
    output_csv = "agent5_crop_economics_1980_2026.csv"
    df_agent5.to_csv(output_csv, index=False)
    print(f"Success! Saved {len(df_agent5):,} rows across 22 crops to '{output_csv}'.")
    
    # Preview January 2026 across all 4 categories in Rangpur District
    jan_2026 = df_agent5[(df_agent5["District"] == "Rangpur") & (df_agent5["Year"] == 2026) & (df_agent5["Month"] == 1)]
    print("\n--- Preview: Rangpur District (January 2026) Across Fruits, Vegetables, Pulses & Grains ---")
    preview_cols = ["Crop", "Crop_Category", "Suitable_Land_Elevation", "Market_Price_BDT_per_kg", "Net_Profit_BDT_per_ha", "Profit_Margin_Percent"]
    print(jan_2026[preview_cols].to_string(index=False))

if __name__ == "__main__":
    build_agent5_rangpur_economics()