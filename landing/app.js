const runtimeRoot = new URL('.', document.currentScript.src);
const languageLinks = document.querySelectorAll('[data-language]');
const roster = document.querySelector('.roster');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const portraitBounds = [
  [60, 170, 360], [420, 260, 320], [735, 190, 350], [1120, 190, 380],
  [45, 570, 430], [495, 640, 300], [825, 615, 300], [1150, 595, 380]
];
const validLanguage = value => Object.hasOwn(COPY, value);
let selectedHire = 0;
let language = document.documentElement.lang;
let copyState = null;
let selectedMetric = 'total_tokens';
let languageRequest = 0;
const experimentCache = new Map([[language, Promise.resolve(document.querySelector('.experiment').outerHTML)]]);

function initialLanguage() {
  const requested = new URL(location.href).searchParams.get('lang');
  if (validLanguage(requested)) return requested;
  const route = location.pathname.slice(runtimeRoot.pathname.length).split('/')[0];
  if (validLanguage(route)) return route;
  try {
    const saved = localStorage.getItem('qh-language');
    if (validLanguage(saved)) return saved;
  } catch { /* Preference storage is optional. */ }
  return navigator.language.toLowerCase().startsWith('ko') ? 'ko' : 'en';
}

function updateProfile(animate = false) {
  const hire = HIRES[selectedHire];
  const content = hire[language];
  document.querySelector('#profile-number').textContent = `${String(selectedHire + 1).padStart(2, '0')} / 08`;
  document.querySelector('#profile-code').textContent = hire.id.toUpperCase();
  document.querySelector('#profile-name').textContent = content.name;
  document.querySelector('#profile-quote').textContent = content.quote;
  document.querySelector('#skill-description').textContent = content.description;
  document.querySelector('#skill-prompt').textContent = `$${hire.id}\n${content.prompt}`;
  document.querySelector('#example-link').href = `https://github.com/SoonGwan/questionable-hires/blob/main/examples/${hire.id}.md`;
  const portrait = document.querySelector('.portrait img');
  const [x, y, size] = portraitBounds[selectedHire];
  portrait.style.width = `${1536 / size * 100}%`;
  portrait.style.left = `${-x / size * 100}%`;
  portrait.style.top = `${-y / size * 100}%`;
  if (animate && !reducedMotion.matches) {
    document.querySelector('.portrait').getAnimations().forEach(animation => animation.cancel());
    document.querySelector('.portrait').animate([
      { opacity: 0, transform: 'translateY(10px) rotate(-3deg)' },
      { opacity: 1, transform: 'translateY(0) rotate(0)' }
    ], { duration: 380, easing: 'cubic-bezier(.22,1,.36,1)' });
  }
}

roster.querySelectorAll('[data-hire]').forEach(button => {
  button.addEventListener('click', () => {
    selectedHire = Number(button.dataset.hire);
    roster.querySelectorAll('button').forEach((item, i) => item.setAttribute('aria-pressed', String(i === selectedHire)));
    updateProfile(true);
  });
});

function updateChart() {
  document.querySelector('.chart-controls').hidden = false;
  document.querySelectorAll('[data-metric]').forEach(button => {
    button.setAttribute('aria-pressed', String(button.dataset.metric === selectedMetric));
  });
  document.querySelectorAll('[data-chart]').forEach(chart => { chart.hidden = chart.dataset.chart !== selectedMetric; });
}

document.querySelector('#evidence').addEventListener('click', event => {
  const button = event.target.closest('[data-metric]');
  if (button) {
    selectedMetric = button.dataset.metric;
    updateChart();
  }
});

function updateMetadata(content) {
  const url = `${SITE.baseUrl}${language}/`;
  const image = `${SITE.baseUrl}assets/og-${language}.png`;
  document.title = content.title;
  document.querySelector('meta[name="description"]').content = content.description;
  const properties = {
    'og:title': content.title, 'og:description': content.description, 'og:url': url,
    'og:locale': language === 'ko' ? 'ko_KR' : 'en_US',
    'og:locale:alternate': language === 'ko' ? 'en_US' : 'ko_KR',
    'og:image': image, 'og:image:secure_url': image, 'og:image:alt': content.ogAlt
  };
  for (const [key, value] of Object.entries(properties)) {
    const meta = document.querySelector(`meta[property="${key}"]`);
    if (meta) meta.content = value;
  }
  for (const [key, value] of Object.entries({
    'twitter:title': content.title, 'twitter:description': content.description,
    'twitter:image': image, 'twitter:image:alt': content.ogAlt
  })) document.querySelector(`meta[name="${key}"]`).content = value;
  document.querySelector('link[rel="canonical"]').href = url;
  const structured = document.querySelector('script[type="application/ld+json"]');
  const graph = JSON.parse(structured.textContent);
  Object.assign(graph['@graph'][1], {
    '@id': `${url}#page`, url, name: content.title, description: content.description, inLanguage: language
  });
  structured.textContent = JSON.stringify(graph);
}

