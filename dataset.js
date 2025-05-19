if (typeof window !== 'undefined') {
  window.dataset = dataset;
  if (typeof window.logStatus === 'function') {
    window.logStatus('dataset.js executed, size: ' + (Array.isArray(dataset) ? dataset.length : 'unknown'));
  }
} else if (typeof globalThis !== 'undefined') {
  globalThis.dataset = dataset;
}
console.log('Dataset loaded:', Array.isArray(dataset) ? dataset.length : 'unknown', 'prompts');
