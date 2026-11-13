/**
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
