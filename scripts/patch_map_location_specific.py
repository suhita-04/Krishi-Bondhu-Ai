"""
Patch map in frontend/index.html to render location-specific data for every Upazila and Union.
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"
ROOT_FILE = BASE_DIR / "index.html"

with open(FRONTEND_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Map header to include Map Scope toggle (আমার জেলা/উপজেলা vs সকল ৫৩৬ ইউনিয়ন)
old_map_header = """                  <button type="button" id="mapStyleToggleBtn" onclick="toggleBaseMapStyle()"
                    class="px-2.5 py-1 rounded-xl bg-leaf-50 dark:bg-earth-800 hover:bg-leaf-100 dark:hover:bg-earth-700 text-leaf-700 dark:text-leaf-300 text-[11px] font-black border border-leaf-500/30 flex items-center gap-1">
                    <i class="fa-solid fa-satellite"></i> <span id="mapStyleToggleLbl">স্যাটেলাইট ভিউ</span>
                  </button>
                  <div
                    class="flex items-center gap-2 text-[11px] font-mono font-bold text-leaf-700 dark:text-leaf-300 bg-earth-50 dark:bg-earth-800 px-2.5 py-1 rounded-xl shrink-0">
                    <span>রংপুর বিভাগ ৫৩৬ ইউনিয়ন লাইভ</span>
                    <span>|</span>
                    <span id="zoomLevelDisplay">১০x</span>
                  </div>"""

new_map_header = """                  <button type="button" id="mapScopeToggleBtn" onclick="toggleMapScope()"
                    class="px-2.5 py-1 rounded-xl bg-leaf-100 dark:bg-leaf-950 hover:bg-leaf-200 dark:hover:bg-leaf-900 text-leaf-800 dark:text-leaf-300 text-[11px] font-black border border-leaf-500/40 flex items-center gap-1 transition shadow-sm" title="ম্যাপের পরিধি পরিবর্তন করুন">
                    <i class="fa-solid fa-layer-group text-leaf-500"></i> <span id="mapScopeToggleLbl">📍 জেলার ইউনিয়নসমূহ</span>
                  </button>
                  <button type="button" id="mapStyleToggleBtn" onclick="toggleBaseMapStyle()"
                    class="px-2.5 py-1 rounded-xl bg-leaf-50 dark:bg-earth-800 hover:bg-leaf-100 dark:hover:bg-earth-700 text-leaf-700 dark:text-leaf-300 text-[11px] font-black border border-leaf-500/30 flex items-center gap-1">
                    <i class="fa-solid fa-satellite"></i> <span id="mapStyleToggleLbl">স্যাটেলাইট ভিউ</span>
                  </button>
                  <div
                    class="flex items-center gap-2 text-[11px] font-mono font-bold text-leaf-700 dark:text-leaf-300 bg-earth-50 dark:bg-earth-800 px-2.5 py-1 rounded-xl shrink-0">
                    <span id="mapNodesCountLbl">৫৩৬ ইউনিয়ন সংযুক্ত</span>
                    <span>|</span>
                    <span id="zoomLevelDisplay">১০x</span>
                  </div>"""

if old_map_header in content:
    content = content.replace(old_map_header, new_map_header, 1)
    print("✓ Patched Map Header Controls")
else:
    normalized_c = content.replace("\r\n", "\n")
    if old_map_header in normalized_c:
        content = normalized_c.replace(old_map_header, new_map_header, 1)
        print("✓ Patched Map Header Controls (CRLF normalized)")
    else:
        print("⚠ old_map_header not found")

# 2. Replace map rendering and inspector logic with Upazila & Union specific engine
old_map_logic_start = "window.initOrRefreshRegionalMap = function() {"
old_map_logic_end = "/* =========================================================\n   DYNAMIC 7-DAY IRRIGATION SCHEDULE & ALERT BANNER\n   ========================================================= */"

new_map_logic = """window.unionMapCircles = {};
window.upazilaMapMarkers = {};
window.districtMapCircles = {};
window.mapScope = 'district'; // 'district' or 'all'

