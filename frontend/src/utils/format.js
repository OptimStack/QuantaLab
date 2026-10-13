export const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
};

export const formatDuration = (seconds) => {
  if (typeof seconds !== 'number') return '0m 0s';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}m ${s}s`;
};

export const formatPercentage = (value) => {
  if (typeof value !== 'number') return '0.0%';
  return `${(value * 100).toFixed(1)}%`;
};

export const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const formatComplexNumber = ({ real, imag }) => {
  const r = real.toFixed(3);
  const i = imag.toFixed(3);
  if (imag >= 0) {
    return `${r} + ${i}i`;
  } else {
    return `${r} - ${Math.abs(imag).toFixed(3)}i`;
  }
};

export const formatProbability = (counts, totalShots) => {
  const probs = {};
  for (const [state, count] of Object.entries(counts)) {
    probs[state] = count / totalShots;
  }
  return probs;
};
