const navToggle = document.querySelector('.nav-toggle');
const siteNav = document.querySelector('.site-nav');

if (navToggle && siteNav) {
  document.body.classList.add('navigation-ready');
  const isEnglish = document.documentElement.lang === 'en';
  const setToggle = (isOpen) => {
    const label = isEnglish ? (isOpen ? 'Close navigation' : 'Open navigation') : (isOpen ? '关闭导航' : '打开导航');
    navToggle.setAttribute('aria-expanded', String(isOpen));
    navToggle.setAttribute('aria-label', label);
    navToggle.textContent = isOpen ? '×' : '☰';
    navToggle.title = label;
  };
  navToggle.addEventListener('click', () => {
    const isOpen = siteNav.classList.toggle('open');
    setToggle(isOpen);
  });

  siteNav.addEventListener('click', () => {
    siteNav.classList.remove('open');
    setToggle(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && siteNav.classList.contains('open')) {
      siteNav.classList.remove('open');
      setToggle(false);
      navToggle.focus();
    }
  });
}

const revealTargets = document.querySelectorAll(
  '.section-heading, .capability-step, .architecture-copy, .architecture-figure, .sandbox-visual, .sandbox-copy, .example-card, .ecosystem-grid article, .edition-table'
);

if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.body.classList.add('reveal-ready');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px' });
  revealTargets.forEach((target) => observer.observe(target));
} else {
  revealTargets.forEach((target) => target.classList.add('is-visible'));
}
