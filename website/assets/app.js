(() => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  const header = document.querySelector('[data-site-header]');
  let lastFocused = null;

  const navLinks = nav ? Array.from(nav.querySelectorAll('a')) : [];

  function setNavigation(open, { returnFocus = false } = {}) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.sr-only').textContent = open ? 'Close navigation' : 'Open navigation';
    nav.dataset.open = String(open);
    document.body.classList.toggle('nav-open', open);

    if (open) {
      lastFocused = document.activeElement;
      window.requestAnimationFrame(() => navLinks[0]?.focus());
    } else if (returnFocus && lastFocused instanceof HTMLElement) {
      lastFocused.focus();
    }
  }

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    setNavigation(open, { returnFocus: !open });
  });

  navLinks.forEach((link) => link.addEventListener('click', () => setNavigation(false)));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      setNavigation(false, { returnFocus: true });
    }
  });

  document.addEventListener('pointerdown', (event) => {
    if (!header || toggle?.getAttribute('aria-expanded') !== 'true') return;
    if (!header.contains(event.target)) setNavigation(false, { returnFocus: true });
  });

  const desktop = window.matchMedia('(min-width: 901px)');
  desktop.addEventListener?.('change', (event) => {
    if (event.matches) setNavigation(false);
  });

  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.querySelector(button.getAttribute('data-copy-target'));
      if (!target) return;
      const original = button.textContent;
      try {
        await navigator.clipboard.writeText(target.textContent || '');
        button.textContent = 'Copied';
      } catch {
        button.textContent = 'Copy unavailable';
      }
      window.setTimeout(() => { button.textContent = original; }, 1400);
    });
  });
})();
