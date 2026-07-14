(() => {
  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const selector = button.getAttribute('data-copy-target');
      const target = selector ? document.querySelector(selector) : null;
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
