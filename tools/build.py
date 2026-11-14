#!/usr/bin/env python3
"""Bouwt de pagina's van oldenburger-stucadoors.

Gebruik:  python3 tools/build.py
Schrijft de .html-bestanden in de hoofdmap en maakt kleinere fotoversies in assets/.
Teksten en volgorde van de pagina's staan in dit bestand; opmaak in assets/site.css,
gedrag in assets/site.js, contactgegevens in gegevens.js.
"""
import os, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'assets')
SITE_URL = ''   # bijvoorbeeld 'https://www.oldenburgerstucadoors.nl' zodra het domein bekend is
VERSIE = '3'    # ophogen bij wijzigingen in site.css / site.js
P = ''          # voorvoegsel voor links (alleen de 404-pagina gebruikt '/')

LOGO = open(os.path.join(ROOT, 'tools', 'logo.svg'), encoding='utf-8').read().replace('<svg width="260" height="46"', '<svg')
MERK = '<svg viewBox="0 0 150 150" aria-hidden="true"><circle cx="75" cy="75" r="70" fill="none" stroke="currentColor" stroke-width="5"/><g fill="none" stroke="currentColor" stroke-width="5"><path d="M50 38H104V52H66V68H96V82H66V114H50Z"/><path d="M58 114V45H104"/><path d="M58 75H96"/></g></svg>'
I_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1Z"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 20l1.4-4.2A8 8 0 1 1 8.6 19L4 20Z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6.5 12 13l8.5-6.5"/></svg>'
I_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
I_HUIS = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 15 16 5l12 10"/><path d="M7 13v13h18V13"/><path d="M13 26v-8h6v8"/></svg>'
I_MENS = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="16" cy="11" r="5"/><path d="M6 27c1-6 5-9 10-9s9 3 10 9"/></svg>'
I_BLAD = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 4h12l5 5v19H8Z"/><path d="M20 4v5h5"/><path d="m12 18 3 3 6-7"/></svg>'

NAV = [('diensten', 'Diensten'), ('werkwijze', 'Werkwijze'), ('projecten', 'Projecten'), ('over-frank', 'Over Frank')]

# ---------- beeld ----------
_dims = {}
def dims(bestand):
    if bestand not in _dims:
        with Image.open(os.path.join(A, bestand)) as im:
            _dims[bestand] = im.size
    return _dims[bestand]

def klein(naam):
    """Maakt (eenmalig) een versie van 800 px breed en geeft de bestandsnaam terug, of None."""
    w, h = dims(naam + '.jpg')
    if w < 1000:
        return None
    doel = os.path.join(A, naam + '-800.jpg')
    if not os.path.exists(doel):
        with Image.open(os.path.join(A, naam + '.jpg')) as im:
            im = im.convert('RGB'); im.thumbnail((800, 4000)); im.save(doel, quality=78, optimize=True, progressive=True)
    return naam + '-800.jpg'

def e(s): return html.escape(s, quote=True)

def img(naam, alt, sizes='100vw', cls='', lui=True, extra=''):
    w, h = dims(naam + '.jpg')
    k = klein(naam)
    srcset = f' srcset="{P}assets/{k} 800w, {P}assets/{naam}.jpg {w}w" sizes="{sizes}"' if k else ''
    c = f' class="{cls}"' if cls else ''
    l = ' loading="lazy" decoding="async"' if lui else ' fetchpriority="high"'
    return f'<img{c} src="{P}assets/{naam}.jpg"{srcset} width="{w}" height="{h}" alt="{e(alt)}"{l}{extra}>'

def video(naam, label, cls=''):
    w, h = dims(naam + '-poster.jpg')
    c = f' class="{cls}"' if cls else ''
    return (f'<video{c} data-auto muted loop playsinline preload="none" width="{w}" height="{h}" poster="{P}assets/{naam}-poster.jpg" '
            f'aria-label="{e(label)}"><source src="{P}assets/{naam}.mp4" type="video/mp4"></video>')

# ---------- vaste onderdelen ----------
def cur(s, actief):
    return ' aria-current="page"' if s == actief else ''

def kop(actief):
    nav = ''.join(f'<a href="{P}{s}"{cur(s, actief)}>{t}</a>' for s, t in NAV)
    thuis = P or './'
    menu = f'<a href="{thuis}"{cur("home", actief)}>Home</a>' + ''.join(
        f'<a href="{P}{s}"{cur(s, actief)}>{t}</a>' for s, t in NAV + [('contact', 'Contact')])
    return f'''<a class="skip" href="#inhoud">Naar de inhoud</a>
<header class="kop">
<div class="wrap kop__in">
<a class="kop__logo" href="{P or "./"}" aria-label="Oldenburger Stucadoors, naar de homepage">{LOGO}</a>
<nav class="kop__nav" aria-label="Hoofdmenu">{nav}</nav>
<a class="kop__tel" data-g="telefoon" hidden>{I_TEL}<span data-g-tekst></span></a>
<a class="knop knop--klein kop__cta" href="{P}contact"{cur("contact", actief)}>Offerte aanvragen</a>
<button class="kop__menu" type="button" aria-expanded="false" aria-controls="menu"><i aria-hidden="true"></i>Menu</button>
</div>
</header>
<div class="menu" id="menu" hidden>
<div class="menu__top"><span>Oldenburger Stucadoors</span><button class="menu__sluit" type="button">Sluiten</button></div>
<nav aria-label="Menu">{menu}</nav>
<div class="menu__onder">
<a class="knop knop--licht" href="{P}contact">Offerte aanvragen</a>
<a class="knop knop--lijn-licht" data-g="telefoon" data-g-voor="Bel " hidden></a>
<a class="knop knop--lijn-licht" data-g="whatsapp" data-g-vast hidden>Stuur een WhatsApp</a>
<p class="menu__slogan">Strak in afwerking, sterk in detail</p>
</div>
</div>'''

