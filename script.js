// Salaama Eats Ltd — site interactions

document.addEventListener('DOMContentLoaded', () => {
  // Preloader
  const preloader = document.getElementById('preloader');
  window.addEventListener('load', () => {
    setTimeout(() => preloader && preloader.classList.add('done'), 300);
  });
  // Fallback in case 'load' already fired
  setTimeout(() => preloader && preloader.classList.add('done'), 1800);

  // Sticky header + floating CTA visibility
  const header = document.getElementById('siteHeader');
  const fab = document.querySelector('.fab');
  const hero = document.querySelector('.hero');
  const onScroll = () => {
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
    if (fab && hero) {
      const pastHero = window.scrollY > hero.offsetHeight - 120;
      fab.classList.toggle('is-visible', pastHero);
    }
  };
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav toggle
  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('mainNav');
  navToggle.addEventListener('click', () => {
    const isOpen = mainNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
  mainNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mainNav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  // Scroll reveal
  const revealEls = document.querySelectorAll('[data-reveal]');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => io.observe(el));

  // Menu tabs
  const tabBtns = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.menu-panel');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const target = document.querySelector(`.menu-panel[data-panel="${btn.dataset.tab}"]`);
      if (target) target.classList.add('active');
    });
  });

  // Signature dishes: continuous auto-scroll is pure CSS (see .slider-track
  // in style.css) — it doubles the cards and animates translateX(-50%) in
  // an infinite loop, pausing on hover/focus via :hover/:focus-within.

  // Subtle arch photo tilt on mouse move
  const heroArch = document.querySelector('.heritage-media');
  const archFrame = heroArch ? heroArch.querySelector('.arch-frame') : null;
  if (heroArch && archFrame && window.matchMedia('(hover: hover)').matches) {
    heroArch.addEventListener('mousemove', (e) => {
      const rect = heroArch.getBoundingClientRect();
      const px = (e.clientX - rect.left) / rect.width - 0.5;
      const py = (e.clientY - rect.top) / rect.height - 0.5;
      archFrame.style.transform = `rotateY(${px * 8}deg) rotateX(${-py * 8}deg)`;
    });
    heroArch.addEventListener('mouseleave', () => {
      archFrame.style.transform = 'rotateY(0deg) rotateX(0deg)';
    });
  }

  // Reservation form (front-end only — no backend wired up)
  const form = document.getElementById('reserveForm');
  const status = document.getElementById('formStatus');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    status.textContent = 'Thank you! Your reservation request has been received — we\'ll confirm by phone or email shortly.';
    form.reset();
  });

  // Footer year
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