async function setLanguage(next, persist = false) {
  if (!validLanguage(next)) return;
  const request = ++languageRequest;
  if (!experimentCache.has(next)) {
    experimentCache.set(next, fetch(new URL(`experiments/${next}.html`, runtimeRoot)).then(response => {
      if (!response.ok) throw new Error('Experiment translation unavailable');
      return response.text();
    }));
  }
  let experiment;
  try {
    experiment = await experimentCache.get(next);
  } catch {
    experimentCache.delete(next);
    if (request === languageRequest) location.assign(new URL(`${next}/${location.hash}`, runtimeRoot));
    return;
  }
  if (request !== languageRequest) return;
  const detailsOpen = document.querySelector('.raw-details').open;
  const checkpointOpen = document.querySelector('.checkpoint-details')?.open;
  const tableScroll = Array.from(document.querySelectorAll('.experiment .table-scroll'), table =>
    table.scrollLeft / Math.max(1, table.scrollWidth - table.clientWidth));
  language = next;
  const content = COPY[language];
  document.documentElement.lang = language;
  document.querySelector('.experiment').outerHTML = experiment;
  document.querySelector('.raw-details').open = detailsOpen;
  if (document.querySelector('.checkpoint-details')) document.querySelector('.checkpoint-details').open = checkpointOpen;
  document.querySelectorAll('[data-evidence-file]').forEach(link => {
    link.href = new URL(link.dataset.evidenceFile, runtimeRoot);
  });
  document.querySelectorAll('[data-download-file]').forEach(link => {
    link.href = new URL(`downloads/${link.dataset.downloadFile}`, runtimeRoot);
  });
  updateChart();
  updateMetadata(content);
  document.querySelectorAll('[data-i18n]').forEach(element => { element.textContent = content[element.dataset.i18n]; });
  document.querySelectorAll('[data-i18n-alt]').forEach(element => { element.alt = content[element.dataset.i18nAlt]; });
  document.querySelectorAll('[data-i18n-aria]').forEach(element => { element.setAttribute('aria-label', content[element.dataset.i18nAria]); });
  languageLinks.forEach(link => {
    link.href = new URL(`${link.dataset.language}/`, runtimeRoot);
    if (link.dataset.language === language) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  roster.querySelectorAll('button').forEach((button, index) => {
    button.querySelector('strong').textContent = HIRES[index][language].name;
    button.setAttribute('aria-pressed', String(index === selectedHire));
  });
  updateProfile();
  document.querySelectorAll('.experiment .table-scroll').forEach((table, index) => {
    table.scrollLeft = (tableScroll[index] || 0) * Math.max(0, table.scrollWidth - table.clientWidth);
  });
  document.querySelector('#copy-status').textContent = copyState ? content[copyState] : '';
  if (persist) {
    try { localStorage.setItem('qh-language', language); } catch { /* Optional preference storage. */ }
  }
  const url = new URL(`${language}/`, runtimeRoot);
  url.search = location.search;
  url.searchParams.delete('lang');
  url.hash = location.hash;
  history.replaceState(null, '', url);
}

languageLinks.forEach(link => link.addEventListener('click', event => {
  if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();
  setLanguage(link.dataset.language, true);
}));
window.addEventListener('popstate', () => setLanguage(initialLanguage()));
updateChart();
setLanguage(initialLanguage());

document.querySelector('#copy').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText('npx skills add SoonGwan/questionable-hires');
    copyState = 'copied';
  } catch {
    copyState = 'copyFailed';
  }
  document.querySelector('#copy-status').textContent = COPY[language][copyState];
});

if (!reducedMotion.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: .08 });
  document.querySelectorAll('.section-heading, .principles > h2, .principle-grid article, .evidence-link').forEach(element => {
    element.classList.add('reveal');
    observer.observe(element);
  });
  document.querySelector('.hero-title').animate([
    { opacity: 0, transform: 'translateY(20px)' },
    { opacity: 1, transform: 'translateY(0)' }
  ], { duration: 850, easing: 'cubic-bezier(.22,1,.36,1)' });
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      document.querySelectorAll('.reveal').forEach(element => element.classList.add('visible'));
      document.getAnimations().forEach(animation => animation.finish());
      observer.disconnect();
    }
  });
}
