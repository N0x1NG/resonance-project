// PAK Human Biometric Logger

const logger = {
  startTime: null,
  data: [],
  isLogging: false,
  stream: null,
  audioContext: null,
  analyser: null,

  async init() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ 
        video: true, 
        audio: true 
      });
      
      document.getElementById('webcam').srcObject = this.stream;
      
      this.audioContext = new AudioContext();
      const source = this.audioContext.createMediaStreamSource(this.stream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      source.connect(this.analyser);
      
      this.updateStatus('Ready. Click Start to begin logging.');
    } catch (err) {
      this.updateStatus('Error: ' + err.message);
    }
  },

  updateStatus(msg) {
    document.getElementById('status').textContent = 'Status: ' + msg;
  },

  getTimestamp() {
    return Date.now() - this.startTime;
  },

  getAudioLevel() {
    if (!this.analyser) return 0;
    const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
    this.analyser.getByteFrequencyData(dataArray);
    const avg = dataArray.reduce((a, b) => a + b) / dataArray.length;
    return Math.round(avg);
  },

  log(event, value) {
    const entry = {
      timestamp: this.getTimestamp(),
      event: event,
      value: value,
      audioLevel: this.getAudioLevel(),
      isoTime: new Date().toISOString()
    };
    this.data.push(entry);
    this.renderData();
    return entry;
  },

  renderData() {
    const dataEl = document.getElementById('data');
    const recent = this.data.slice(-20);
    dataEl.textContent = JSON.stringify(recent, null, 2);
  },

  startLoop() {
    if (!this.isLogging) return;
    
    this.log('ambient', {
      audioLevel: this.getAudioLevel()
    });
    
    setTimeout(() => this.startLoop(), 1000);
  },

  export() {
    const blob = new Blob([JSON.stringify(this.data, null, 2)], {
      type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pak-human-log-${Date.now()}.json`;
    a.click();
  }
};

function startLogging() {
  logger.startTime = Date.now();
  logger.isLogging = true;
  logger.data = [];
  logger.log('session_start', { userAgent: navigator.userAgent });
  logger.startLoop();
  logger.updateStatus('LOGGING ACTIVE 🔴');
}

function stopLogging() {
  logger.isLogging = false;
  logger.log('session_end', { totalEntries: logger.data.length });
  logger.updateStatus('Logging stopped. ' + logger.data.length + ' entries captured.');
}

function tagEvent(tag) {
  if (!logger.isLogging) {
    logger.updateStatus('Start logging first!');
    return;
  }
  logger.log('manual_tag', { tag: tag });
  logger.updateStatus('Tagged: ' + tag);
}

function exportData() {
  logger.export();
  logger.updateStatus('Data exported!');
}

window.onload = () => logger.init();