function toggleMapScope() {
  window.mapScope = (window.mapScope === 'district') ? 'all' : 'district';
  const btnLbl = document.getElementById('mapScopeToggleLbl');
  const countLbl = document.getElementById('mapNodesCountLbl');
  if (btnLbl) {
    btnLbl.textContent = (window.mapScope === 'district') ? '📍 জেলার ইউনিয়নসমূহ' : '🌐 সকল ৫৩৬ ইউনিয়ন';
  }
  if (countLbl) {
    countLbl.textContent = (window.mapScope === 'district') ? 'জেলার ইউনিয়ন ভিউ' : 'রংপুর ৫৩৬ ইউনিয়ন ভিউ';
  }
  renderLocationSpecificMapNodes();
}

function getUnionConditionColor(u, layer) {
  if (!u || !u.telemetry) return '#10B981';
  if (layer === 'smap') return u.telemetry.smap_color;
  if (layer === 'ndvi') return u.telemetry.ndvi_color;
  if (layer === 'ecostress') return u.telemetry.lst_color;
  if (layer === 'gpm') return u.telemetry.flood_color;
  return '#10B981';
}

function getUnionConditionLabel(u, layer) {
  if (!u || !u.telemetry) return 'স্বাভাবিক অবস্থা';
  if (layer === 'smap') return `মাটির রস: ${u.telemetry.smap_label}`;
  if (layer === 'ndvi') return `সবুজ স্বাস্থ্য: ${u.telemetry.ndvi_label}`;
  if (layer === 'ecostress') return `রোদের তাপ: ${u.telemetry.lst_label}`;
  if (layer === 'gpm') return `প্লাবন/বৃষ্টি: ${u.telemetry.flood_label}`;
  return 'স্বাভাবিক';
}

function updateMapLayerLegend(layer) {
  const titleEl = document.getElementById('mapLegendTitle');
  const barEl = document.getElementById('mapLegendBar');
  const labelsEl = document.getElementById('mapLegendLabels');
  if (!titleEl || !barEl || !labelsEl) return;

  if (layer === 'smap') {
    titleEl.textContent = 'মাটির রস নির্দেশক স্কেল (SMAP L4)';
    barEl.className = 'w-full h-3 rounded-full bg-gradient-to-r from-red-500 via-amber-500 to-emerald-500 mb-1';
    labelsEl.innerHTML = '<span class="text-rose-600 font-bold">শুকনো (<১৮%)</span><span class="text-amber-600 font-bold">মাঝারি রস</span><span class="text-emerald-600 font-bold">পর্যাপ্ত রস (>২৪%)</span>';
  } else if (layer === 'ndvi') {
    titleEl.textContent = 'ফসলের সবুজ স্বাস্থ্য স্কেল (Landsat/NDVI)';
    barEl.className = 'w-full h-3 rounded-full bg-gradient-to-r from-amber-500 via-lime-500 to-emerald-700 mb-1';
    labelsEl.innerHTML = '<span class="text-amber-600 font-bold">হালকা/চাপযুক্ত</span><span class="text-lime-600 font-bold">স্বাভাবিক</span><span class="text-emerald-700 font-bold">গাঢ় সতেজ (>০.৫৮)</span>';
  } else if (layer === 'ecostress') {
    titleEl.textContent = 'পৃষ্ঠ তাপমাত্রা ও তাপীয় চাপ (ECOSTRESS LST)';
    barEl.className = 'w-full h-3 rounded-full bg-gradient-to-r from-emerald-500 via-amber-500 to-rose-600 mb-1';
    labelsEl.innerHTML = '<span class="text-emerald-600 font-bold">অনুকূল (<৩২°C)</span><span class="text-amber-600 font-bold">উষ্ণ (৩৪°C)</span><span class="text-rose-600 font-bold">তীব্র তাপদাহ (>৩৬°C)</span>';
  } else if (layer === 'gpm') {
    titleEl.textContent = 'বৃষ্টিপাত ও প্লাবন ঝুঁকি স্কেল (NASA GPM IMERG)';
    barEl.className = 'w-full h-3 rounded-full bg-gradient-to-r from-orange-500 via-emerald-500 via-sky-400 to-blue-700 mb-1';
    labelsEl.innerHTML = '<span class="text-orange-600 font-bold">অনাবৃষ্টি</span><span class="text-emerald-600 font-bold">স্বাভাবিক</span><span class="text-sky-500 font-bold">মাঝারি</span><span class="text-blue-700 font-bold">উচ্চ প্লাবন</span>';
  }
}

