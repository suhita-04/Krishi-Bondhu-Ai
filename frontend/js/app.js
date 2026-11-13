/**
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
