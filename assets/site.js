(function () {
  'use strict';
  var G = window.GEGEVENS || {};
  var doc = document, html = doc.documentElement;
  var rustig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function alle(s, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(s)); }
  function schoon(v) { return (v == null ? '' : String(v)).trim(); }
  function veilig(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var tel = schoon(G.telefoon), wa = schoon(G.whatsapp).replace(/\D/g, ''), mail = schoon(G.email);
  var telHref = tel ? 'tel:' + tel.replace(/[^\d+]/g, '') : '';
  var waHref = wa ? 'https://wa.me/' + wa : '';

  /* 1. Gegevens invullen: alles zonder waarde blijft verborgen */
  var waarden = { telefoon: tel, whatsapp: wa ? (tel || '+' + wa) : '', email: mail, adres: schoon(G.adres), kvk: schoon(G.kvk) };
  var links = { telefoon: telHref, whatsapp: waHref, email: mail ? 'mailto:' + mail : '' };
  alle('[data-g]').forEach(function (el) {
    var k = el.getAttribute('data-g'), v = waarden[k];
    if (!v) return;
    var doel = el.querySelector('[data-g-tekst]') || el;
    if (!el.hasAttribute('data-g-vast')) doel.textContent = (el.getAttribute('data-g-voor') || '') + v;
    if (el.tagName === 'A' && links[k]) {
      el.href = links[k];
      if (k === 'whatsapp') { el.target = '_blank'; el.rel = 'noopener'; }
    }
    el.hidden = false;
  });
  if (tel || wa) html.classList.add('heeft-balk');
  alle('[data-jaar]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* 2. Reviews */
  var reviews = (G.reviews || []).filter(function (r) { return r && schoon(r.tekst) && schoon(r.naam); });
  alle('[data-reviews]').forEach(function (blok) {
    if (!reviews.length) return;
    blok.querySelector('[data-reviews-lijst]').innerHTML = reviews.map(function (r) {
      return '<figure class="review"><blockquote>' + veilig(schoon(r.tekst)) + '</blockquote><footer><strong>' + veilig(schoon(r.naam)) + '</strong>' +
        (schoon(r.plaats) ? ', ' + veilig(schoon(r.plaats)) : '') + '</footer></figure>';
    }).join('');
    blok.hidden = false;
  });

  /* 3. Bedrijfsgegevens voor zoekmachines */
  try {
    var ld = { '@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness', name: 'Oldenburger Stucadoors',
      slogan: 'Strak in afwerking, sterk in detail', url: location.origin + '/',
      description: 'Stucwerk, afbouw, betonlook, gietvloeren en verfspuiten in Drenthe en omgeving.',
      areaServed: { '@type': 'AdministrativeArea', name: 'Drenthe' }, founder: { '@type': 'Person', name: 'Frank Oldenburger' } };
    if (tel) ld.telephone = tel;
    if (mail) ld.email = mail;
    if (waarden.adres) ld.address = waarden.adres;
    var s = doc.createElement('script'); s.type = 'application/ld+json'; s.textContent = JSON.stringify(ld); doc.head.appendChild(s);
  } catch (e) {}

  /* 4. Kop: schaduw bij scrollen, menu op telefoon */
  var kop = doc.querySelector('.kop');
  function scrolt() { if (kop) kop.classList.toggle('is-los', window.scrollY > 8); }
  window.addEventListener('scroll', scrolt, { passive: true }); scrolt();

  var menu = doc.getElementById('menu'), menuKnop = doc.querySelector('.kop__menu');
  function zetMenu(open) {
    if (!menu) return;
    menu.hidden = !open; html.classList.toggle('menu-open', open);
    menuKnop.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) menu.querySelector('.menu__sluit').focus(); else menuKnop.focus();
  }
  if (menu && menuKnop) {
    menuKnop.addEventListener('click', function () { zetMenu(true); });
    menu.querySelector('.menu__sluit').addEventListener('click', function () { zetMenu(false); });
    menu.addEventListener('keydown', function (e) { if (e.key === 'Escape') zetMenu(false); });
    alle('a', menu).forEach(function (a) { a.addEventListener('click', function () { menu.hidden = true; html.classList.remove('menu-open'); }); });
  }

  /* 5. Video's: alleen afspelen als ze in beeld zijn */
  var videos = alle('video[data-auto]');
  var zuinig = navigator.connection && navigator.connection.saveData;
  if (rustig || zuinig || !('IntersectionObserver' in window)) {
    videos.forEach(function (v) { v.controls = true; });
  } else {
    var kijker = new IntersectionObserver(function (items) {
      items.forEach(function (it) {
        var v = it.target;
        if (it.isIntersecting) { v.muted = true; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.35 });
    videos.forEach(function (v) { kijker.observe(v); });
  }

  /* 6. Hero: overige achtergrondfoto's pas laden als de pagina klaar is */
  function laadDia() { alle('.hero__beeld img[data-src]').forEach(function (i) { i.src = i.getAttribute('data-src'); i.removeAttribute('data-src'); }); }
  if (doc.readyState === 'complete') laadDia(); else window.addEventListener('load', laadDia);

  /* 7. Projecten: filter en vergroting */
  var galerij = doc.querySelector('.galerij');
  if (galerij) {
    var werken = alle('.werk', galerij), filters = alle('.filters button'), leeg = doc.querySelector('.leeg');
    var zichtbaar = werken.slice();
    filters.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        zichtbaar = werken.filter(function (w) { var ok = f === 'alles' || w.getAttribute('data-cat') === f; w.hidden = !ok; return ok; });
        if (leeg) leeg.hidden = zichtbaar.length > 0;
      });
    });

    var bak = doc.querySelector('.lichtbak');
    if (bak && bak.showModal) {
      var podium = bak.querySelector('.lichtbak__podium'), titel = bak.querySelector('.lichtbak__titel'), teller = bak.querySelector('.lichtbak__teller');
      var nu = 0;
      function toon(i) {
        nu = (i + zichtbaar.length) % zichtbaar.length;
        var w = zichtbaar[nu], vid = w.getAttribute('data-video'), alt = w.querySelector('img').alt;
        podium.innerHTML = vid
          ? '<video src="' + vid + '" poster="' + w.getAttribute('data-groot') + '" controls autoplay muted loop playsinline aria-label="' + veilig(alt) + '"></video>'
          : '<img src="' + w.getAttribute('data-groot') + '" alt="' + veilig(alt) + '">';
        titel.textContent = w.querySelector('strong').textContent;
        teller.textContent = (nu + 1) + ' / ' + zichtbaar.length;
      }
      werken.forEach(function (w) { w.addEventListener('click', function () { toon(zichtbaar.indexOf(w)); bak.showModal(); }); });
      bak.querySelector('[data-vorige]').addEventListener('click', function () { toon(nu - 1); });
      bak.querySelector('[data-volgende]').addEventListener('click', function () { toon(nu + 1); });
      bak.querySelector('[data-sluit]').addEventListener('click', function () { bak.close(); });
      bak.addEventListener('close', function () { podium.innerHTML = ''; });
      bak.addEventListener('click', function (e) { if (e.target === podium || e.target === bak) bak.close(); });
      bak.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') toon(nu - 1); if (e.key === 'ArrowRight') toon(nu + 1); });
      var x0 = null;
      podium.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      podium.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) toon(nu + (dx < 0 ? 1 : -1)); x0 = null; });
    }
  }

  /* 8. Offerteformulier */
  var form = doc.querySelector('.formulier');
  if (form) {
    var melding = form.querySelector('.melding'), knop = form.querySelector('button[type=submit]');
    var eind = schoon(G.formulier);
    var soort = new URLSearchParams(location.search).get('soort');
    if (soort) alle('option', form).forEach(function (o) { if (o.value.toLowerCase() === soort.toLowerCase()) o.selected = true; });

    function meld(tekst, goed) { melding.textContent = tekst; melding.className = 'melding ' + (goed ? 'melding--goed' : 'melding--fout'); melding.hidden = false; melding.focus(); }
    function fout(veld, tekst) {
      var el = form.elements[veld], f = form.querySelector('[data-fout="' + veld + '"]');
      el.setAttribute('aria-invalid', tekst ? 'true' : 'false'); f.textContent = tekst || ''; f.hidden = !tekst;
      return !tekst;
    }
    function tekstVan(d) {
      return ['Offerteaanvraag via de website', '', 'Naam: ' + d.naam, 'Plaats: ' + d.plaats, 'E-mail: ' + d.email, 'Telefoon: ' + d.telefoon,
        'Soort werk: ' + d.soort, 'Oppervlakte (m2): ' + d.oppervlakte, '', d.bericht].join('\n');
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault(); melding.hidden = true;
      var d = {}; ['naam', 'plaats', 'email', 'telefoon', 'soort', 'oppervlakte', 'bericht'].forEach(function (k) { d[k] = schoon(form.elements[k].value); });
      var ok = true;
      ok = fout('naam', d.naam ? '' : 'Vul je naam in.') && ok;
      var mailOk = !d.email || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email);
      ok = fout('email', !mailOk ? 'Dit e-mailadres klopt niet.' : (!d.email && !d.telefoon ? 'Vul een e-mailadres of telefoonnummer in.' : '')) && ok;
      ok = fout('bericht', d.bericht ? '' : 'Vertel kort wat je wilt laten doen.') && ok;
      if (!ok) { var eerste = form.querySelector('[aria-invalid=true]'); if (eerste) eerste.focus(); return; }
      if (form.elements.website.value) return; /* spamval */

      if (eind) {
        knop.disabled = true; var oud = knop.textContent; knop.textContent = 'Bezig met versturen…';
        fetch(eind, { method: 'POST', headers: { Accept: 'application/json', 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); meld('Bedankt, je aanvraag is verstuurd. Frank neemt zo snel mogelijk contact met je op.', true); })
          .catch(function () { meld('Versturen is niet gelukt. Probeer het opnieuw' + (tel ? ' of bel ' + tel : '') + '.', false); })
          .then(function () { knop.disabled = false; knop.textContent = oud; });
      } else if (mail) {
        location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent('Offerteaanvraag ' + d.soort + ' - ' + d.naam) + '&body=' + encodeURIComponent(tekstVan(d));
        meld('Je e-mailprogramma opent met je aanvraag. Klik daar op versturen om hem af te ronden.', true);
      } else if (wa) {
        window.open(waHref + '?text=' + encodeURIComponent(tekstVan(d)), '_blank', 'noopener');
        meld('WhatsApp opent met je aanvraag. Verstuur het bericht daar om hem af te ronden.', true);
      } else {
        meld('Het formulier is nog niet gekoppeld, je aanvraag is niet verstuurd.', false);
      }
    });
  }
})();
