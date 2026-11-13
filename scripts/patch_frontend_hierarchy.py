"""
Patch frontend/index.html to implement 3-tier Zilla -> Upazila -> Union selection
in Hero section, and verify all sections.
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"
ROOT_FILE = BASE_DIR / "index.html"

with open(FRONTEND_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the hero district dropdown
hero_idx = -1
for i, l in enumerate(lines):
    if 'id="heroDistrictSelect"' in l:
        hero_idx = i
        break

if hero_idx != -1:
    # Find closing tag </select>
    close_idx = -1
    for j in range(hero_idx, hero_idx + 25):
        if '</select>' in lines[j]:
            close_idx = j
            break
    
    if close_idx != -1:
        # Check comment right before hero_idx
        start_idx = hero_idx
        if '<!-- Rangpur 8-District Dropdown' in lines[hero_idx - 1]:
            start_idx = hero_idx - 1

        hero_replacement = """       <!-- Rangpur 8-District Dropdown (১. জেলা নির্বাচন) -->
       <div>
         <label class="block text-[11px] font-bold text-slate-300 mb-1 flex items-center justify-between">
           <span class="flex items-center gap-1"><i class="fa-solid fa-map-pin text-harvest-400"></i> ১. জেলা নির্বাচন (রংপুর বিভাগের ৮ জেলা):</span>
           <span class="text-[10px] text-emerald-400 font-normal">রংপুর বিভাগ কনফিগারড</span>
         </label>
         <select id="heroDistrictSelect" onchange="onDistrictSelectionChanged()" class="w-full bg-slate-900 border-2 border-leaf-500 rounded-xl px-3 py-2 text-sm sm:text-base text-white font-bold focus:outline-none shadow-inner">
           <option value="rangpur" selected>রংপুর (Rangpur) - তিস্তা প্লাবনভূমি ও মঙ্গা/খরা ঝুঁকি</option>
           <option value="dinajpur">দিনাজপুর (Dinajpur) - পুরাতন হিমালয় পাদদেশীয় বেলে-দোআঁশ ও খরা</option>
           <option value="kurigram">কুড়িগ্রাম (Kurigram) - তিস্তা ও ব্রহ্মপুত্র চরাঞ্চল ও নদীভাঙন</option>
           <option value="gaibandha">গাইবান্ধা (Gaibandha) - তিস্তা ও ব্রহ্মপুত্র চরাঞ্চল ও মৌসুমি প্লাবন</option>
           <option value="nilphamari">নীলফামারী (Nilphamari) - তিস্তা সেচ ক্যানেল ও স্বল্প বৃষ্টিপাত</option>
           <option value="thakurgaon">ঠাকুরগাঁও (Thakurgaon) - অম্লীয় বেলে-দোআঁশ ও ভূগর্ভস্থ পাথর স্তর</option>
           <option value="panchagarh">পঞ্চগড় (Panchagarh) - হিমালয় সংলগ্ন চরম শৈত্যপ্রবাহ ও কুয়াশা</option>
           <option value="lalmonirhat">লালমনিরহাট (Lalmonirhat) - তিস্তা ব্যারাজ ভাটি অঞ্চল ও বালুময় চর</option>
         </select>
       </div>

       <!-- 3-Tier Hierarchy: Upazila & Union Selectors (২. উপজেলা ➔ ৩. ইউনিয়ন) -->
       <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-0.5">
         <div>
           <label class="block text-[11px] font-bold text-slate-300 mb-1 flex items-center gap-1">
             <i class="fa-solid fa-tree-city text-emerald-400"></i> ২. উপজেলা নির্বাচন (৫৬ উপজেলা):
           </label>
           <select id="heroUpazilaSelect" onchange="onHeroUpazilaChanged()" class="w-full bg-slate-900 border-2 border-leaf-500/80 rounded-xl px-3 py-2 text-xs sm:text-sm text-white font-bold focus:outline-none shadow-inner">
             <!-- Populated dynamically -->
           </select>
         </div>
         <div>
           <label class="block text-[11px] font-bold text-slate-300 mb-1 flex items-center gap-1">
             <i class="fa-solid fa-house-chimney-window text-emerald-400"></i> ৩. ইউনিয়ন নির্বাচন (৫৩৬ ইউনিয়ন):
           </label>
           <select id="heroUnionSelect" onchange="onHeroUnionChanged()" class="w-full bg-slate-900 border-2 border-leaf-500/80 rounded-xl px-3 py-2 text-xs sm:text-sm text-white font-bold focus:outline-none shadow-inner">
             <!-- Populated dynamically -->
           </select>
         </div>
       </div>

       <!-- Union Telemetry Status Card -->
       <div id="heroUnionDetailsBadge" class="p-2 sm:p-2.5 rounded-xl bg-emerald-950/70 border border-emerald-500/50 text-[11px] text-emerald-200 flex flex-wrap items-center justify-between gap-1.5 shadow-sm">
         <span id="heroUnionInfoText"><i class="fa-solid fa-location-dot text-emerald-400 mr-1"></i> <strong id="heroUnionNameLbl" class="text-white">রংপুর সদর</strong> | মাটির ধরন: <span id="heroUnionSoilLbl" class="text-emerald-300 font-bold">দোআঁশ</span></span>
         <span class="font-mono text-harvest-300 font-bold" id="heroUnionMetaLbl">উচ্চতা: ৩০.৫ মি. | অববাহিকা: তিস্তা</span>
       </div>
"""
        new_lines = lines[:start_idx] + [hero_replacement] + lines[close_idx + 1:]
        with open(FRONTEND_FILE, "w", encoding="utf-8") as out_f:
            out_f.writelines(new_lines)
        print("✓ Hero section successfully replaced with 3-tier cascade!")
        
        # Mirror to root index.html
        shutil.copyfile(FRONTEND_FILE, ROOT_FILE)
        print("✓ Mirrored to root index.html")
    else:
        print("⚠ Could not find </select> tag for hero")
else:
    print("⚠ Could not find heroDistrictSelect")
