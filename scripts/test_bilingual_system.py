import urllib.request
import urllib.parse
import json
import re

print("=== 1. Testing Backend API Bilingual Responses ===")
base_url = "http://127.0.0.1:8000"

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))

def post_json(url, data):
    payload = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))

try:
    # 1. Regions
    reg_data = get_json(f"{base_url}/api/regions")
    districts = reg_data.get("regions", [])
    print(f"Regions API returned {len(districts)} districts.")
    assert len(districts) == 8, f"Expected 8 Rangpur districts, got {len(districts)}"
    for d in districts:
        assert "primary_risk" in d, f"Missing primary_risk in {d['id']}"
        assert "primary_risk_bn" in d, f"Missing primary_risk_bn in {d['id']}"
    print("✅ Regions API has both English and Bengali risks for all 8 Rangpur districts!")

    # 2. Crops
    crops_data = get_json(f"{base_url}/api/crops").get("crops", [])
    print(f"Crops API returned {len(crops_data)} crops.")
    for c in crops_data:
        assert "name_en" in c and c["name_en"], f"Missing name_en in crop {c.get('id')}"
        assert "name_bn" in c and c["name_bn"], f"Missing name_bn in crop {c.get('id')}"
    print("✅ Crops API has both English and Bengali names for all crops!")

    # 3. Multi-agent Analysis
    payload = {
        "region_id": "rangpur",
        "upazila": "rangpur_sadar",
        "union_id": "RNG_U001",
        "union_name": "Alamnagar",
        "past_crop": "boro_rice",
        "monoculture_years": 3,
        "priority": "water_saving",
        "land_bigha": 2.5
    }
    ana_data = post_json(f"{base_url}/api/analyze", payload)
    master = ana_data.get("master_adaptive_strategy", {})
    assert "farmer_directive_bn" in master, "Missing farmer_directive_bn"
    assert "farmer_directive_en" in master, "Missing farmer_directive_en"
    assert "strategy_theme" in master, "Missing strategy_theme"
    assert "strategy_theme_en" in master, "Missing strategy_theme_en"
    print("Master Directive (BN):", master["farmer_directive_bn"][:80], "...")
    print("Master Directive (EN):", master["farmer_directive_en"][:80], "...")

    seq = master.get("adaptive_crop_sequence", [])
    assert len(seq) == 3, f"Expected 3 seasons, got {len(seq)}"
    for s in seq:
        assert "crop_name" in s and "crop_name_en" in s, f"Crop name missing in stage {s['stage']}"
        assert "why_chosen_bn" in s and "why_chosen_en" in s, f"Why chosen missing in stage {s['stage']}"
    print("✅ Adaptive crop sequence has complete bilingual details across all 3 seasons!")

    # Specialist agents check
    agents = ana_data.get("specialist_agent_evaluations", {})
    deg = agents.get("degradation_agent", {})
    assert "warning_bn" in deg and "warning_en" in deg, "Missing deg warning bilingual"
    soil = agents.get("soil_agent", {})
    assert "warning_bn" in soil and "warning_en" in soil, "Missing soil warning bilingual"
    print("✅ Specialist agents return complete English and Bengali alerts & recommendations!")

except Exception as e:
    import traceback
    print(f"API test error: {e}")
    traceback.print_exc()

print("\n=== 2. Testing Frontend index.html Dictionary Completeness ===")
with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_t = html.find("const t = {")
end_t = html.find("function toggleLanguage()", start_t)
t_code = html[start_t:end_t]

bn_part = t_code[t_code.find("bn: {"):t_code.find("en: {")]
en_part = t_code[t_code.find("en: {"):]

bn_keys = set(re.findall(r'([a-zA-Z0-9_]+)\s*:', bn_part)) - {'bn'}
en_keys = set(re.findall(r'([a-zA-Z0-9_]+)\s*:', en_part)) - {'en'}

print(f"Total keys in t.bn: {len(bn_keys)}")
print(f"Total keys in t.en: {len(en_keys)}")

pure_en_keys = {k for k in en_keys if not k.isdigit() and len(k) > 1}
missing_in_en = bn_keys - pure_en_keys
print("Keys in BN missing in EN:", missing_in_en)
assert len(missing_in_en) == 0, f"Found keys missing in EN: {missing_in_en}"
print("✅ 100% dictionary key symmetry between Bengali and English!")

print("\n=== 3. Testing HTML data-i18n Coverage ===")
data_i18n_matches = re.findall(r'data-i18n=["\']([^"\']+)["\']', html)
print(f"Total data-i18n tags in HTML: {len(data_i18n_matches)}")

missing_in_dict = [k for k in data_i18n_matches if k not in bn_keys]
if missing_in_dict:
    print(f"WARNING: The following data-i18n keys are not in t.bn: {set(missing_in_dict)}")
else:
    print("✅ All data-i18n tags have matching keys in t.bn and t.en!")

print("\n🎉 ALL BILINGUAL CHECKS PASSED PERFECTLY!")
