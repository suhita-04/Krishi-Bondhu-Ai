/**
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