def voet(afsluiter=True):
    cta = f'''<section class="donker sectie" style="padding-block:clamp(56px,7vw,88px)">
<div class="wrap afsluiter">
<div><h2 class="h2">Benieuwd wat er in jouw ruimte <em>mogelijk is</em>?</h2>
<p>Vraag een vrijblijvende opname aan. Frank komt langs en denkt met je mee.</p></div>
<div class="knoppen"><a class="knop knop--licht" href="{P}contact">Offerte aanvragen</a>
<a class="knop knop--lijn-licht" data-g="telefoon" data-g-voor="Bel " hidden></a></div>
</div>
</section>''' if afsluiter else ''
    links = ''.join(f'<li><a href="{P}{s}">{t}</a></li>' for s, t in NAV + [('contact', 'Contact')])
    return f'''{cta}
<footer class="voet">
<div class="wrap voet__in">
<div class="voet__merk">{MERK}<div class="voet__naam">Oldenburger Stucadoors</div><div class="voet__slogan">Strak in afwerking, sterk in detail</div></div>
<nav aria-label="Voetmenu"><h2>Pagina's</h2><ul>{links}</ul></nav>
<div><h2>Contact</h2><ul>
<li><a data-g="telefoon" hidden></a></li>
<li><a data-g="email" hidden></a></li>
<li><a data-g="whatsapp" data-g-vast hidden>WhatsApp</a></li>
<li data-g="adres" hidden></li>
<li>Werkgebied: Drenthe en omgeving</li>
</ul></div>
</div>
<div class="wrap voet__onder"><span>© <span data-jaar>2026</span> Oldenburger Stucadoors<span data-g="kvk" data-g-voor=" · KvK " hidden></span></span><a href="{P}privacy">Privacyverklaring</a></div>
</footer>
<div class="balk" aria-label="Snel contact">
<a data-g="telefoon" data-g-vast hidden>{I_TEL}Bel</a>
<a data-g="whatsapp" data-g-vast hidden>{I_WA}WhatsApp</a>
<a class="is-hoofd" href="{P}contact">Offerte</a>
</div>'''

