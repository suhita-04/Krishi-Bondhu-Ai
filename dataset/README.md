# কৃষি BONDHU AI — Longitudinal Agro-Climatic & Economic Datasets (1980–2026)

This directory hosts the empirical telemetry datasets synthesized and validated for **কৃষি BONDHU AI**, developed by **Team Nokkhotro** for the **NASA Space Apps Challenge 2026** ("Field Shift: Adapting Farms with NASA Data").

The repository contains **1,913,624 multi-spectral, agro-climatic, and socio-economic records** spanning **47 consecutive years (1980–2026)** across all **536 administrative unions** in the 8 districts of Rangpur Division, Bangladesh.

---

## 📁 Dataset Inventory

| File Name | Size | Records | Temporal Scope | Primary Data Sources & Metrics |
| :--- | :---: | :---: | :---: | :--- |
| [`rangpur_536_unions.csv`](./data/rangpur_536_unions.csv) | 0.14 MB | 536 | Baseline | Administrative hierarchy (Division, District, Upazila, Union), Centroid Coordinates (Lat, Lon), Elevation (m), Land Elevation Type (Vita, Medium, Low, Char), River Basin, Soil Texture, Drainage Classification. |
| [`agent1_precipitation_1980_2026.csv`](./data/agent1_precipitation_1980_2026.csv) | 88.3 MB | 302,304 | 1980–2026 | **NASA GPM IMERG & MERRA-2**: Corrected precipitation (`PRECTOTCORR`), localized rainfall (mm/month), river basin flood factor, active waterlogging days, orchard and high-value vegetable flood safety flags. |
| [`agent2_Soil_Moisture_Rainfall_Temperature_536_Unions_Monthly_1981-2026.csv`](./data/agent2_Soil_Moisture_Rainfall_Temperature_536_Unions_Monthly_1981-2026.csv) | 24.4 MB | 295,872 | 1981–2026 | **NASA POWER (MERRA-2)**: Mean temperature at 2m (`T2M`), Maximum temperature (`T2M_MAX`), Minimum temperature (`T2M_MIN`), Relative humidity at 2m (`RH2M`), Kharif/Rabi seasonal heat stress. |
| [`agent3_soil_moisture_1980_2026.csv`](./data/agent3_soil_moisture_1980_2026.csv) | 74.4 MB | 302,304 | 1980–2026 | **NASA POWER (CERES / MERRA-2)**: All-sky surface shortwave downward irradiance (`ALLSKY_SFC_SW_DWN` in $MJ/m^2/day$), photosynthetic radiation indices, solar pump feasibility, thermal evapotranspiration. |
| [`agent4_agronomy_solar_1980_2026.csv`](./data/agent4_agronomy_solar_1980_2026.csv) | 65.5 MB | 302,304 | 1980–2026 | **NASA SMAP & MERRA-2**: Surface topsoil wetness (`GWETTOP`), Root-zone soil wetness (`GWETROOT`), soil water deficit, drought vulnerability index, AWD (Alternate Wetting & Drying) trigger flags. |
| [`agent5_crop_economics_1980_2026.csv`](./data/agent5_crop_economics_1980_2026.csv) | 33.8 MB | 302,304 | 1980–2026 | **World Bank & BBS / DAM**: Consumer Price Index (`FP.CPI.TOTL`), real inflation-adjusted crop market prices (BDT/kg), per-bigha input costs (irrigation fuel, fertilizer, labor), net profit margins for 10 regional crops. |
| [`agent6_Atmospheric_Conditions_536_Unions_Monthly_1981-2026.csv`](./data/agent6_Atmospheric_Conditions_536_Unions_Monthly_1981-2026.csv) | 24.7 MB | 295,872 | 1981–2026 | **NASA POWER (MERRA-2)**: Wind speed at 2m (`WS2M`), surface atmospheric pressure (`PS`), aerodynamic resistance, crop lodging risk ratings, high-wind stalk break danger warnings. |

---

## 🛠️ Data Reproduction Code

All datasets can be audited, verified, and re-generated programmatically using the self-contained Python scripts in the [`code/`](./code) subdirectory:

- [`code/setup_rangpur_unions.py`](./code/setup_rangpur_unions.py): Generates GIS coordinates, elevation profiles, and agro-ecological zones.
- [`code/agent1.py`](./code/agent1.py): Pulls NASA GPM/MERRA-2 precipitation and computes hydro-drainage metrics.
- [`code/agent2.py`](./code/agent2.py): Pulls NASA thermal and relative humidity parameters.
- [`code/agent3.py`](./code/agent3.py): Ingests solar irradiance and derives photo-thermal indices.
- [`code/agent4.py`](./code/agent4.py): Fuses SMAP L4 soil moisture with agricultural water management logic.
- [`code/agent5.py`](./code/agent5.py): Ingests World Bank CPI indicators and simulates crop profit dynamics.
- [`code/agent6.py`](./code/agent6.py): Synthesizes wind shear, surface pressure, and lodging vulnerability.

---

## 📖 In-Depth Telemetry Documentation

For complete mathematical definitions, ground validation error metrics ($RMSE$, $MAE$, $R^2$), sensor lineage, and fusion pipelines, consult:
- **[Comprehensive Data Validation & Telemetry Guide](../data_validation_and_dataset_uses.md)**

---

## ⚖️ Restricted License & Usage Terms

These datasets are proprietary research outputs created for the **কৃষি BONDHU AI** platform by **Team Nokkhotro**. 
- **Academic & Judge Evaluation**: Freely accessible for review and evaluation within the scope of competition judging.
- **Third-Party & Commercial Use**: **Restricted**. Any external reuse, redistribution, modification, retraining, or integration into external products requires explicit written authorization from the authors. See [LICENSE](../LICENSE) for full legal terms.
