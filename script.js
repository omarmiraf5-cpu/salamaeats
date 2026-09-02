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

  // Signature dishes marquee. Driven by scrollLeft rather than a CSS
  // transform: transforming the ~3000px track makes iOS Safari promote it to
  // one giant composited layer, which it discards under memory pressure —
  // the slider goes blank after a while. Advancing a real scroll container
  // keeps Safari on its ordinary scrolling path, and lets people swipe it.
  const dishTrack = document.getElementById('dishTrack');
  if (dishTrack && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const SPEED = 0.35;           // px per frame, ~21px/s at 60fps
    let pos = 0;                  // kept as a float; scrollLeft alone would round away sub-pixel steps
    let paused = false;
    let userScrolling = null;

    // The second half of the track duplicates the first, so snapping back by
    // exactly one set's width is invisible. Measure that from the card
    // positions rather than using scrollWidth/2 — the track's padding and
    // gaps make those differ by a pixel, which shows up as a visible jump
    // and drifts further out of register on every loop.
    const cards = dishTrack.children;
    const halfWidth = () =>
      cards.length >= 5 ? cards[cards.length / 2].offsetLeft - cards[0].offsetLeft : 0;

    function frame() {
      const half = halfWidth();
      if (!paused && half > 0) {
        pos += SPEED;
        if (pos >= half) pos -= half;
        dishTrack.scrollLeft = pos;
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);

    // Let go of the reins while the user is dragging the row themselves,
    // then pick up from wherever they left it.
    const resume = () => {
      clearTimeout(userScrolling);
      userScrolling = setTimeout(() => {
        const half = halfWidth();
        pos = half > 0 ? dishTrack.scrollLeft % half : dishTrack.scrollLeft;
        paused = false;
      }, 1200);
    };
    dishTrack.addEventListener('touchstart', () => { paused = true; clearTimeout(userScrolling); }, { passive: true });
    dishTrack.addEventListener('touchend', resume, { passive: true });
    dishTrack.addEventListener('wheel', () => { paused = true; resume(); }, { passive: true });

    // Pause on hover, but only where hovering is a real thing — on touch,
    // iOS latches :hover and would never release it.
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      dishTrack.addEventListener('mouseenter', () => { paused = true; });
      dishTrack.addEventListener('mouseleave', () => {
        const half = halfWidth();
        pos = half > 0 ? dishTrack.scrollLeft % half : dishTrack.scrollLeft;
        paused = false;
      });
    }
  }

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