def pagina(bestand, actief, titel, omschrijving, inhoud, afsluiter=True, index=True):
    og = ''
    if SITE_URL:
        pad = '' if bestand == 'index' else bestand
        og = f'<link rel="canonical" href="{SITE_URL}/{pad}">\n<meta property="og:url" content="{SITE_URL}/{pad}">\n<meta property="og:image" content="{SITE_URL}/assets/deel.jpg">\n'
    robots = '' if index else '<meta name="robots" content="noindex">\n'
    doc = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(omschrijving)}">
{robots}<meta name="theme-color" content="#F4EDE1">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Oldenburger Stucadoors">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(omschrijving)}">
{og}<link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{P}assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{P}assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}assets/site.css?v={VERSIE}">
</head>
<body>
{kop(actief)}
<main id="inhoud">
{inhoud.strip()}
</main>
{voet(afsluiter)}
<script src="{P}gegevens.js?v={VERSIE}"></script>
<script src="{P}assets/site.js?v={VERSIE}"></script>
</body>
</html>
'''
    open(os.path.join(ROOT, bestand + '.html'), 'w', encoding='utf-8').write(doc)

REVIEWS = '''<section class="sectie" data-reviews hidden aria-labelledby="reviews-titel">
<div class="wrap">
<div class="kop-rij"><div><p class="label">Reviews</p><h2 class="h2" id="reviews-titel">Wat klanten zeggen</h2></div></div>
<div class="reviews" data-reviews-lijst></div>
</div>
</section>'''

# ---------- inhoud ----------
DIENSTEN = [
    ('stucwerk', 'Stucwerk', 'Glad pleisterwerk voor wanden en plafonds. Strak, egaal en klaar om te schilderen of te behangen. De basis van elk mooi interieur.',
     ['Wanden', 'Plafonds', 'Nieuwbouw en renovatie'], ('img', 'dakkapel-stucwerk', 'Strak gestucte dakkapel en schuin plafond')),
    ('afbouw', 'Afbouw', 'Wanden, plafonds en afwerking in nieuwbouw en verbouw. Met aandacht voor elke hoek, naad en aansluiting, zodat het geheel klopt.',
     ['Nieuwbouw', 'Verbouwing', 'Gewelven en bogen'], ('img', 'gewelf-glad', 'Glad afgewerkt gewelf')),
    ('betonlook', 'Betonlook', 'De rustige, stoere uitstraling van beton, naadloos aangebracht. Elke wand is uniek door de natuurlijke wolking, in warme of koele tinten.',
     ['Accentwanden', 'Badkamers', 'Schouwen', 'Kleur naar wens'], ('img', 'schouw-betonlook', 'Zwevende schouw afgewerkt in betonlook')),
    ('gietvloeren', 'Gietvloeren', 'Eén doorlopende vloer zonder voegen. Rustig voor het oog, mooi van uitstraling en makkelijk schoon te houden.',
     ['Naadloos', 'Mat of glanzend', 'Woonkamer, keuken, hal'], ('img', 'gietvloer-tuindeuren', 'Woonkamer met naadloze gietvloer en tuindeuren')),
    ('verfspuiten', 'Verfspuiten', 'Snel en egaal spuitwerk voor wanden en plafonds, zonder strepen of rollerstructuur. Ideaal als afronding op vers stucwerk.',
     ['Wanden en plafonds', 'Egaal resultaat', 'Na stucwerk'], ('video', 'verfspuiten', 'Plafond en wanden worden gespoten in een afgedekte ruimte')),
]
DIENST_KLEIN = {'stucwerk': 'dakkapel-stucwerk', 'afbouw': 'gewelf-glad', 'betonlook': 'schouw-betonlook', 'gietvloeren': 'gietvloer-tuindeuren', 'verfspuiten': 'verfspuiten-poster'}
SOORT = {'stucwerk': 'Stucwerk', 'afbouw': 'Afbouw', 'betonlook': 'Betonlook', 'gietvloeren': 'Gietvloer', 'verfspuiten': 'Verfspuiten'}

STAPPEN = [
    ('Laag 1', 'De kale muur', ('video', 'kale-muur', 'Kale wanden met hoekprofielen, klaar om gestuct te worden'),
     'Komt bij je langs, bekijkt de ondergrond, meet op en adviseert welke afwerking het mooist wordt in jouw ruimte.',
     'Je krijgt een heldere offerte en weet vooraf wat er gaat gebeuren en wanneer.'),
    ('Laag 2', 'De hechtlaag', ('video', 'hechtlaag', 'Stuc wordt gespoten over de roze hechtlaag'),
     'Dekt vloeren, kozijnen en alles wat schoon moet blijven netjes af. Daarna komt de voorbehandeling, zodat het stucwerk goed hecht.',
     'Jouw spullen blijven beschermd. Je hoeft alleen de ruimte zo leeg mogelijk te maken.'),
    ('Laag 3', 'Opzetten', ('video', 'opzetten', 'Stuc wordt machinaal op een bakstenen muur gespoten'),
     'Brengt het materiaal in de juiste dikte aan en zet de wand recht en vlak uit, de basis voor alles wat volgt.',
     'De ruimte verandert zichtbaar. Oneffenheden en oude gaten verdwijnen onder de nieuwe laag.'),
    ('Laag 4', 'Afspanen', ('img', 'frank-afspanen-1', 'Frank spant het gewelf glad'),
     'Wacht het juiste moment af en spant de wand glad. Hier zit het vakmanschap: dit bepaalt hoe strak je wand straks is.',
     'De wand krijgt die gladde, egale uitstraling waar je het allemaal voor doet.'),
    ('Oplevering', 'Strak en klaar', ('video', 'oplevering', 'Rondgang door een strak opgeleverde ruimte'),
     'Loopt het resultaat samen met je na, ruimt alles op en geeft advies over drogen en schilderen.',
     'Een opgeruimde ruimte met een strakke wand. Na de droogtijd is hij klaar voor verf of behang.'),
]
STAP_KLEIN = ['kale-muur-poster', 'hechtlaag-poster', 'opzetten-poster', 'frank-afspanen-1', 'oplevering-poster']

CATS = [('stucwerk', 'Stucwerk'), ('betonlook', 'Betonlook'), ('gietvloer', 'Gietvloeren'), ('gewelf', 'Gewelven'), ('spuitwerk', 'Spuitwerk')]
WERK = [
    ('badkamer-beige-1', 'Badkamer met warme betonlook op wanden en vloer', 'Badkamer in warme betonlook', 'betonlook', False),
    ('gietvloer-glans', 'Hoogglans gietvloer waarin het raam weerspiegelt', 'Gietvloer in hoogglans', 'gietvloer', False),
    ('dakkapel-stucwerk', 'Strak gestucte dakkapel en schuin plafond', 'Dakkapel en schuin plafond', 'stucwerk', False),
    ('gewelf-glad', 'Glad afgewerkt gewelf', 'Gewelf, glad gezet', 'gewelf', False),
    ('schouw-betonlook', 'Zwevende schouw in betonlook', 'Schouw in betonlook', 'betonlook', False),
    ('verfspuiten', 'Plafond en wanden worden gespoten', 'Plafond en wanden gespoten', 'spuitwerk', True),
    ('gietvloer-tuindeuren', 'Woonkamer met naadloze gietvloer en tuindeuren', 'Gietvloer in de woonkamer', 'gietvloer', False),
    ('douche-betonlook', 'Inloopdouche met betonlook wanden', 'Douche in betonlook', 'betonlook', False),
    ('gewelf-overzicht', 'Gewelfde kelder tijdens het opzetten', 'Gewelfde kelder', 'gewelf', False),
    ('oplevering', 'Rondgang door een strak opgeleverde woonruimte', 'Strak opgeleverde woonruimte', 'stucwerk', True),
    ('badkamer-brons', 'Badkamer met metallic wanden', 'Badkamer met metallic wanden', 'betonlook', False),
    ('wanden-roze-1', 'Strak afgewerkte wanden in een warme tint', 'Wanden in warme tint', 'stucwerk', False),
    ('gietvloer-hal-1', 'Hal met doorlopende gietvloer naar de woonkamer', 'Doorlopende vloer, hal tot tuin', 'gietvloer', False),
    ('badkamer-naadloos', 'Badkamer met naadloze vloer en wanden', 'Naadloze badkamer', 'betonlook', False),
    ('afbouw-uitvoering', 'Afbouw in uitvoering met stucmachine en hoekprofielen', 'Afbouw in uitvoering', 'stucwerk', True),
    ('gietvloer-vide', 'Hoge ruimte met naadloze gietvloer', 'Gietvloer onder de vide', 'gietvloer', False),
    ('spuitwerk-uitvoering', 'Ruimte met verfspuitmachine tijdens het spuitwerk', 'Spuitwerk in uitvoering', 'spuitwerk', False),
    ('gietvloer-mat', 'Matte gietvloer in warme tint', 'Matte gietvloer', 'gietvloer', False),
    ('wanden-roze-2', 'Woonruimte met strak afgewerkte wanden en trap', 'Woonruimte afgewerkt', 'stucwerk', False),
    ('gewelf-opzet', 'Gewelf met hoekovergang tijdens het opzetten', 'Gewelf in uitvoering', 'gewelf', False),
    ('gietvloer-woonkamer', 'Woonkamer met gietvloer en tuindeuren', 'Gietvloer met tuinzicht', 'gietvloer', False),
    ('badkamer-beige-2', 'Badkamerwand in betonlook met verlichte spiegel', 'Badkamerwand met spiegel', 'betonlook', False),
    ('opzetten', 'Stuc wordt machinaal op een bakstenen muur gespoten', 'Machinaal stucen', 'stucwerk', True),
]

def bouw():
    global P
    cat = dict(CATS)

    # ----- Home -----
    dia = ['badkamer-naadloos', 'gietvloer-glans', 'schouw-betonlook', 'gietvloer-tuindeuren', 'gewelf-glad', 'badkamer-beige-1']
    dias = ''
    for i, n in enumerate(dia):
        if i == 0:
            dias += img(n, '', '100vw', lui=False, extra=f' style="animation-delay:{i*6-1}s"')
        else:
            w, h = dims(n + '.jpg')
            dias += f'<img data-src="assets/{n}.jpg" width="{w}" height="{h}" alt="" style="animation-delay:{i*6-1}s">'
    dienstkaarten = ''.join(
        f'<a class="boogkaart" href="diensten#{s}">{img(DIENST_KLEIN[s], alt, "(max-width:920px) 64vw, 230px")}<span>{t}</span></a>'
        for s, t, _, _, (_, _, alt) in DIENSTEN)
    lagen = ''
    for (nr, t, (_, _, alt), _, _), n in zip(STAPPEN, STAP_KLEIN):
        lagen += f'<a class="laagkaart" href="werkwijze" style="text-decoration:none;color:inherit">{img(n, alt, "(max-width:920px) 64vw, 230px")}<div><small>{nr}</small><strong>{t}</strong></div></a>'
    home = f'''