window.initOrRefreshRegionalMap = function() {
  const mapEl = document.getElementById('bangladeshLeafletMap');
  if (!mapEl) return;
  if (typeof L === 'undefined') {
    mapEl.innerHTML = '<div class="w-full h-full flex items-center justify-center text-xs font-bold text-slate-300 p-4 text-center">ইন্টারনেট সংযোগ না থাকায় অফলাইন মোড সক্রিয় রয়েছে।</div>';
    return;
  }

  if (!window.leafletMap) {
    const startDist = bdDistricts.find(d => d.id === currentSelectedDistId) || { lat: 25.7439, lon: 89.2752 };
    window.leafletMap = L.map('bangladeshLeafletMap', {
      center: [startDist.lat, startDist.lon],
      zoom: 10,
      zoomControl: false,
      dragging: true,
      touchZoom: true,
      scrollWheelZoom: true
    });

    streetTileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap'
    });
    satTileLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 18,
      attribution: '&copy; Esri Satellite'
    });
    streetTileLayer.addTo(window.leafletMap);

    window.leafletMap.on('zoomend', () => {
      const zEl = document.getElementById('zoomLevelDisplay');
      if (zEl && window.leafletMap) zEl.textContent = `${window.leafletMap.getZoom()}x`;
    });
  }

  renderLocationSpecificMapNodes();
};

function renderLocationSpecificMapNodes() {
  if (!window.leafletMap) return;
  const h = getRangpurHierarchy();
  if (!h || !h.districts) return;

  // Clear existing union circles, upazila markers and district boundaries
  Object.values(window.unionMapCircles).forEach(c => c.remove());
  window.unionMapCircles = {};

  Object.values(window.upazilaMapMarkers).forEach(m => m.remove());
  window.upazilaMapMarkers = {};

  Object.values(window.districtMapCircles).forEach(c => c.remove());
  window.districtMapCircles = {};

  const activeDist = h.districts[currentSelectedDistId];
  if (!activeDist) return;

  // Render district boundary ring
  const distCircle = L.circle([activeDist.lat, activeDist.lon], {
    radius: 32000,
    color: '#10B981',
    weight: 2,
    dashArray: '5, 8',
    fillColor: '#10B981',
    fillOpacity: 0.03,
    interactive: false
  }).addTo(window.leafletMap);
  window.districtMapCircles[activeDist.id] = distCircle;

  // Choose districts to render based on scope toggle
  const districtsToRender = (window.mapScope === 'all') ? Object.values(h.districts) : [activeDist];

  districtsToRender.forEach(d => {
    Object.values(d.upazilas || {}).forEach(upz => {
      const isUpzSelected = (upz.key === currentSelectedUpazilaKey && d.id === currentSelectedDistId);

      // 1. Upazila Centroid Badge
      const upzIcon = L.divIcon({
        className: 'upazila-map-pill',
        html: `<div style="background:${isUpzSelected ? '#047857' : 'rgba(15,23,42,0.85)'};border:1.5px solid ${isUpzSelected ? '#34d399' : '#64748b'};color:#ffffff;font-size:10px;font-weight:bold;padding:2px 8px;border-radius:12px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.5);cursor:pointer;font-family:'Hind Siliguri',sans-serif;">
                🏢 ${upz.name_bn} (${upz.total_unions})
               </div>`,
        iconAnchor: [38, 12]
      });

      const upzMarker = L.marker([upz.lat, upz.lon], { icon: upzIcon }).addTo(window.leafletMap);
      upzMarker.on('click', () => {
        if (currentSelectedDistId !== d.id) {
          syncDistrictSelectors(d.id, upz.key);
        } else {
          handleUpazilaChange(upz.key);
        }
        window.leafletMap.flyTo([upz.lat, upz.lon], 11, { duration: 0.8 });
      });
      window.upazilaMapMarkers[`${d.id}_${upz.key}`] = upzMarker;

      // 2. Render every union with its specific telemetry
      (upz.unions || []).forEach(u => {
        const isUnionSelected = (u.id === currentSelectedUnionId);
        const color = getUnionConditionColor(u, activeMapLayer);
        const label = getUnionConditionLabel(u, activeMapLayer);

        const circle = L.circle([u.lat, u.lon], {
          radius: isUnionSelected ? 1800 : (isUpzSelected ? 1400 : 1200),
          color: isUnionSelected ? '#FFFFFF' : (isUpzSelected ? '#FDE047' : color),
          weight: isUnionSelected ? 4 : (isUpzSelected ? 2.5 : 1.2),
          fillColor: color,
          fillOpacity: isUnionSelected ? 0.88 : (isUpzSelected ? 0.65 : 0.45)
        }).addTo(window.leafletMap);

        const tooltipHtml = `
          <div style="font-family:'Hind Siliguri',sans-serif;min-width:170px;padding:3px;">
            <div style="font-weight:bold;font-size:13px;color:#059669;margin-bottom:2px;">📍 ${u.name_bn}</div>
            <div style="font-size:11px;color:#475569;margin-bottom:3px;">উপজেলা: <b>${upz.name_bn}</b> (${d.name_bn})</div>
            <div style="background:${color};color:#ffffff;font-size:10px;font-weight:bold;padding:2px 6px;border-radius:6px;display:inline-block;margin-bottom:4px;">
              ${label}
            </div>
            <div style="font-size:11px;color:#334155;line-height:1.4;">
              মাটি: <b>${u.soil_texture}</b><br>
              উচ্চতা: <b>${u.elevation_m} মি.</b> • ${u.river_basin || 'তিস্তা'} অববাহিকা
            </div>
            <div style="font-size:10px;color:#0284c7;font-weight:bold;margin-top:3px;">👉 ক্লিক করে এই ইউনিয়নের বিস্তারিত তথ্য দেখুন</div>
          </div>
        `;
        circle.bindTooltip(tooltipHtml, { direction: 'top', sticky: true });

        circle.on('click', () => {
          if (currentSelectedDistId !== d.id) {
            currentSelectedDistId = d.id;
          }
          currentSelectedUpazilaKey = upz.key;
          handleUnionChange(u.id);
          window.centerMapOnSelectedUnion(u);
          if (window.innerWidth < 1024) {
            document.getElementById('parcelInspectorSection')?.scrollIntoView({ behavior: 'smooth' });
          }
        });

        window.unionMapCircles[u.id] = circle;
      });
    });
  });

  updateMapLayerLegend(activeMapLayer);

  // If a union is selected, center and pulse on it
  if (currentUnionObj) {
    window.centerMapOnSelectedUnion(currentUnionObj);
  }
}

