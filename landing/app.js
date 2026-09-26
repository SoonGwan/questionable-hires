const languageButtons = document.querySelectorAll('[data-language]');
const roster = document.querySelector('.roster');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
// Bounds in the approved 1536 × 1024 cast artwork; keep props inside each portrait.
const portraitBounds = [
  [60, 170, 360], [420, 260, 320], [735, 190, 350], [1120, 190, 380],
  [45, 570, 430], [495, 640, 300], [825, 615, 300], [1150, 595, 380]
];
const validLanguage = value => Object.hasOwn(COPY, value);
let selectedHire = 0;
let language = 'ko';
let copyState = null;

function initialLanguage() {
  const requested = new URL(location.href).searchParams.get('lang');
  if (validLanguage(requested)) return requested;
  try {
    const saved = localStorage.getItem('qh-language');
    if (validLanguage(saved)) return saved;
  } catch { /* Language selection works even when storage is unavailable. */ }
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

HIRES.forEach((hire, index) => {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'hire';
  button.innerHTML = `<span class="number">${String(index + 1).padStart(2, '0')}</span><span><strong></strong><span class="codename">${hire.id}</span></span><span class="arrow" aria-hidden="true">↗</span>`;
  button.addEventListener('click', () => {
    selectedHire = index;
    roster.querySelectorAll('button').forEach((item, i) => item.setAttribute('aria-pressed', String(i === index)));
    updateProfile(true);
  });
  roster.append(button);
});

function setLanguage(next, persist = false) {
  if (!validLanguage(next)) return;
  language = next;
  const content = COPY[language];
  document.documentElement.lang = language;
  document.title = content.title;
  document.querySelector('meta[name="description"]').content = content.description;
  document.querySelectorAll('[data-i18n]').forEach(element => { element.textContent = content[element.dataset.i18n]; });
  document.querySelectorAll('[data-i18n-alt]').forEach(element => { element.alt = content[element.dataset.i18nAlt]; });
  document.querySelectorAll('[data-i18n-aria]').forEach(element => { element.setAttribute('aria-label', content[element.dataset.i18nAria]); });
  languageButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
  roster.querySelectorAll('button').forEach((button, index) => {
    button.querySelector('strong').textContent = HIRES[index][language].name;
    button.setAttribute('aria-pressed', String(index === selectedHire));
  });
  updateProfile();
  document.querySelector('#copy-status').textContent = copyState ? content[copyState] : '';
  if (persist) {
    try { localStorage.setItem('qh-language', language); } catch { /* Optional preference storage. */ }
    const url = new URL(location.href);
    url.searchParams.set('lang', language);
    history.replaceState(null, '', url);
  }
}

languageButtons.forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.language, true)));
window.addEventListener('popstate', () => setLanguage(initialLanguage()));
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