<section class="hero">
<div class="hero__beeld" aria-hidden="true">{dias}<div class="hero__waas"></div></div>
<div class="wrap hero__in">
<div class="hero__tekst">
<p class="label">Stucadoor in Drenthe</p>
<h1 class="hero__titel">Strak in afwerking,<br><em>sterk in detail.</em></h1>
<div class="hero__streep"></div>
<p>Van glad stucwerk en gewelven tot betonlook, gietvloeren en spuitwerk. Vakwerk dat je elke dag ziet, en elke dag voelt.</p>
<div class="knoppen"><a class="knop knop--licht" href="contact">Vraag een offerte aan</a><a class="knop knop--lijn-licht" href="projecten">Bekijk projecten</a></div>
</div>
<div class="hero__boog">
{video('hero-gewelf', 'Frank spuit stuc op een gewelfd plafond')}
<div class="zegel"><svg class="zegel__ring" width="150" height="150" viewBox="0 0 150 150" aria-hidden="true"><defs><path id="ring" d="M75 75m-56 0a56 56 0 1 1 112 0a56 56 0 1 1 -112 0"/></defs><text font-family="Inter, sans-serif" font-size="10.5" font-weight="600" letter-spacing="3.1" fill="#6E5A32"><textPath href="#ring">STRAK IN AFWERKING · STERK IN DETAIL · </textPath></text></svg><span style="width:56px;height:56px;color:#8C7445">{MERK}</span></div>
</div>
</div>
</section>