window.refreshRegionalLeafletMap = function() {
  if (!window.leafletMap) {
    window.initOrRefreshRegionalMap();
  }
  if (window.leafletMap) {
    setTimeout(() => {
      window.leafletMap.invalidateSize();
      window.centerMapOnSelectedDistrict();
    }, 60);
  }
};

window.updateMapLayerVisuals = function(layer) {
  activeMapLayer = layer;
  updateMapLayerLegend(layer);
  if (!window.leafletMap) return;

  const h = getRangpurHierarchy();
  if (!h || !h.districts) return;

  Object.entries(window.unionMapCircles).forEach(([uId, circle]) => {
    let foundUnion = null;
    let foundUpz = null;
    let foundDist = null;
    for (const d of Object.values(h.districts)) {
      for (const upz of Object.values(d.upazilas || {})) {
        for (const u of (upz.unions || [])) {
          if (u.id === uId) {
            foundUnion = u;
            foundUpz = upz;
            foundDist = d;
            break;
          }
        }
        if (foundUnion) break;
      }
      if (foundUnion) break;
    }

    if (foundUnion) {
      const isUnionSelected = (foundUnion.id === currentSelectedUnionId);
      const isUpzSelected = (foundUpz.key === currentSelectedUpazilaKey && foundDist.id === currentSelectedDistId);
      const color = getUnionConditionColor(foundUnion, layer);
      const label = getUnionConditionLabel(foundUnion, layer);

      circle.setStyle({
        radius: isUnionSelected ? 1800 : (isUpzSelected ? 1400 : 1200),
        color: isUnionSelected ? '#FFFFFF' : (isUpzSelected ? '#FDE047' : color),
        weight: isUnionSelected ? 4 : (isUpzSelected ? 2.5 : 1.2),
        fillColor: color,
        fillOpacity: isUnionSelected ? 0.88 : (isUpzSelected ? 0.65 : 0.45)
      });

      const tooltipHtml = `
        <div style="font-family:'Hind Siliguri',sans-serif;min-width:170px;padding:3px;">
          <div style="font-weight:bold;font-size:13px;color:#059669;margin-bottom:2px;">📍 ${foundUnion.name_bn}</div>
          <div style="font-size:11px;color:#475569;margin-bottom:3px;">উপজেলা: <b>${foundUpz.name_bn}</b> (${foundDist.name_bn})</div>
          <div style="background:${color};color:#ffffff;font-size:10px;font-weight:bold;padding:2px 6px;border-radius:6px;display:inline-block;margin-bottom:4px;">
            ${label}
          </div>
          <div style="font-size:11px;color:#334155;line-height:1.4;">
            মাটি: <b>${foundUnion.soil_texture}</b><br>
            উচ্চতা: <b>${foundUnion.elevation_m} মি.</b> • ${foundUnion.river_basin || 'তিস্তা'} অববাহিকা
          </div>
          <div style="font-size:10px;color:#0284c7;font-weight:bold;margin-top:3px;">👉 ক্লিক করে এই ইউনিয়নের বিস্তারিত তথ্য দেখুন</div>
        </div>
      `;
      circle.setTooltipContent(tooltipHtml);
    }
  });

  if (typeof window.updateDistrictInspectorFromLive === 'function' && window.liveAnalysisData) {
    window.updateDistrictInspectorFromLive(window.liveAnalysisData);
  }
};

