if (typeof window.appendLoadingDebug === 'function') {
  appendLoadingDebug('dataset-loader.js executing (protocol ' + location.protocol + ')');
}

function handleError(err) {
  console.error('Failed to load dataset.json', err);
  if (typeof window.appendLoadingDebug === 'function') {
    appendLoadingDebug('Error fetching dataset.json: ' + (err.message || err));
  }
  if (typeof window.datasetReject === 'function') {
    window.datasetReject(err);
  }
}

if (location.protocol === 'file:') {
  handleError(new Error('Cannot fetch dataset.json when using file:// protocol'));
} else {
  if (typeof window.stepDebug === 'function') {
    window.stepDebug('Fetching dataset.json');
  } else {
    appendLoadingDebug('Fetching dataset.json');
  }
  fetch('dataset.json')
    .then(r => {
      if (typeof window.stepDebug === 'function') {
        window.stepDebug('dataset.json HTTP status ' + r.status);
      } else if (typeof window.appendLoadingDebug === 'function') {
        appendLoadingDebug('dataset.json HTTP status ' + r.status);
      }
      if (!r.ok) {
        throw new Error('HTTP ' + r.status + ' ' + r.statusText);
      }
      return r.json();
    })
    .then(data => {
      if (typeof window.stepDebug === 'function') {
        const len = Array.isArray(data) ? data.length : '?';
        window.stepDebug('dataset.json parsed, length ' + len);
      } else if (typeof window.appendLoadingDebug === 'function') {
        const len = Array.isArray(data) ? data.length : '?';
        appendLoadingDebug('dataset.json parsed, length ' + len);
      }
      window.dataset = data;
      if (typeof window.datasetResolve === 'function') {
        window.datasetResolve();
      }
    })
    .catch(handleError);
}