<section class="zeker" aria-label="Waar je op kunt rekenen">
<div class="wrap"><ul>
<li>{I_HUIS}<div><strong>Vrijblijvende opname aan huis</strong><span>Frank bekijkt de ruimte en denkt mee</span></div></li>
<li>{I_BLAD}<div><strong>Heldere offerte vooraf</strong><span>Je weet waar je aan toe bent</span></div></li>
<li>{I_MENS}<div><strong>Persoonlijk contact met Frank</strong><span>Van opname tot oplevering</span></div></li>
</ul></div>
</section>

<section class="sectie diep">
<div class="wrap">
<div class="quote-merk">{MERK}</div>
<p class="quote">Een wand of vloer zie je elke dag. Daarom verdient hij <em>echt vakwerk</em>: rustig, strak en gemaakt om lang mooi te blijven.</p>
</div>
</section>

<section class="sectie">
<div class="wrap">
<div class="kop-rij"><div><p class="label">Diensten</p><h2 class="h2">Vijf manieren om een ruimte af te maken</h2></div><a class="link" href="diensten">Alle diensten bekijken</a></div>
<div class="rij">{dienstkaarten}</div>
</div>
</section>

<section class="sectie donker">
<div class="wrap uitgelicht">
<div class="uitgelicht__beelden">{img('frank-afspanen-2', 'Frank zet het gewelf glad met de spaan', '(max-width:820px) 46vw, 340px')}{img('gewelf-glad', 'Het gladde resultaat van het gewelf', '(max-width:820px) 46vw, 340px')}</div>
<div class="uitgelicht__tekst">
<p class="label">Uitgelicht</p>
<h2 class="h2">Een gewelf, <em>laag voor laag</em> strak gezet</h2>
<p>Geen rechte wand, maar een doorlopende boog. Machinaal opgezet en daarna met de hand gladgespaand, tot de ronding vloeiend doorloopt.</p>
<a class="link" href="projecten">Bekijk het project</a>
</div>
</div>
</section>

<section class="sectie diep">
<div class="wrap">
<div class="kop-rij"><div><p class="label">Werkwijze</p><h2 class="h2">Laag voor laag naar <em>een strakke wand</em></h2></div><a class="link" href="werkwijze">Zo werkt Frank</a></div>
<div class="rij">{lagen}</div>
</div>
</section>

<section class="sectie">
<div class="wrap">
<div class="kop-rij"><div><p class="label">Projecten</p><h2 class="h2">Recent werk</h2></div><a class="link" href="projecten">Alle projecten</a></div>
<div class="trio">{img('badkamer-beige-1', 'Badkamer met betonlook wanden en naadloze vloer', '(max-width:700px) 100vw, 700px')}<div>{img('gietvloer-glans', 'Hoogglans gietvloer', '(max-width:700px) 50vw, 480px')}{img('schouw-betonlook', 'Schouw in betonlook', '(max-width:700px) 50vw, 480px')}</div></div>
</div>
</section>

{REVIEWS.replace('class="sectie"', 'class="sectie diep"')}

<section class="sectie diep" style="border-top:1px solid var(--lijn)">
<div class="wrap duo">
<div class="duo__beeld">{img('frank-afspanen-1', 'Frank aan het werk met de spaan', '(max-width:820px) 340px, 440px', 'boog')}</div>
<div class="duo__tekst">
<p class="label">Over Frank</p>
<h2 class="h2">Persoonlijk contact, van opname tot oplevering</h2>
<p class="intro">Frank Oldenburger komt zelf langs om je ruimte te bekijken en denkt met je mee over de mooiste afwerking.</p>
<a class="link" href="over-frank">Maak kennis met Frank</a>
</div>
</div>
</section>'''
    pagina('index', 'home', 'Oldenburger Stucadoors | Stucadoor in Drenthe',
           'Strak in afwerking, sterk in detail. Stucwerk, afbouw, betonlook, gietvloeren en verfspuiten in Drenthe en omgeving. Vraag een vrijblijvende offerte aan.', home)

    # ----- Diensten -----
    blokken = ''
    for i, (s, t, tekst, chips, (soort, naam, alt)) in enumerate(DIENSTEN):
        beeld = img(naam, alt, '(max-width:820px) 340px, 440px', 'boog') if soort == 'img' else video(naam, alt, 'boog')
        ch = ''.join(f'<li>{c}</li>' for c in chips)
        blokken += f'''
<section id="{s}" class="sectie{' diep' if i % 2 else ''}" style="padding-block:clamp(48px,7vw,88px)">
<div class="wrap duo{' duo--om' if i % 2 else ''}">
<div class="duo__beeld">{beeld}</div>
<div class="duo__tekst">
<span class="nummer" aria-hidden="true">0{i+1}</span>
<h2 class="h2">{t}</h2>
<p class="intro">{tekst}</p>
<ul class="chips">{ch}</ul>
<a class="link" href="contact?soort={SOORT[s]}">Offerte voor {t.lower()} aanvragen</a>
</div>
</div>
</section>'''
    snel = ''.join(f'<a href="#{s}">{t}</a>' for s, t, *_ in DIENSTEN)
    diensten = f'''
