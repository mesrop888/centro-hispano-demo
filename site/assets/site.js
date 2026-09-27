document.documentElement.classList.remove('no-js');
const LANG = (document.documentElement.lang || 'en').slice(0, 2);
const T = {
  en: { pause: 'Pause the photos', play: 'Play the photos', one: 'One field needs attention.', many: (n) => `${n} fields need attention.`, subj: 'Question from the website', ok: 'Your email app should open with the message ready. If it does not, write to info@centrohispano.am.', place: 'Placement test', open: 'Open menu', close: 'Close menu' },
  es: { pause: 'Pausar las fotos', play: 'Reanudar las fotos', one: 'Hay un campo por revisar.', many: (n) => `Hay ${n} campos por revisar.`, subj: 'Consulta desde la web', ok: 'Tu aplicación de correo debería abrirse con el mensaje listo. Si no, escribe a info@centrohispano.am.', place: 'Prueba de nivel', open: 'Abrir menú', close: 'Cerrar menú' },
  hy: { pause: 'Կանգնեցնել լուսանկարները', play: 'Շարունակել լուսանկարները', one: 'Մեկ դաշտ պետք է ուղղել։', many: (n) => `${n} դաշտ պետք է ուղղել։`, subj: 'Հարց կայքից', ok: 'Ձեր էլ․ փոստի հավելվածը կբացվի պատրաստ հաղորդագրությամբ։ Եթե ոչ, գրեք info@centrohispano.am հասցեին։', place: 'Մակարդակի թեստ', open: 'Բացել մենյուն', close: 'Փակել մենյուն' },
}[LANG] || {};

// Mobile menu
const menuBtn = document.querySelector('.menu-btn');
const nav = document.getElementById('nav');
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? T.close : T.open);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.setAttribute('aria-label', T.open);
      menuBtn.focus();
    }
  });
}

// Photo ribbons: duplicate each strip once so the loop is seamless
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const ribbons = document.querySelector('.ribbons');
if (ribbons && !reduce) {
  ribbons.querySelectorAll('.ribbon').forEach((r) => {
    [...r.children].forEach((li) => {
      const copy = li.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true');
      copy.querySelectorAll('img').forEach((img) => { img.alt = ''; img.loading = 'lazy'; });
      r.appendChild(copy);
    });
    r.classList.add('is-moving');
  });
  const toggle = ribbons.querySelector('.ribbons-ctl button');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const paused = ribbons.classList.toggle('is-paused');
      toggle.textContent = paused ? T.play : T.pause;
      toggle.setAttribute('aria-pressed', String(paused));
    });
  }
}

// Fiesta wall lightbox: opens out of the clicked photo, slides between photos
const wall = document.querySelector('.wall');
const lb = document.getElementById('lightbox');
if (wall && lb && typeof lb.showModal === 'function') {
  const items = [...wall.querySelectorAll('button')];
  const img = lb.querySelector('img');
  const cap = lb.querySelector('figcaption');
  let i = 0;
  const show = (n, dir) => {
    i = (n + items.length) % items.length;
    const b = items[i];
    img.src = b.dataset.full;
    img.alt = b.querySelector('img').alt;
    cap.textContent = `${b.dataset.cap} · ${i + 1} / ${items.length}`;
    if (dir) {
      img.classList.remove('slide-next', 'slide-prev');
      void img.offsetWidth;
      img.classList.add(dir > 0 ? 'slide-next' : 'slide-prev');
    }
  };
  const open = (n) => {
    const r = items[n].getBoundingClientRect();
    lb.style.setProperty('--fx', `${Math.round(r.left + r.width / 2 - innerWidth / 2)}px`);
    lb.style.setProperty('--fy', `${Math.round(r.top + r.height / 2 - innerHeight / 2)}px`);
    lb.style.setProperty('--fs', Math.max(0.15, Math.min(0.6, r.width / Math.min(1100, innerWidth))).toFixed(2));
    show(n);
    lb.showModal();
  };
  const close = () => {
    if (reduce || !lb.open) { lb.close(); return; }
    lb.classList.add('is-closing');
    setTimeout(() => { lb.classList.remove('is-closing'); lb.close(); }, 190);
  };
  items.forEach((b, n) => b.addEventListener('click', () => open(n)));
  lb.querySelector('.lb-prev').addEventListener('click', () => show(i - 1, -1));
  lb.querySelector('.lb-next').addEventListener('click', () => show(i + 1, 1));
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.addEventListener('cancel', (e) => { e.preventDefault(); close(); });
  lb.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') show(i - 1, -1);
    if (e.key === 'ArrowRight') show(i + 1, 1);
  });
  lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
  lb.addEventListener('close', () => items[i].focus());
}

// The price staircase grows once it scrolls into view
document.querySelectorAll('.ladder').forEach((ladder) => {
  ladder.querySelectorAll('li').forEach((li, n) => li.style.setProperty('--i', n));
  if (reduce || !('IntersectionObserver' in window)) return;
  if (ladder.getBoundingClientRect().top < innerHeight * 0.9) return; // already visible: leave it standing
  ladder.classList.add('is-armed');
  const io = new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return;
    ladder.classList.add('is-in');
    ladder.classList.remove('is-armed');
    io.disconnect();
  }, { threshold: 0.3 });
  io.observe(ladder);
});

// Ribbons stop animating while offscreen
if (ribbons && !reduce && 'IntersectionObserver' in window) {
  new IntersectionObserver(([e]) => ribbons.classList.toggle('is-offscreen', !e.isIntersecting)).observe(ribbons);
}

// Contact form: no backend, so compose an email to the Center
const form = document.querySelector('#contact-form');
if (form) {
  const params = new URLSearchParams(location.search);
  if (params.get('subject')) form.querySelector('[name=subject]').value = params.get('subject') === 'Placement test' ? T.place : params.get('subject');
  const status = form.querySelector('.form-status');
  const check = (field) => {
    const input = field.querySelector('input, textarea');
    const ok = input.checkValidity();
    field.classList.toggle('is-invalid', !ok);
    input.setAttribute('aria-invalid', String(!ok));
    return ok;
  };
  form.querySelectorAll('.field').forEach((f) => {
    f.querySelector('input, textarea').addEventListener('blur', () => { if (f.classList.contains('is-invalid')) check(f); });
  });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const bad = [...form.querySelectorAll('.field')].filter((f) => !check(f));
    if (bad.length) {
      status.classList.remove('is-ok');
      status.textContent = bad.length === 1 ? T.one : T.many(bad.length);
      bad[0].querySelector('input, textarea').focus();
      return;
    }
    const d = new FormData(form);
    const subject = d.get('subject') || T.subj;
    const body = `${d.get('message')}\n\n${d.get('name')}\n${d.get('email')}`;
    window.location.href = `mailto:info@centrohispano.am?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    status.classList.add('is-ok');
    status.textContent = T.ok;
  });
}

// Justified fiesta wall: each tile takes its photo's real proportions once known
document.querySelectorAll('.wall button').forEach((b) => {
  const im = b.querySelector('img');
  const set = () => { if (im.naturalWidth) b.style.setProperty('--ar', Math.min(2, Math.max(0.6, im.naturalWidth / im.naturalHeight)).toFixed(3)); };
  if (im.complete) set(); else im.addEventListener('load', set, { once: true });
});