window.centerMapOnSelectedDistrict = function() {
  if (!window.leafletMap || bdDistricts.length === 0) return;
  const dist = bdDistricts.find(d => d.id === currentSelectedDistId);
  if (!dist) return;
  renderLocationSpecificMapNodes();
  window.leafletMap.flyTo([dist.lat, dist.lon], 10, { duration: 0.7 });
};

function toggleBaseMapStyle() {
  if (!window.leafletMap || !streetTileLayer || !satTileLayer) return;
  useSatelliteBase = !useSatelliteBase;
  const lbl = document.getElementById('mapStyleToggleLbl');
  if (useSatelliteBase) {
    window.leafletMap.removeLayer(streetTileLayer);
    satTileLayer.addTo(window.leafletMap);
    if (lbl) lbl.textContent = currentLang === 'bn' ? 'রাস্তা ও এলাকা ভিউ' : 'Street View';
  } else {
    window.leafletMap.removeLayer(satTileLayer);
    streetTileLayer.addTo(window.leafletMap);
    if (lbl) lbl.textContent = currentLang === 'bn' ? 'স্যাটেলাইট ভিউ' : 'Satellite View';
  }
}

function locateFarmerOnMap() {
  if (!navigator.geolocation) {
    alert(currentLang === 'bn' ? 'আপনার ব্রাউজারে GPS সুবিধা নেই।' : 'Geolocation is not supported by your browser.');
    return;
  }
  const btn = document.getElementById('mapLocateBtn');
  if (btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>খোঁজা হচ্ছে...</span>';

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const { latitude, longitude } = pos.coords;
      let nearestUnion = null;
      let nearestDistId = 'rangpur';
      let nearestUpzKey = '';
      let minDist = Infinity;

      const h = getRangpurHierarchy();
      if (h && h.districts) {
        Object.entries(h.districts).forEach(([dId, dObj]) => {
          Object.entries(dObj.upazilas || {}).forEach(([uKey, uObj]) => {
            (uObj.unions || []).forEach(u => {
              const dSq = Math.pow(u.lat - latitude, 2) + Math.pow(u.lon - longitude, 2);
              if (dSq < minDist) {
                minDist = dSq;
                nearestUnion = u;
                nearestDistId = dId;
                nearestUpzKey = uKey;
              }
            });
          });
        });
      }

      if (window.leafletMap && typeof L !== 'undefined') {
        if (userGpsMarker) userGpsMarker.remove();
        userGpsMarker = L.marker([latitude, longitude]).addTo(window.leafletMap)
          .bindPopup(currentLang === 'bn' ? '📍 আপনার বর্তমান অবস্থান (GPS)' : '📍 Your Location').openPopup();
      }

      if (nearestUnion) {
        currentSelectedDistId = nearestDistId;
        currentSelectedUpazilaKey = nearestUpzKey;
        handleUnionChange(nearestUnion.id);
        window.centerMapOnSelectedUnion(nearestUnion);
      }
      if (btn) btn.innerHTML = '<i class="fa-solid fa-crosshairs"></i> <span>আমার এলাকা (GPS)</span>';
    },
    () => {
      alert(currentLang === 'bn' ? 'অবস্থান পাওয়া যায়নি। দয়া করে তালিকা থেকে বেছে নিন।' : 'Unable to retrieve GPS location.');
      if (btn) btn.innerHTML = '<i class="fa-solid fa-crosshairs"></i> <span>আমার এলাকা (GPS)</span>';
    },
    { timeout: 8000 }
  );
}