<section class="wrap" style="padding-block:clamp(48px,7vw,88px) clamp(16px,3vw,32px)">
<div style="display:flex;flex-direction:column;gap:24px">
<p class="label">Diensten</p>
<h1 class="h1">Vijf afwerkingen, <em>één aanspreekpunt.</em></h1>
<p class="intro">Wand, plafond of vloer: Frank verzorgt de hele afwerking, zodat alles op elkaar aansluit.</p>
<nav class="snel" aria-label="Diensten op deze pagina">{snel}</nav>
</div>
</section>
{blokken}'''
    pagina('diensten', 'diensten', 'Diensten | Oldenburger Stucadoors',
           'Stucwerk, afbouw, betonlook, gietvloeren en verfspuiten door Frank Oldenburger in Drenthe en omgeving.', diensten)

    # ----- Werkwijze -----
    stappen = ''
    for nr, t, (soort, naam, alt), doet, merkt in STAPPEN:
        beeld = img(naam, alt, '(max-width:760px) 100vw, 340px', 'stap__beeld') if soort == 'img' else video(naam, alt, 'stap__beeld')
        stappen += f'''
<li class="stap">
{beeld}
<div>
<div class="stap__kop"><span>{nr}</span><h2>{t}</h2></div>
<div class="stap__cols">
<div><h3>Wat Frank doet</h3><p>{doet}</p></div>
<div><h3>Wat jij merkt</h3><p>{merkt}</p></div>
</div>
</div>
</li>'''
    werkwijze = f'''
<section class="wrap" style="padding-block:clamp(48px,7vw,88px) clamp(32px,5vw,64px)">
<div class="kop-rij" style="margin-bottom:0"><div><p class="label">Werkwijze</p><h1 class="h1">Laag voor laag, <em>tot hij strak is.</em></h1></div>
<p class="intro" style="max-width:42ch">Een strakke wand ontstaat niet in één keer. Hieronder zie je de muur veranderen, laag voor laag. Bij elke laag lees je wat Frank doet en wat jij ervan merkt.</p></div>
</section>
<section class="wrap" style="padding-bottom:var(--sectie)">
<ol class="stappen">{stappen}
</ol>
</section>'''
    pagina('werkwijze', 'werkwijze', 'Werkwijze | Oldenburger Stucadoors',
           'Laag voor laag naar een strakke wand: zo werkt Oldenburger Stucadoors, van opname tot oplevering.', werkwijze)

    # ----- Projecten -----
    figuren = ''
    for naam, alt, t, c, is_video in WERK:
        bron = naam + '-poster' if is_video else naam
        w, h = dims(bron + '.jpg')
        k = None if is_video else klein(naam)
        srcset = f' srcset="assets/{k} 800w, assets/{naam}.jpg {w}w" sizes="(max-width:900px) 50vw, 400px"' if k else ''
        extra = f' data-video="assets/{naam}.mp4"' if is_video else ''
        speel = '<span class="werk__speel" aria-hidden="true"></span>' if is_video else ''
        figuren += (f'<button class="werk" type="button" data-cat="{c}" data-groot="assets/{bron}.jpg"{extra} aria-label="{e(t)} vergroten">'
                    f'<span class="werk__beeld"><img src="assets/{k or bron + ".jpg"}"{srcset} width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async">{speel}</span>'
                    f'<span class="werk__titel"><strong>{t}</strong><small>{cat[c]}</small></span></button>\n')
    knoppen = '<button type="button" data-filter="alles" aria-pressed="true">Alles</button>' + ''.join(
        f'<button type="button" data-filter="{c}" aria-pressed="false">{t}</button>' for c, t in CATS)
    vier = [('img', 'gewelf-ruw', 'Het gewelf in ruwe staat', 'Ruwe staat'), ('video', 'hero-gewelf', 'Stuc wordt machinaal op het gewelf gespoten', 'Opzetten'),
            ('img', 'frank-afspanen-2', 'Frank spant het gewelf glad', 'Afspanen'), ('img', 'gewelf-glad', 'Het glad afgewerkte gewelf', 'Resultaat')]
    vier_html = ''.join(
        f'<figure>{img(n, alt, "(max-width:760px) 50vw, 290px") if s == "img" else video(n, alt)}<figcaption><span>0{i+1}</span>{t}</figcaption></figure>'
        for i, (s, n, alt, t) in enumerate(vier))
    projecten = f'''
<section class="wrap" style="padding-block:clamp(48px,7vw,88px) clamp(32px,5vw,64px)">
<div class="kop-rij" style="margin-bottom:0"><div><p class="label">Projecten</p><h1 class="h1">Het werk <em>spreekt voor zich.</em></h1></div>
<p class="intro" style="max-width:40ch">Van een gewelfde kelder tot een badkamer in warme betonlook. Een greep uit recent werk van Frank.</p></div>
</section>

<section class="sectie donker">
<div class="wrap">
<div class="kop-rij"><div><p class="label">Uitgelicht project</p><h2 class="h2">Het gewelf, <em>van ruw tot strak</em></h2></div>
<p style="max-width:44ch">Een gewelfd plafond vraagt om geduld en een vaste hand. Machinaal opgezet, daarna met de spaan gladgezet tot de boog vloeiend doorloopt.</p></div>
<div class="vier">{vier_html}</div>
</div>
</section>

