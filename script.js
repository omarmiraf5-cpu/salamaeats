// Salama Eats Ltd — site interactions

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

  // Testimonials carousel
  const testis = document.querySelectorAll('.testi');
  const dotsWrap = document.getElementById('testiDots');
  let testiIndex = 0;
  testis.forEach((_, i) => {
    const dot = document.createElement('button');
    if (i === 0) dot.classList.add('active');
    dot.setAttribute('aria-label', `Show testimonial ${i + 1}`);
    dot.addEventListener('click', () => showTesti(i));
    dotsWrap.appendChild(dot);
  });
  function showTesti(i) {
    testis.forEach(t => t.classList.remove('active'));
    dotsWrap.querySelectorAll('button').forEach(d => d.classList.remove('active'));
    testis[i].classList.add('active');
    dotsWrap.children[i].classList.add('active');
    testiIndex = i;
  }
  setInterval(() => {
    showTesti((testiIndex + 1) % testis.length);
  }, 6000);

  // Signature dishes slider
  const track = document.getElementById('dishTrack');
  if (track) {
    const cards = Array.from(track.children);
    const prevBtn = document.getElementById('dishPrev');
    const nextBtn = document.getElementById('dishNext');
    const dotsWrap = document.getElementById('dishDots');
    let autoplayTimer = null;

    cards.forEach((_, i) => {
      const dot = document.createElement('button');
      if (i === 0) dot.classList.add('active');
      dot.setAttribute('aria-label', `Go to dish ${i + 1}`);
      dot.addEventListener('click', () => scrollToCard(i));
      dotsWrap.appendChild(dot);
    });

    function cardStep() {
      const style = getComputedStyle(track);
      return cards[0].getBoundingClientRect().width + parseFloat(style.columnGap || style.gap || 28);
    }
    function scrollToCard(i) {
      track.scrollTo({ left: cards[i].offsetLeft - track.offsetLeft, behavior: 'smooth' });
    }
    function nearestIndex() {
      const pos = track.scrollLeft + track.offsetLeft;
      let closest = 0;
      let min = Infinity;
      cards.forEach((c, i) => {
        const d = Math.abs(c.offsetLeft - pos);
        if (d < min) { min = d; closest = i; }
      });
      return closest;
    }
    function updateDots() {
      const idx = nearestIndex();
      dotsWrap.querySelectorAll('button').forEach((d, i) => d.classList.toggle('active', i === idx));
      return idx;
    }
    prevBtn.addEventListener('click', () => { track.scrollBy({ left: -cardStep(), behavior: 'smooth' }); stopAutoplay(); });
    nextBtn.addEventListener('click', () => { track.scrollBy({ left: cardStep(), behavior: 'smooth' }); stopAutoplay(); });

    let scrollTicking = false;
    track.addEventListener('scroll', () => {
      if (!scrollTicking) {
        requestAnimationFrame(() => { updateDots(); scrollTicking = false; });
        scrollTicking = true;
      }
    }, { passive: true });

    // Pointer drag-to-scroll
    let isDown = false, startX = 0, startScroll = 0, moved = false;
    track.addEventListener('pointerdown', (e) => {
      isDown = true; moved = false;
      startX = e.clientX; startScroll = track.scrollLeft;
      track.classList.add('dragging');
      stopAutoplay();
    });
    track.addEventListener('pointermove', (e) => {
      if (!isDown) return;
      const dx = e.clientX - startX;
      if (Math.abs(dx) > 4) moved = true;
      track.scrollLeft = startScroll - dx;
    });
    function endDrag() {
      if (!isDown) return;
      isDown = false;
      track.classList.remove('dragging');
      startAutoplay();
    }
    track.addEventListener('pointerup', endDrag);
    track.addEventListener('pointerleave', endDrag);
    track.addEventListener('click', (e) => { if (moved) e.preventDefault(); }, true);

    function startAutoplay() {
      stopAutoplay();
      autoplayTimer = setInterval(() => {
        const idx = nearestIndex();
        const next = (idx + 1) % cards.length;
        if (next === 0) track.scrollTo({ left: 0, behavior: 'smooth' });
        else scrollToCard(next);
      }, 4500);
    }
    function stopAutoplay() {
      if (autoplayTimer) clearInterval(autoplayTimer);
    }
    track.addEventListener('mouseenter', stopAutoplay);
    track.addEventListener('mouseleave', startAutoplay);
    startAutoplay();
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