window.updateDistrictInspectorFromLive = function(data) {
  if (!data) return;
  const dist = data.district_profile || {};
  const sat = data.nasa_earth_observations || {};
  const agents = data.specialist_agent_evaluations || {};
  const master = data.master_adaptive_strategy || {};
  const isBn = currentLang === 'bn';

  const unionObj = currentUnionObj || getHierarchyUnion(currentSelectedDistId, currentSelectedUpazilaKey, currentSelectedUnionId);
  const upzObj = getHierarchyUpazila(currentSelectedDistId, currentSelectedUpazilaKey);
  const distObj = bdDistricts.find(d => d.id === currentSelectedDistId);

  const nameEl = document.getElementById('inspectorParcelName');
  if (nameEl) {
    if (unionObj && upzObj) {
      nameEl.textContent = `📍 ${unionObj.name_bn} (${upzObj.name_bn}, ${distObj ? distObj.name_bn : 'রংপুর'})`;
    } else {
      nameEl.textContent = isBn ? `${dist.name_bn || 'জেলা'} (${dist.division_bn || ''})` : `${dist.name_en || 'District'} (${dist.division || ''})`;
    }
  }

  let smapVal = sat.smap_hydrology?.root_zone_moisture_m3_m3 ?? 0.22;
  let ndviVal = sat.landsat_modis_vegetation?.ndvi_score ?? 0.50;
  let lstVal = sat.modis_lst?.land_surface_temp_day_c ?? 34.0;
  let etVal = sat.modis_lst?.evapotranspiration_rate_mm_day ?? 4.5;
  let isCritical = false;

  if (unionObj && unionObj.telemetry) {
    smapVal = unionObj.telemetry.smap_val;
    ndviVal = unionObj.telemetry.ndvi_val;
    lstVal = unionObj.telemetry.lst_val;
    isCritical = (smapVal < 0.18 || unionObj.telemetry.flood_val > 65 || lstVal >= 36.0);
  }

  const smapPct = Math.round(smapVal * 100);

  const moistEl = document.getElementById('inspectorMoistVal');
  const moistBar = document.getElementById('inspectorMoistBar');
  if (moistEl) {
    const moistLbl = unionObj?.telemetry?.smap_label || (smapPct < 18 ? 'শুকনো (<১৮%)' : 'মাঝারি রস');
    moistEl.textContent = `${smapPct}% (${moistLbl})`;
  }
  if (moistBar) {
    moistBar.style.width = `${Math.min(100, Math.max(12, Math.round(smapPct * 2.5)))}%`;
    moistBar.className = `h-full rounded-full transition-all duration-500 ${smapVal < 0.18 ? 'bg-rose-500' : smapVal < 0.23 ? 'bg-amber-500' : 'bg-emerald-500'}`;
  }

  const ndviEl = document.getElementById('inspectorNdviVal');
  const ndviBar = document.getElementById('inspectorNdviBar');
  if (ndviEl) {
    const ndviLbl = unionObj?.telemetry?.ndvi_label || 'স্বাভাবিক সবুজ';
    ndviEl.textContent = `${ndviVal} (${ndviLbl})`;
  }
  if (ndviBar) {
    ndviBar.style.width = `${Math.min(100, Math.max(10, Math.round(ndviVal * 100)))}%`;
    ndviBar.className = `h-full rounded-full transition-all duration-500 ${ndviVal >= 0.55 ? 'bg-emerald-600' : ndviVal >= 0.45 ? 'bg-lime-500' : 'bg-amber-500'}`;
  }

  const etEl = document.getElementById('inspectorEtVal');
  const etBar = document.getElementById('inspectorEtBar');
  if (etEl) {
    const lstLbl = unionObj?.telemetry?.lst_label || `${lstVal}°C`;
    etEl.textContent = `${lstVal}°C (${lstLbl}) • ${etVal} মিমি/দিন`;
  }
  if (etBar) {
    etBar.style.width = `${Math.min(100, Math.max(15, Math.round((lstVal / 42) * 100)))}%`;
    etBar.className = `h-full rounded-full transition-all duration-500 ${lstVal >= 36 ? 'bg-rose-600' : lstVal >= 33 ? 'bg-amber-500' : 'bg-emerald-500'}`;
  }

  const advEl = document.getElementById('inspectorAdvice');
  if (advEl) {
    if (unionObj) {
      advEl.innerHTML = `
        <div class="space-y-1.5 text-left">
          <div class="text-[11px] font-bold text-emerald-900 dark:text-emerald-200">
            🌾 <strong>প্রস্তাবিত ফসল প্যাটার্ন:</strong> ${unionObj.recommended_pattern || 'শীতকালীন সবজি ও আলু'}
          </div>
          <div class="text-[11px] text-slate-700 dark:text-slate-300">
            💧 <strong>মাটি ও নিষ্কাশন:</strong> ${unionObj.soil_texture} (${unionObj.elevation_type}) • ${unionObj.drainage || 'উত্তম নিষ্কাশন'}
          </div>
          <div class="text-[11px] text-slate-700 dark:text-slate-300">
            ⛰️ <strong>উচ্চতা ও নদী:</strong> সমুদ্রপৃষ্ঠ থেকে ${unionObj.elevation_m} মিটার • ${unionObj.river_basin || 'তিস্তা'} অববাহিকা
          </div>
          <div class="text-[11px] text-harvest-700 dark:text-harvest-400 font-semibold pt-1 border-t border-emerald-200 dark:border-emerald-700/60">
            🤖 <strong>নাসা এগ্রো-এজেন্ট পরামর্শ:</strong> ${master.farmer_directive_bn || agents.soil_agent?.observations_bn || 'পরিমিত সেচ ও উপযুক্ত ফসল চক্র বজায় রাখুন।'}
          </div>
        </div>
      `;
    } else {
      advEl.textContent = master.farmer_directive_bn || agents.soil_agent?.observations_bn || '';
    }
  }

  const badge = document.getElementById('inspectorStatusBadge');
  if (badge) {
    badge.innerHTML = `<i class="fa-solid fa-circle-info"></i> ${isCritical ? (isBn ? 'সতর্কতামূলক পর্যবেক্ষণ' : 'Alert') : (isBn ? 'অনুকূল পর্যবেক্ষণ' : 'Optimal')}`;
    badge.className = isCritical
      ? 'px-2.5 sm:px-3 py-1 rounded-full text-[11px] sm:text-xs font-black border flex items-center gap-1 bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border-rose-300'
      : 'px-2.5 sm:px-3 py-1 rounded-full text-[11px] sm:text-xs font-black border flex items-center gap-1 bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-300';
  }
};
"""

normalized_c = content.replace("\r\n", "\n")
start_idx = normalized_c.find(old_map_logic_start)
end_idx = normalized_c.find(old_map_logic_end)

if start_idx != -1 and end_idx != -1:
    content = normalized_c[:start_idx] + new_map_logic + "\n" + normalized_c[end_idx:]
    print("✓ Patched Map Logic Engine")
else:
    print(f"⚠ Map logic markers not found: start={start_idx}, end={end_idx}")

# Also make sure syncDistrictSelectors calls renderLocationSpecificMapNodes()
if "renderLocationSpecificMapNodes()" not in content:
    content = content.replace("updateHeroDistrictBadges(distId);", "updateHeroDistrictBadges(distId);\n  if (typeof renderLocationSpecificMapNodes === 'function') renderLocationSpecificMapNodes();")
    print("✓ Added renderLocationSpecificMapNodes hook to syncDistrictSelectors")

# Save updated files
with open(FRONTEND_FILE, "w", encoding="utf-8") as f:
    f.write(content)
print(f"✓ Saved updated {FRONTEND_FILE}")

shutil.copyfile(FRONTEND_FILE, ROOT_FILE)
print(f"✓ Mirrored to root {ROOT_FILE}")