<section class="sectie">
<div class="wrap">
<div class="kop-rij"><h2 class="h2">Meer werk</h2><div class="filters" role="group" aria-label="Filter op soort werk" style="flex-direction:row;max-width:none">{knoppen}</div></div>
<div class="galerij">
{figuren}</div>
<p class="leeg" hidden>Van dit soort werk staan nog geen foto's online.</p>
</div>
</section>

<dialog class="lichtbak" aria-label="Foto vergroot">
<div class="lichtbak__in">
<div class="lichtbak__top"><span class="lichtbak__teller"></span><button class="lichtbak__knop" type="button" data-sluit>Sluiten</button></div>
<div class="lichtbak__podium"></div>
<div class="lichtbak__onder"><span class="lichtbak__titel"></span><div class="lichtbak__nav"><button class="lichtbak__knop" type="button" data-vorige>Vorige</button><button class="lichtbak__knop" type="button" data-volgende>Volgende</button></div></div>
</div>
</dialog>'''
    pagina('projecten', 'projecten', 'Projecten | Oldenburger Stucadoors',
           'Projecten van Oldenburger Stucadoors: gewelven, betonlook, gietvloeren, stucwerk en spuitwerk in Drenthe en omgeving.', projecten)

    # ----- Over Frank -----
    over = f'''
<section class="wrap sectie" style="padding-top:clamp(48px,7vw,88px)">
<div class="duo">
<div class="duo__beeld">{img('frank-afspanen-2', 'Frank Oldenburger aan het werk met de spaan', '(max-width:820px) 340px, 440px', 'boog boog--schaduw', lui=False)}</div>
<div class="duo__tekst" style="gap:22px">
<p class="label">Over Frank</p>
<h1 class="h1">De man achter <em>de spaan.</em></h1>
<p class="intro">Bij Oldenburger Stucadoors heb je direct contact met Frank Oldenburger. Hij komt zelf langs om je ruimte te bekijken en denkt met je mee over de mooiste afwerking.</p>
<p class="tekst">Of het nu gaat om een strakke wand, een gewelf, een badkamer in betonlook of een naadloze vloer: het werk is pas klaar als het ook van dichtbij klopt.</p>
<p class="handtekening">Frank Oldenburger</p>
<a class="knop" href="contact">Plan een vrijblijvende opname</a>
</div>
</div>
</section>

<section class="sectie diep">
<div class="wrap">
<div class="kop-rij"><h2 class="h2">Waar je op kunt rekenen</h2></div>
<div class="drie">
<article>{img('dakkapel-stucwerk', 'Strak afgewerkte dakkapel', '(max-width:820px) 100vw, 380px')}<h3>Strak in afwerking</h3><p>Rechte hoeken, vlakke wanden en nette aansluitingen. Het resultaat moet kloppen, ook als je er van dichtbij naar kijkt.</p></article>
<article>{video('afdekken', 'Detail van een strak afgewerkte hoek en aansluiting')}<h3>Sterk in detail</h3><p>Aandacht voor de kleine dingen: stopcontacten, plinten, kozijnen. Juist daar zie je het verschil.</p></article>
<article>{img('frank-afspanen-1', 'Frank op de trap, aan het werk aan een gewelf', '(max-width:820px) 100vw, 380px')}<h3>Persoonlijk contact</h3><p>Korte lijnen met Frank zelf, van de eerste opname tot de oplevering.</p></article>
</div>
</div>
</section>

{REVIEWS}'''
    pagina('over-frank', 'over-frank', 'Over Frank | Oldenburger Stucadoors',
           'Maak kennis met Frank Oldenburger, stucadoor in Drenthe. Persoonlijk contact van opname tot oplevering.', over)

    # ----- Contact -----
    opties = ''.join(f'<option>{o}</option>' for o in ['Stucwerk', 'Afbouw', 'Betonlook', 'Gietvloer', 'Verfspuiten', 'Anders'])
    contact = f'''
