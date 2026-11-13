"""
Script to format the project files according to README.md specification.
Creates:
1. Root index.html (synced from frontend/index.html)
2. Standalone HTML entry points:
   - crop-recommender.html
   - dashboard.html
   - irrigation-alerts.html
   - map-explorer.html
   - resources.html
3. Assets directory at root:
   - assets/icons/logo.png
   - assets/icons/logo.svg
4. css/styles.css
5. js/ modules:
   - js/app.js
   - js/calculator.js
   - js/i18n.js
   - js/map.js
   - js/voice-assistant.js
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Sync index.html to root
frontend_index = BASE_DIR / "frontend" / "index.html"
root_index = BASE_DIR / "index.html"
if frontend_index.exists():
    shutil.copy(frontend_index, root_index)
    print("✓ Synced root index.html")

# 2. Sync assets to root
assets_icons = BASE_DIR / "assets" / "icons"
assets_icons.mkdir(parents=True, exist_ok=True)
src_logo = BASE_DIR / "frontend" / "assets" / "icons" / "logo.png"
if src_logo.exists():
    shutil.copy(src_logo, assets_icons / "logo.png")
    print("✓ Synced assets/icons/logo.png")

# Create SVG logo if not exists
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#10b981;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#047857;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="46" fill="url(#grad)" stroke="#ffffff" stroke-width="3"/>
  <path d="M50 20 C35 35 30 55 50 80 C70 55 65 35 50 20 Z" fill="#ffffff" opacity="0.95"/>
  <circle cx="50" cy="48" r="8" fill="#f59e0b"/>
</svg>'''
with open(assets_icons / "logo.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print("✓ Created assets/icons/logo.svg")

# 3. Create standalone HTML pages
standalone_pages = {
    "crop-recommender.html": ("crop-recommender", "ফসল চক্র ও লাভজনক বিকল্প ফসল (Crop Recommender)"),
    "dashboard.html": ("dashboard", "ফসলের হালচাল ও টেলিমেট্রি ড্যাশবোর্ড (Farm Dashboard)"),
    "irrigation-alerts.html": ("irrigation-alerts", "সেচ সতর্কতা ও পাম্প খরচের হিসাব (Irrigation Alerts)"),
    "map-explorer.html": ("map-explorer", "নাসা স্যাটেলাইট জমির নকশা (Satellite Parcel Explorer)"),
    "resources.html": ("resources", "নাসা গাইড, ডাটা ভ্যালিডেশন ও বৈজ্ঞানিক গবেষণা (NASA Guide & Resources)")
}

template = """<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url=index.html#{hash_route}">
  <title>কৃষি BONDHU AI - {title}</title>
  <link rel="icon" href="assets/icons/logo.png" type="image/png">
  <script>
    window.location.replace("index.html#{hash_route}");
  </script>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #0f172a; color: #f8fafc; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
    .loader-box {{ text-align: center; padding: 24px; border-radius: 20px; background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(255,255,255,0.1); max-width: 440px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
    .spinner {{ width: 44px; height: 44px; border: 4px solid rgba(16, 185, 129, 0.2); border-top-color: #10b981; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    h2 {{ font-size: 1.1rem; margin-bottom: 8px; color: #34d399; }}
    p {{ font-size: 0.9rem; color: #94a3b8; line-height: 1.5; }}
    a {{ color: #10b981; font-weight: bold; text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="loader-box">
    <div class="spinner"></div>
    <h2>{title}</h2>
    <p>নির্দিষ্ট মডিউলে নিয়ে যাওয়া হচ্ছে...<br><a href="index.html#{hash_route}">স্বয়ংক্রিয়ভাবে লোড না হলে এখানে ক্লিক করুন</a></p>
  </div>
</body>
</html>"""

for fname, (route, tit) in standalone_pages.items():
    page_path = BASE_DIR / fname
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(template.format(hash_route=route, title=tit))
    print(f"✓ Created {fname}")

# 4. Create css/styles.css
css_dir = BASE_DIR / "css"
css_dir.mkdir(parents=True, exist_ok=True)
styles_css = """/*
 * Krishi BONDHU AI Global Design System & Ergonomics
 * Aligned with NASA Space Apps 2026 Standards
 */

:root {
  --leaf-500: #10b981;
  --leaf-600: #059669;
  --leaf-700: #047857;
  --terracotta-500: #f97316;
  --harvest-500: #eab308;
  --canal-500: #0284c7;
  --earth-800: #1e293b;
  --earth-900: #0f172a;
}

/* Touch-First Accessibility Targets for Smallholder Farmers (48px+) */
.touch-target {
  min-height: 48px;
  min-width: 48px;
}

/* Smooth Scrolling & Safe Area Padding for Mobile Phones */
html {
  scroll-behavior: smooth;
}

.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 16px);
}

.pt-safe {
  padding-top: env(safe-area-inset-top, 16px);
}

/* Voice Microphone Pulsing Animation */
@keyframes pulse-mic {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
  70% { box-shadow: 0 0 0 20px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.pulse-mic {
  animation: pulse-mic 2s infinite cubic-bezier(0.66, 0, 0, 1);
}

/* Focus and Accessibility Ring */
button:focus-visible, a:focus-visible, select:focus-visible, input:focus-visible {
  outline: 2px solid var(--leaf-500);
  outline-offset: 2px;
}
"""
with open(css_dir / "styles.css", "w", encoding="utf-8") as f:
    f.write(styles_css)
print("✓ Created css/styles.css")

# 5. Create js/ modules
js_dir = BASE_DIR / "js"
js_dir.mkdir(parents=True, exist_ok=True)

# js/calculator.js
calc_js = """/**
 * Krishi BONDHU AI - Precision Irrigation & Fuel Cost Calculator Module
 * Formulations derived from NASA POWER, SMAP & Department of Agricultural Extension (DAE)
 */

window.IrrigationCalculator = {
  // Base crop water demand (Liters per Bigha)
  cropWaterDemand: {
    boro_rice: 45000,
    maize: 28000,
    wheat: 22000,
    sorghum: 18000,
    mustard: 15000,
    pearl_millet: 14000,
    mungbean: 12000,
    lentil: 12000,
    potato: 20000
  },

  // Tariff baselines in Bangladesh (BDT)
  tariffs: {
    dieselPerLiter: 108.0, // ৳/L
    electricPerKWh: 8.5    // ৳/kWh (Agri-subsidized tariff)
  },

  /**
   * Calculates required water volume (Liters)
   */
  calculateWaterVolume: function(bigha, cropId, weatherFactor = 1.0) {
    const baseDemand = this.cropWaterDemand[cropId] || 25000;
    return Math.round(bigha * baseDemand * weatherFactor);
  },

  /**
   * Calculates pump discharge rate Q (Liters per Hour)
   */
  getPumpDischargeRate: function(hp) {
    return Math.max(6000, hp * 4000);
  },

  /**
   * Calculates required runtime in hours
   */
  calculateRuntimeHours: function(totalWaterLiters, hp) {
    const dischargeRate = this.getPumpDischargeRate(hp);
    return totalWaterLiters / dischargeRate;
  },

  /**
   * Calculates fuel or power expense
   */
  calculateCost: function(runtimeHours, hp, powerSource = 'diesel') {
    if (powerSource === 'diesel') {
      const litersConsumed = runtimeHours * hp * 0.22;
      const cost = litersConsumed * this.tariffs.dieselPerLiter;
      return { litersConsumed: Math.round(litersConsumed * 10) / 10, costBdt: Math.round(cost) };
    } else {
      const kwhConsumed = runtimeHours * hp * 0.75;
      const cost = kwhConsumed * this.tariffs.electricPerKWh;
      return { kwhConsumed: Math.round(kwhConsumed * 10) / 10, costBdt: Math.round(cost) };
    }
  }
};
"""
with open(js_dir / "calculator.js", "w", encoding="utf-8") as f:
    f.write(calc_js)
print("✓ Created js/calculator.js")

# js/i18n.js
i18n_js = """/**
 * Krishi BONDHU AI - Bilingual Isolation Dictionary (Bangla & English)
 */

window.BilingualDictionary = {
  bn: {
    appTitle: "কৃষি BONDHU AI",
    tagline: "নাসার স্যাটেলাইট অবজারভেশন ভিত্তিক স্মার্ট কৃষি সিদ্ধান্ত ইঞ্জিন",
    navHome: "প্রথম পাতা",
    navMap: "জমির নকশা",
    navCrops: "ফসল চক্র",
    navCalc: "সেচ ও খরচ",
    navDash: "ফসলের হালচাল",
    navGuide: "নাসা গাইড",
    selectDistrict: "জেলা নির্বাচন করুন",
    pastCropLabel: "পূর্ববর্তী ফসল",
    monoYearsLabel: "টানা কত বছর একই ফসল চাষ করছেন?",
    priorityGoal: "আপনার প্রধান উদ্দেশ্য",
    runAnalysis: "৬+১ এআই এজেন্ট দিয়ে খামার বিশ্লেষণ চালান",
    hotlineText: "জরুরি কৃষি সহায়তায় কল করুন: ১৬১২৩"
  },
  en: {
    appTitle: "Krishi BONDHU AI",
    tagline: "NASA Earth Observation Powered Precision Farming Decision Engine",
    navHome: "Home",
    navMap: "Parcel Map",
    navCrops: "Crop Rotation",
    navCalc: "Irrigation & Cost",
    navDash: "Dashboard",
    navGuide: "NASA Guide",
    selectDistrict: "Select District",
    pastCropLabel: "Previous Crop",
    monoYearsLabel: "Consecutive Years of Same Crop",
    priorityGoal: "Farmer Primary Objective",
    runAnalysis: "Run 6+1 Multi-Agent Farm Analysis",
    hotlineText: "National Agriculture Helpline: 16123"
  }
};
"""
with open(js_dir / "i18n.js", "w", encoding="utf-8") as f:
    f.write(i18n_js)
print("✓ Created js/i18n.js")

# js/map.js
map_js = """/**
 * Krishi BONDHU AI - Geospatial Layer Controller
 * Supports SMAP, Landsat NDVI, MODIS LST, and GPM Rain Radar
 */

window.MapController = {
  activeLayer: 'smap',
  layers: {
    smap: { nameBn: 'মাটির আর্দ্রতা (SMAP)', unit: 'm³/m³', colorScale: ['#ef4444', '#f59e0b', '#10b981', '#0284c7'] },
    ndvi: { nameBn: 'উদ্ভিদের সজীবতা (Landsat NDVI)', unit: 'Score', colorScale: ['#b45309', '#eab308', '#22c55e', '#15803d'] },
    lst:  { nameBn: 'ভূমির তাপমাত্রা (MODIS LST)', unit: '°C', colorScale: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'] },
    gpm:  { nameBn: 'বৃষ্টিপাত রাডার (GPM IMERG)', unit: 'mm/day', colorScale: ['#f8fafc', '#93c5fd', '#3b82f6', '#1e40af'] }
  },
  rangpurDistricts: [
    { id: 'rangpur', nameBn: 'রংপুর', lat: 25.7439, lon: 89.2752 },
    { id: 'dinajpur', nameBn: 'দিনাজপুর', lat: 25.6217, lon: 88.6355 },
    { id: 'kurigram', nameBn: 'কুড়িগ্রাম', lat: 25.8054, lon: 89.6362 },
    { id: 'gaibandha', nameBn: 'গাইবান্ধা', lat: 25.3288, lon: 89.5408 },
    { id: 'nilphamari', nameBn: 'নীলফামারী', lat: 25.9318, lon: 88.8560 },
    { id: 'thakurgaon', nameBn: 'ঠাকুরগাঁও', lat: 26.0337, lon: 88.4617 },
    { id: 'panchagarh', nameBn: 'পঞ্চগড়', lat: 26.3411, lon: 88.5542 },
    { id: 'lalmonirhat', nameBn: 'লালমনিরহাট', lat: 25.9923, lon: 89.2847 }
  ]
};
"""
with open(js_dir / "map.js", "w", encoding="utf-8") as f:
    f.write(map_js)
print("✓ Created js/map.js")

# js/voice-assistant.js
voice_js = """/**
 * Krishi BONDHU AI - AgroBani Voice Assistant Module (STT & TTS)
 * Colloquial Bangla (bn-BD) and English (en-US)
 */

window.AgroBaniVoice = {
  isListening: false,
  synth: window.speechSynthesis,
  recognition: null,

  init: function() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'bn-BD';
    }
  },

  speak: function(text, lang = 'bn-BD') {
    if (!this.synth) return;
    this.synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.95;
    this.synth.speak(utterance);
  }
};
"""
with open(js_dir / "voice-assistant.js", "w", encoding="utf-8") as f:
    f.write(voice_js)
print("✓ Created js/voice-assistant.js")

# js/app.js
app_js = """/**
 * Krishi BONDHU AI - Main Application Controller
 * Handles Theme, Audio Ambience, and System Event Binding
 */

window.AppController = {
  theme: localStorage.getItem('krishi_theme') || 'light',
  audioCtx: null,

  initTheme: function() {
    if (this.theme === 'dark' || (!('krishi_theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  },

  toggleTheme: function() {
    const isDark = document.documentElement.classList.toggle('dark');
    this.theme = isDark ? 'dark' : 'light';
    localStorage.setItem('krishi_theme', this.theme);
  },

  playFieldWindAmbience: function() {
    if (!this.audioCtx) {
      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    // Procedural wind synthesizer using Web Audio API pink noise
    const bufferSize = this.audioCtx.sampleRate * 2;
    const buffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      data[i] = (b0 + b1 + b2) * 0.08;
    }
    const noise = this.audioCtx.createBufferSource();
    noise.buffer = buffer;
    noise.loop = true;
    const filter = this.audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(320, this.audioCtx.currentTime);
    noise.connect(filter);
    filter.connect(this.audioCtx.destination);
    noise.start();
    return noise;
  }
};
"""
with open(js_dir / "app.js", "w", encoding="utf-8") as f:
    f.write(app_js)
print("✓ Created js/app.js")

print("\n🎉 ALL PROJECT FILES FORMATTED PERFECTLY ACCORDING TO README.MD!")

