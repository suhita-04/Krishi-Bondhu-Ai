import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"
ROOT_FILE = BASE_DIR / "index.html"

with open(FRONTEND_FILE, "r", encoding="utf-8") as f:
    c = f.read().replace("\r\n", "\n")

target1 = """  // Populate Upazilas and Unions for this district
  const upzKey = populateUpazilaDropdowns(distId, targetUpzKey);
  const unionObj = populateUnionDropdowns(distId, upzKey, targetUnionId);

  if (unionObj) {"""

replacement1 = """  // Populate Upazilas and Unions for this district
  const upzKey = populateUpazilaDropdowns(distId, targetUpzKey);
  const unionObj = populateUnionDropdowns(distId, upzKey, targetUnionId);

  if (typeof renderLocationSpecificMapNodes === 'function') {
    renderLocationSpecificMapNodes();
  }

  if (unionObj) {"""

if target1 in c:
    c = c.replace(target1, replacement1, 1)
    print("✓ Added renderLocationSpecificMapNodes in syncDistrictSelectors")
else:
    print("⚠ target1 not found")

target2 = """function handleUpazilaChange(upzKey) {
  currentSelectedUpazilaKey = upzKey;
  ['heroUpazilaSelect', 'recUpazilaSelect', 'mapUpazilaSelect'].forEach(selId => {
    const el = document.getElementById(selId);
    if (el) el.value = upzKey;
  });
  const unionObj = populateUnionDropdowns(currentSelectedDistId, upzKey);
  if (unionObj) {
    updateAllUnionBadges(unionObj);
    if (typeof window.centerMapOnSelectedUnion === 'function') {
      window.centerMapOnSelectedUnion(unionObj);
    }
  }
  loadLiveBackendAnalysis(currentSelectedDistId);
}"""

replacement2 = """function handleUpazilaChange(upzKey) {
  currentSelectedUpazilaKey = upzKey;
  ['heroUpazilaSelect', 'recUpazilaSelect', 'mapUpazilaSelect'].forEach(selId => {
    const el = document.getElementById(selId);
    if (el) el.value = upzKey;
  });
  const unionObj = populateUnionDropdowns(currentSelectedDistId, upzKey);
  if (typeof renderLocationSpecificMapNodes === 'function') {
    renderLocationSpecificMapNodes();
  }
  if (unionObj) {
    updateAllUnionBadges(unionObj);
    if (typeof window.centerMapOnSelectedUnion === 'function') {
      window.centerMapOnSelectedUnion(unionObj);
    }
  }
  loadLiveBackendAnalysis(currentSelectedDistId);
}"""

if target2 in c:
    c = c.replace(target2, replacement2, 1)
    print("✓ Added renderLocationSpecificMapNodes in handleUpazilaChange")
else:
    print("⚠ target2 not found")

target3 = """function handleUnionChange(unionId) {
  currentSelectedUnionId = unionId;
  ['heroUnionSelect', 'recUnionSelect', 'mapUnionSelect'].forEach(selId => {
    const el = document.getElementById(selId);
    if (el) el.value = unionId;
  });
  const unionObj = getHierarchyUnion(currentSelectedDistId, currentSelectedUpazilaKey, unionId);
  if (unionObj) {
    currentUnionObj = unionObj;
    currentSelectedUnionName = unionObj.name_en;
    updateAllUnionBadges(unionObj);
    if (typeof window.centerMapOnSelectedUnion === 'function') {
      window.centerMapOnSelectedUnion(unionObj);
    }
  }
  loadLiveBackendAnalysis(currentSelectedDistId);
}"""

replacement3 = """function handleUnionChange(unionId) {
  currentSelectedUnionId = unionId;
  ['heroUnionSelect', 'recUnionSelect', 'mapUnionSelect'].forEach(selId => {
    const el = document.getElementById(selId);
    if (el) el.value = unionId;
  });
  const unionObj = getHierarchyUnion(currentSelectedDistId, currentSelectedUpazilaKey, unionId);
  if (unionObj) {
    currentUnionObj = unionObj;
    currentSelectedUnionName = unionObj.name_en;
    updateAllUnionBadges(unionObj);
    if (typeof window.centerMapOnSelectedUnion === 'function') {
      window.centerMapOnSelectedUnion(unionObj);
    }
    if (typeof window.updateDistrictInspectorFromLive === 'function') {
      window.updateDistrictInspectorFromLive(window.liveAnalysisData || { district_profile: {} });
    }
    // Re-style union circles to highlight selected union
    if (window.unionMapCircles) {
      Object.entries(window.unionMapCircles).forEach(([uId, circ]) => {
        const isSel = (uId === unionId);
        circ.setStyle({
          radius: isSel ? 1800 : 1300,
          color: isSel ? '#FFFFFF' : getUnionConditionColor(unionObj, activeMapLayer),
          weight: isSel ? 4 : 1.2,
          fillOpacity: isSel ? 0.90 : 0.45
        });
      });
    }
  }
  loadLiveBackendAnalysis(currentSelectedDistId);
}"""

if target3 in c:
    c = c.replace(target3, replacement3, 1)
    print("✓ Added circle re-styling and inspector refresh in handleUnionChange")
else:
    print("⚠ target3 not found")

with open(FRONTEND_FILE, "w", encoding="utf-8") as f:
    f.write(c)
print(f"✓ Saved {FRONTEND_FILE}")

shutil.copyfile(FRONTEND_FILE, ROOT_FILE)
print(f"✓ Mirrored to root {ROOT_FILE}")