<section class="wrap sectie" style="padding-top:clamp(48px,7vw,88px)">
<div class="contact">
<div class="contact__links">
<p class="label">Contact</p>
<h1 class="h1">Vertel wat je <em>voor ogen hebt.</em></h1>
<p class="intro">Vul het formulier in of neem direct contact op. Frank reageert persoonlijk en plant een vrijblijvende opname bij je thuis.</p>
<div class="kanalen">
<a data-g="telefoon" hidden>{I_TEL}<span><small>Bellen</small><strong data-g-tekst></strong></span></a>
<a data-g="whatsapp" data-g-vast hidden>{I_WA}<span><small>WhatsApp</small><strong>Stuur een bericht of foto's</strong></span></a>
<a data-g="email" hidden>{I_MAIL}<span><small>E-mail</small><strong data-g-tekst></strong></span></a>
<div>{I_PIN}<span><small>Werkgebied</small><strong>Drenthe en omgeving</strong></span></div>
</div>
</div>
<form class="formulier" novalidate>
<h2>Offerte aanvragen</h2>
<p>Hoe meer je vertelt, hoe gerichter Frank kan meedenken.</p>
<div class="veld"><label for="f-naam">Naam</label><input id="f-naam" name="naam" type="text" autocomplete="name" required aria-describedby="fout-naam"><span class="veld__fout" id="fout-naam" data-fout="naam" hidden></span></div>
<div class="veld"><label for="f-plaats">Plaats <i>(optioneel)</i></label><input id="f-plaats" name="plaats" type="text" autocomplete="address-level2"></div>
<div class="veld"><label for="f-email">E-mailadres</label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" aria-describedby="fout-email"><span class="veld__fout" id="fout-email" data-fout="email" hidden></span></div>
<div class="veld"><label for="f-telefoon">Telefoonnummer</label><input id="f-telefoon" name="telefoon" type="tel" autocomplete="tel" inputmode="tel"></div>
<div class="veld"><label for="f-soort">Soort werk</label><select id="f-soort" name="soort">{opties}</select></div>
<div class="veld"><label for="f-oppervlakte">Oppervlakte in m² <i>(ongeveer)</i></label><input id="f-oppervlakte" name="oppervlakte" type="text" inputmode="numeric"></div>
<div class="veld veld--breed"><label for="f-bericht">Wat wil je laten doen?</label><textarea id="f-bericht" name="bericht" rows="5" required aria-describedby="fout-bericht"></textarea><span class="veld__fout" id="fout-bericht" data-fout="bericht" hidden></span></div>
<div class="honing" aria-hidden="true"><label for="f-website">Laat dit veld leeg</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<p class="melding" role="status" tabindex="-1" hidden></p>
<div class="formulier__voet"><button class="knop" type="submit">Offerte aanvragen</button><small>Je gegevens worden alleen gebruikt om op je aanvraag te reageren. Lees de <a href="privacy">privacyverklaring</a>.</small></div>
</form>
</div>
</section>'''
    pagina('contact', 'contact', 'Contact en offerte | Oldenburger Stucadoors',
           'Vraag een vrijblijvende offerte aan bij Oldenburger Stucadoors, stucadoor in Drenthe en omgeving.', contact, afsluiter=False)

    # ----- Privacy -----
    privacy = '''
<section class="wrap sectie" style="padding-top:clamp(48px,7vw,88px)">
<div class="proza">
<p class="label">Privacy</p>
<h1 class="h1" style="color:var(--inkt)">Privacyverklaring</h1>
<p>Oldenburger Stucadoors gaat zorgvuldig om met je gegevens. Hieronder lees je welke gegevens worden verwerkt en waarom.</p>
<h2>Welke gegevens</h2>
<p>Als je het offerteformulier invult of contact opneemt, ontvangt Oldenburger Stucadoors de gegevens die je zelf doorgeeft:</p>
<ul><li>naam en plaats</li><li>e-mailadres en telefoonnummer</li><li>de omschrijving van het werk en eventuele foto's die je meestuurt</li></ul>
<h2>Waarvoor</h2>
<p>De gegevens worden alleen gebruikt om op je aanvraag te reageren, een offerte te maken en de afgesproken werkzaamheden uit te voeren. Ze worden niet verkocht en niet gebruikt voor reclame.</p>
<h2>Delen met anderen</h2>
<p>Gegevens worden alleen gedeeld als dat nodig is om de website en het formulier te laten werken, bijvoorbeeld met de partij die de website host en de dienst die formulierberichten doorstuurt, of als de wet dat verplicht.</p>
<h2>Bewaren</h2>
<p>Je gegevens worden niet langer bewaard dan nodig is voor het doel waarvoor je ze hebt gegeven, of zolang de wet dat voorschrijft, bijvoorbeeld voor de administratie.</p>
<h2>Cookies</h2>
<p>Deze website plaatst geen cookies en houdt geen bezoekersstatistieken bij. Lettertypes en beelden worden vanaf de website zelf geladen.</p>
<h2>Jouw rechten</h2>
<p>Je kunt altijd vragen welke gegevens er van je bekend zijn, en vragen om ze aan te passen of te verwijderen. Neem daarvoor contact op via de <a href="contact">contactpagina</a>. Heb je een klacht over de omgang met je gegevens, dan kun je die ook indienen bij de Autoriteit Persoonsgegevens.</p>
</div>
</section>'''
    pagina('privacy', '', 'Privacyverklaring | Oldenburger Stucadoors', 'Hoe Oldenburger Stucadoors omgaat met je gegevens.', privacy, afsluiter=False)

    # ----- 404 -----
    P = '/'
    pagina('404', '', 'Pagina niet gevonden | Oldenburger Stucadoors', 'Deze pagina bestaat niet.', '''
<section class="wrap sectie"><div class="midden">
<p class="label">Pagina niet gevonden</p>
<h1 class="h1">Hier zit een <em>gat in de muur.</em></h1>
<p class="intro">Deze pagina bestaat niet of is verplaatst. Ga terug naar de homepage of bekijk de projecten.</p>
<div class="knoppen"><a class="knop" href="/">Naar de homepage</a><a class="knop knop--lijn" href="/projecten">Bekijk projecten</a></div>
</div></section>''', afsluiter=False, index=False)
    P = ''

    if SITE_URL:
        urls = ['', 'diensten', 'werkwijze', 'projecten', 'over-frank', 'contact', 'privacy']
        open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            ''.join(f'<url><loc>{SITE_URL}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
        open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
    print('klaar')

if __name__ == '__main__':
    bouw()
