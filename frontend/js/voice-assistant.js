/**
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
