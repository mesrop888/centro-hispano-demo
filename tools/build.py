# Centro Hispano — Fiesta build. Writes static pages into argv[1].
import pathlib, sys

OUT = pathlib.Path(sys.argv[1])

ALL = """025fd91750514651aaf2e91e0e7fa8d2.jpg 04f1b25e36e74a48a98bcad3430499a1.png 078c5fd0cb8a4b599b643ff8f7656158.jpg 0a8b40f27452440981a51c4c149a5fc9.png 0e37da43989240ffbc17dab3d53c9cdb.jpg 0e644dbea30c42f9928efb442f2427fc.jpg 111515242bf449c68f76a99a045b48f7.jpg 123a94f591184b91ac400cbc56f2da47.jpg 12a398283fdc41c88117994045c1a0df.jpg 16a949235d3e4740abd7e24249adc6f0.jpg 1e5397673e394aba82a7f4ee50ce73f8.jpg 210114791108458594e4496b1b44a152.jpg 22d0e79f931444aab9339638ea5ef423.jpg 245c267e75ff4de8a970bc1e960d82a3.jpg 2498b915d0614a3a92aafae63ee775d2.jpg 2557022d35554fd49a68daac123e4e3c.jpg 283b781ee761447e99eca886a3891c27.jpg 2b278f41e4d646eea393b7d18229e70a.jpg 39549d7aebe94623b5d262b000c057c9.jpg 3ad5b3e418994bafb6d9735725a72ab0.jpg 40a5dceca16a45d8a17fa6077df25631.jpg 42f8c0e496af495c9fb10e634e31987d.jpg 4494b57138634dad8c4e26dd29391bd5.jpg 4ab4f220a9324691b0b15ca0726ed2c3.jpg 5f8ed6a5c7964566a4a3b6736aa3a04b.jpg 63b335c844464c43b5885ec29569bb8f.jpg 65bdacc65668436393e1c1a733a7a59a.jpg 67bbc821efee42bdb64ff7f986acbe38.jpg 6bc73fda53b64a048e283e178f572690.jpg 6da8adf4c8de4920970d3bb4244b9dc4.jpg 705cf5d5aafb4bcc82208c8dc4160c26.jpg 712d436181a34309acfed9e9bb5072c5.png 7407c0b6729b40e0a6582404fe59ee4f.jpg 7d2c5775054c4bf6a9ec87b4ac6b9fad.jpg 7ff5ac1e9d624a9f9ff6bfbdbc1faddc.jpg 8601924ec0d14bd392c6ca0284420993.png 892660a430034863bbea6428a60cdc14.png 8ba8e9e42606453a8bf7b23c571bcc0b.png 8be0f2d7f3b34a80896d81ffbc20f9c8.jpg 8f0531124c57475ba703b141bdb75930.jpg 93fb63c85a0b48349cf4f30be6d6d21d.jpg 9431bd7494064f27945da7aaf8bd2322.png 974d125963384bf3be7fd9b069b04913.jpg 97dcae3a89bc493bbe01a97d16a1e6ee.jpg 9e63e0deda6a43d59139569799384946.jpg 9f75c74f12a6477da7117da7ee386709.jpg a048b916389540d599e8587ee17cf1a4.png a196f370382a4d6981e957fd9f4b507f.jpg a5dd05d22d6b48eba51d06798e650c44.jpg a686a2eddefb4cf389319656b630dc78.jpg a9228cdd7fb64534a4408bcb5fa761e8.jpg be22ee667ca94397b48627b3e6bfda23.jpg c2c24be8dbfd47728d8915a8078d1868.jpg c32b05ffc7da4a03b58e573d331c09fc.png c4d8345566d147b7a767b63ff43f7b7c.jpg c74e1c1bf07b463ead3508638651cafd.jpg c97a7f15042644268f2a638bbe58e04c.jpg cab24279f0354f68a692ccbe0322903d.jpg cccf8097429446178ebc5ae7af452ca1.jpg db24054d26a6447a9faa9122e5617259.jpg dcc55928ec4c4f68a1bb9a3852a2ad3a.jpg e2c748cef495494d901edc413c832974.jpg e492613d453e40c39a4a8c94f7826abb.jpg eb95237ee53342a5acc9b06c0c79ac2a.jpg ec53fa4b93aa43859b40c3f6cf7de89f.jpg ec61266a8a83400792d7d8c99c7faa68.jpg f7c9cee93a2a4f13a595dfe9bee01188.jpg fa1d8071178f4aa492bd7a54fc90dd5b.png fc8c874d34ec4f498fcbb37cb7a6409d.png fe59ee871b29408799892ed4aded437f.jpg""".split()
FULL = {f[:6]: f for f in ALL}
USED = []
PAGES = {}

def src(p, mode, w, h, q=80):
    f = FULL[p]; USED.append(p)
    ident, ext = f.split(".")
    out = "png" if p in ("fc8c87", "9431bd", "c32b05") else "jpg"
    return f"https://static.wixstatic.com/media/0c1502_{ident}~mv2.{ext}/v1/{mode}/w_{w},h_{h},al_c,q_{q},enc_auto/{p}.{out}"

def pic(p, w, h, alt, cls="", eager=False, sizes="(max-width: 760px) 100vw, 40vw"):
    a, b = src(p, "fill", w, h), src(p, "fill", w * 2, h * 2)
    USED.pop();
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{a}" srcset="{a} {w}w, {b} {w*2}w" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" '
            f'loading="{"eager" if eager else "lazy"}"{" fetchpriority=\"high\"" if eager else ""} decoding="async">')

def cut(p, w, h, alt, cls=""):  # transparent cut-out art, keep aspect
    s = src(p, "fit", w, h, 90)
    return f'<img class="{cls}" src="{s}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async">'

LOGO = "https://static.wixstatic.com/media/0c1502_070f380011be40ed92d53050e5c54a0b~mv2.png/v1/fill/w_420,h_133,al_c,q_90,enc_auto/centro-hispano.png"
ARROW = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M2 9h13M10 4l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PHONE = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M5.2 1.8 7 5.6 5.3 7a9.6 9.6 0 0 0 5.7 5.7l1.4-1.7 3.8 1.8-.6 3A1.8 1.8 0 0 1 13.8 17 13.4 13.4 0 0 1 1 4.2a1.8 1.8 0 0 1 1.3-1.8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'

FLAG_AM = '<svg viewBox="0 0 30 30"><rect width="30" height="10" fill="#d90012"/><rect y="10" width="30" height="10" fill="#0033a0"/><rect y="20" width="30" height="10" fill="#f2a800"/></svg>'
FLAG_ES = '<svg viewBox="0 0 30 30"><rect width="30" height="30" fill="#aa151b"/><rect y="7.5" width="30" height="15" fill="#f1bf00"/></svg>'
FLAG_US = ('<svg viewBox="0 0 30 30"><rect width="30" height="30" fill="#fff"/>'
           + "".join(f'<rect y="{i * 30 / 13:.2f}" width="30" height="{30 / 13:.2f}" fill="#b22234"/>' for i in range(0, 13, 2))
           + '<rect width="15" height="16.15" fill="#3c3b6e"/>'
           + "".join(f'<circle cx="{2.5 + c * 3.3 + (r % 2) * 1.65:.2f}" cy="{2.2 + r * 2.9:.2f}" r=".75" fill="#fff"/>' for r in range(5) for c in range(4 - r % 2))
           + '</svg>')

NAV = [("cursos.html", "Courses"), ("eventos.html", "Events"), ("nosotros.html", "About")]

def header(active):
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    cta = f'<li class="nav-cta"><a href="contacto.html"{" aria-current=\"page\"" if active == "contacto.html" else ""}>Contact us</a></li>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="{LOGO}" width="172" height="55" alt="Centro Hispano — Hispanic Center, since 2003"></a>
    <div class="langs" role="group" aria-label="Language">
      <a href="@@HREF_hy@@" hreflang="hy" lang="hy" @@CUR_hy@@><span class="flag" aria-hidden="true">{FLAG_AM}</span><span class="sr">Հայերեն</span></a>
      <a href="@@HREF_en@@" hreflang="en" lang="en" @@CUR_en@@><span class="flag" aria-hidden="true">{FLAG_US}</span><span class="sr">English</span></a>
      <a href="@@HREF_es@@" hreflang="es" lang="es" @@CUR_es@@><span class="flag" aria-hidden="true">{FLAG_ES}</span><span class="sr">Español</span></a>
    </div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><svg class="burger" viewBox="0 0 16 16" aria-hidden="true"><path class="b1" d="M1.5 3.5h13"/><path class="b2" d="M1.5 8h13"/><path class="b3" d="M1.5 12.5h13"/></svg></button>
    <nav class="nav" id="nav" aria-label="Main"><ul>{items}{cta}</ul></nav>
  </div>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo-chip" href="index.html"><img src="{LOGO}" width="180" height="57" alt="Centro Hispano"></a>
        <p class="since">Spanish language and Hispanic culture in Armenia since 15 December 2003.</p>
      </div>
      <div>
        <h2>Visit</h2>
        <p>Mashtots Avenue 52/2<br>Yerevan 0009, Armenia</p>
        <p class="mt" style="margin-top:12px;color:#ffffff">Mon–Fri 10:00–21:00<br>Sat 11:00–19:00</p>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a class="num" href="tel:+37433547102">+374 33 547 102</a></li>
          <li><a class="num" href="tel:+37491547102">+374 91 547 102</a></li>
          <li><a href="mailto:info@centrohispano.am">info@centrohispano.am</a></li>
        </ul>
      </div>
      <div>
        <h2>Follow</h2>
        <ul>
          <li><a href="https://www.instagram.com/centrohispano.am/" rel="noopener">Instagram</a></li>
          <li><a href="https://www.facebook.com/centrohispano.am" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="fine"><span>© 2003–2026 Centro Hispano · Hispanic Center</span><span>Spanish A1–C2 · DELE preparation · Fiestas, film and music</span></div>
  </div>
</footer>'''

LIGHTBOX = f'''<dialog class="lightbox" id="lightbox" aria-label="Photo viewer">
  <figure><img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt=""><figcaption></figcaption></figure>
  <button class="lb-btn lb-prev" type="button" aria-label="Previous photo"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M16 9H3M8 4 3 9l5 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  <button class="lb-btn lb-next" type="button" aria-label="Next photo">{ARROW}</button>
  <button class="lb-btn lb-close" type="button" aria-label="Close viewer"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4 4l10 10M14 4 4 14" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg></button>
</dialog>'''

def page(file, active, title, desc, main, extra=""):
    html = f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#d1303a">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Figtree:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="assets/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="alternate" hreflang="en" href="@@HREF_en@@">
<link rel="alternate" hreflang="es" href="@@HREF_es@@">
<link rel="alternate" hreflang="hy" href="@@HREF_hy@@">
</head>
<body>
{header(active)}
<main id="main">
{main}
</main>
{FOOTER}
{extra}
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    PAGES[file] = html

# ---------------- content ----------------
LEVELS = [("A1", "Beginner", "36,000", "a", 0), ("A2", "Elementary", "36,000", "a", 1),
          ("B1.1", "Basic initial", "48,000", "b", 2), ("B1.2", "Upper basic", "48,000", "b", 3),
          ("B2.1", "Intermediate initial", "48,000", "b", 4), ("B2.2", "Upper intermediate", "48,000", "b", 5),
          ("C1", "Advanced", "60,000", "c", 6), ("C2", "Proficiency", "60,000", "c", 7)]

def ladder():
    li = "".join(f'''<li class="{g}" style="--h:{h}"><a href="cursos.html#{c.lower().replace('.', '')}">
  <span><span class="lv">{c}</span><span class="nm">{n}</span></span>
  <span class="pr">{p}<small>AMD / month</small></span></a></li>''' for c, n, p, g, h in LEVELS)
    return f'<ol class="ladder" aria-label="Classical Spanish levels and monthly fees">{li}</ol>'

COURSES = [
    ("classical", "c2c24b", "A group lesson around white tables in a red-walled classroom", "Classical Spanish",
     "The full programme, six levels from A1 to C2. Reading, writing and speaking together.", ["3× a week", "1.5 h lessons", "2 months per level"], "from 36,000", "AMD / month"),
    ("accelerated", "a9228c", "Students at a group lesson in a bright classroom", "Accelerated",
     "For when you need Spanish in a very short time.", ["4× a week", "1.5 h lessons", "2 months"], "64,000", "AMD / month"),
    ("passive", "be22ee", "A relaxed group class with the teacher at the board", "Passive",
     "General Spanish for everyday life, at a gentler pace.", ["2× a week", "1.5 h lessons", "4 months"], "32,000", "AMD / month"),
    ("conversational", "04f1b2", "Students talking around a table under a mural", "Conversational",
     "Seminars and debates with native speakers, plus films and songs.", ["2× a week", "1.5 h", "Continuous"], "24,000", "AMD / month"),
    ("individual", "3ad5b3", "A teacher working one-to-one with a student", "Individual",
     "A programme built around you, any level, your schedule.", ["1–6× a week", "1 h lessons", "Two people: 12,000"], "8,000", "AMD / lesson"),
    ("dele", "65bdac", "A Centro Hispano certificate of completion", "DELE preparation",
     "Exam preparation with Instituto Cervantes materials. Certificate at the end.", ["All 4 skills", "1 h lessons", "Your level"], "8,000", "AMD / lesson"),
]

def course_cards():
    out = []
    for k, p, alt, t, d, tags, fee, unit in COURSES:
        tg = "".join(f"<li>{x}</li>" for x in tags)
        out.append(f'''<article class="course">
  {pic(p, 480, 300, alt, sizes="(max-width: 600px) 100vw, (max-width: 980px) 50vw, 33vw")}
  <div class="body">
    <h3><a href="cursos.html#{k}">{t}</a></h3>
    <p>{d}</p>
    <ul class="tags">{tg}</ul>
    <div class="fee"><b>{fee}</b><span>{unit}</span></div>
  </div>
</article>''')
    return "".join(out)

COLLAGE = [
    ("dcc559", "x2", "Students on yellow chairs during a lesson"), ("db2405", "", "A small group studying at a round table"),
    ("283b78", "", "A teacher writing on the whiteboard"), ("12a398", "h2", "A classroom with maps of the Spanish-speaking world"),
    ("245c26", "", "Students reading beside a mural of Cervantes"), ("2498b9", "w2", "A teacher helping a student with her notebook"),
    ("QUOTE", "", ""), ("1e5397", "w2", "A seminar around long red tables"), ("6da8ad", "w2", "Students working together at a table"),
    ("705cf5", "", "Two women reviewing papers at a desk"), ("ec53fa", "w2", "A lesson in a classroom decorated with a mural"),
    ("4494b5", "w2", "Two members of the Center at their desks"), ("9431bd", "w2", "Yellow brush-stroke artwork of students from the Center"),
]

def collage():
    out = []
    for p, cls, alt in COLLAGE:
        if p == "QUOTE":
            out.append('<figure class="quote w2"><p>“All classes are led by qualified local and native Spanish-speaking teachers.”</p><span>In person or online</span></figure>')
        elif p == "9431bd":
            out.append(f'<figure class="{cls}" style="background:var(--yellow)">{cut(p, 420, 380, alt)}</figure>')
        else:
            big = cls in ("x2",)
            out.append(f'<figure class="{cls}">{pic(p, 520 if big else 320, 400 if big else 240, alt, sizes="(max-width: 560px) 50vw, 25vw")}</figure>')
    return f'<div class="collage">{"".join(out)}</div>'

DIPLOMAS = [("111515", "Students holding their course certificates", "Certificates"),
            ("123a94", "Scholarship winners holding their diplomas", "Spanish Scholarship"),
            ("0e37da", "Students presenting their certificates", "Awards")]

RIB_A = [("025fd9", "Dancers posing in front of a colourful mural"), ("078c5f", "Friends raising a toast at an evening event"),
         ("4ab4f2", "Guests in front of an event backdrop"), ("c74e1c", "Guests posing at a photo wall"),
         ("9f75c7", "A speaker at an event in front of flags"), ("e49261", "Guests at a dinner with a man in a sombrero"),
         ("eb9523", "A lively evening at a bar event")]
RIB_B = [("c97a7f", "Guests in a room decorated with a mural"), ("c4d834", "A hallway decorated with flags of Spanish-speaking countries"),
         ("8f0531", "Two people talking beside a mural"), ("a048b9", "A display wall at the Center"),
         ("7ff5ac", "A celebration cake decorated with the Center's logo"), ("8be0f2", "Guests in formal dress at a reception"),
         ("ec6126", "People gathered in an orange-walled room")]

def ribbon(items, rev=False):
    li = "".join(f"<li>{pic(p, 240, 170, alt, sizes='240px')}</li>" for p, alt in items)
    return f'<ul class="ribbon{" rev" if rev else ""}">{li}</ul>'

WALL = [("cccf80", "A crowd dancing at an open-air fiesta", "Open-air fiesta"),
        ("974d12", "Dancers in red dresses with members of the Center", "Dance evening"),
        ("16a949", "A couple dancing salsa beside congas", "Salsa night"),
        ("f7c9ce", "Mariachi musicians beside a Mexican flag", "Mariachi night"),
        ("210114", "A conga line at a pool party with Latin American flags", "Summer party"),
        ("63b335", "A guitarist performing on a dark stage", "Acoustic evening"),
        ("0e644d", "A singer and band performing on stage", "Live concert"),
        ("93fb63", "A flamenco dancer's red skirt in motion", "Flamenco"),
        ("255702", "A large group holding Spanish and Latin American flags", "Community"),
        ("a686a2", "Guests around a pool at a summer fiesta", "Pool fiesta"),
        ("2b278f", "Guests holding a Yo ♥ Centro Hispano t-shirt", "Yo ♥ CH"),
        ("97dcae", "Guests cutting a celebration cake", "Celebration"),
        ("22d0e7", "Friends at a stand decorated with flags", "Festival stand"),
        ("e2c748", "A speaker in front of Latin American flags", "Cultural evening"),
        ("cab242", "Guests relaxing on sofas at an evening event", "Club evening")]

def wall(items):
    btns = []
    for p, alt, cap in items:
        thumb = src(p, "fit", 480, 480); USED.pop()
        full = src(p, "fit", 1400, 1000, 85)
        btns.append(f'<button type="button" data-full="{full}" data-cap="{cap}" aria-label="Open photo: {cap}"><img src="{thumb}" alt="{alt}" loading="lazy" decoding="async"></button>')
    return f'<div class="wall">{"".join(btns)}</div>'

HISTORY = [
    ("860192", "The Center's building with its yellow doors", "2024", "A new building: a film studio, seminar rooms and spaces for events.", "feature"),
    ("6bc73f", "A radio host at the microphone", "2004", "“Tiempo Hispano”, Armenia's first live radio show in Armenian and Spanish.", ""),
    ("fa1d80", "Cover of the album I Love Latino", "2011", "The album “I ♥ Latino”: salsa, bachata, merengue, cumbia, reggaeton.", ""),
    ("67bbc8", "An event space at the Center", "2024", "A monthly Spanish Film Forum with the Embassy of Spain, through June 2025.", ""),
    ("7407c0", "Guests and diplomats at a reception", "2024", "The Honorary Consulate of Guatemala officially opens beside the Center.", ""),
    ("0a8b40", "A warm restaurant interior with wooden chairs", "2025", "“Olé”, a Spanish restaurant, opens inside the Center.", "w2"),
    ("c32b05", "Orange brush-stroke artwork of students from the Center", "2005", "Spanish courses begin, from beginner to the highest level.", "art"),
]

def history():
    out = []
    for p, alt, yr, t, cls in HISTORY:
        if cls == "art":
            im = f'<div style="background:var(--orange-deep);display:grid;place-items:center;aspect-ratio:4/3">{cut(p, 380, 280, alt)}</div>'
        else:
            im = pic(p, 760 if cls == "feature" else 400, 475 if cls == "feature" else 300, alt, sizes="(max-width: 560px) 100vw, 25vw")
        out.append(f'<li class="{cls}">{im}<div class="txt"><span class="yr">{yr}</span><p>{t}</p></div></li>')
    out.append('<li class="cta"><a href="nosotros.html"><span class="yr">Our story ' + ARROW + '</span><p>Every year since 2003, from the first film festival to Olé.</p></a></li>')
    return f'<ol class="history">{"".join(out)}</ol>'

PEOPLE = ["39549d", "40a5dc", "42f8c0", "712d43", "7d2c57", "8ba8e9", "9e63e0", "a196f3", "a5dd05"]
TEAM = [("Ashot Parsyan", "Founder and CEO"), ("Anush Derdzyan", "Director · Professor"), ("Vigen Parsyan", "CEO Assistant"),
        ("Svetlana Martirosyan", "Professor · Translator"), ("Lusine Khazaryan", "Professor"), ("Melchor Perez Paez", "Native certified ELE professor"),
        ("Vard Ohanyan", "Marketing and design"), ("Elizabeth Babayan", "Administrative assistant"), ("Elen Babakhanyan", "Administrative assistant")]

def people():
    figs = "".join(f"<figure>{pic(p, 240, 320, 'Portrait of a member of the Centro Hispano team', sizes='(max-width: 520px) 50vw, 11vw')}</figure>" for p in PEOPLE)
    names = "".join(f"<li><b>{n}</b> <span>· {r}</span></li>" for n, r in TEAM)
    return f'<div class="people">{figs}</div><ul class="names">{names}</ul>'

# ---------------- index ----------------
index_main = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>¿Y tú hablas <span>español?</span></h1>
      <p class="lede">Spanish courses for every level and twenty-two years of fiestas, film and music, on Mashtots Avenue in Yerevan.</p>
      <div class="actions">
        <a class="btn" href="#courses">Find your course {ARROW}</a>
        <a class="btn btn--white" href="tel:+37491547102">{PHONE} +374 91 547 102</a>
      </div>
    </div>
    <div class="hero-art">
      {pic("5f8ed6", 640, 512, "Three students on bright beanbags with a laptop and books under the words ¿Y tú hablas español?", cls="main", eager=True, sizes="(max-width: 900px) 100vw, 46vw")}
      {cut("fc8c87", 380, 267, "Red brush-stroke artwork of students from the Center", cls="brush")}
      <span class="sticker" aria-hidden="true">Desde<b>2003</b></span>
    </div>
  </div>
</section>

<section class="ribbons" aria-label="Moments from Centro Hispano">
  {ribbon(RIB_A)}
  {ribbon(RIB_B, rev=True)}
  <div class="ribbons-ctl"><button type="button" aria-pressed="false">Pause the photos</button></div>
</section>

<section class="section sun" id="courses" aria-labelledby="courses-h">
  <div class="wrap">
    <div class="head">
      <h2 id="courses-h">Pick your level. <em>We’ll get you talking.</em></h2>
      <p>Six levels from A1 to C2, two months each. Already know some Spanish? Take a placement test and join the group at your level.</p>
    </div>
    {ladder()}
    <div class="ladder-note"><span>All prices per month. Groups start with at least four students.</span><a href="contacto.html?subject=Placement%20test">Book a placement test {ARROW}</a></div>
    <div class="courses">{course_cards()}</div>
    {collage()}
  </div>
</section>

<section class="section yellow" aria-labelledby="dip-h">
  <div class="wrap diplomas">
    <div>
      <h2 id="dip-h">Certificates, scholarships, proud faces.</h2>
      <p>Every course ends with a certificate of completion. Since 2012 our yearly Spanish Scholarship has given its winners free Spanish training at the Center.</p>
      <a class="btn btn--red" href="cursos.html#dele">DELE preparation {ARROW}</a>
    </div>
    <div class="polaroids">
      {"".join(f"<figure>{pic(p, 360, 360, alt, sizes='(max-width: 520px) 50vw, 25vw')}<figcaption>{cap}</figcaption></figure>" for p, alt, cap in DIPLOMAS)}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="wall-h">
  <div class="wrap">
    <div class="head">
      <h2 id="wall-h">¡Fiesta! <em>Life at the Center.</em></h2>
      <p>Open-air fiestas, salsa nights, mariachi, flamenco, concerts and pool parties. Tap any photo to see it bigger.</p>
    </div>
    {wall(WALL)}
    <p class="mt"><a class="btn btn--red" href="https://www.instagram.com/centrohispano.am/" rel="noopener">See what’s next on Instagram {ARROW}</a></p>
  </div>
</section>

<section class="section redfield" aria-labelledby="why-h">
  <div class="wrap">
    <div class="head">
      <h2 id="why-h">Why Spanish? <em>Because the world speaks it.</em></h2>
      <p>More than twenty countries, their music, literature and cinema in the original, and a quicker road to Portuguese, Italian or French.</p>
    </div>
    <p class="why-line"><b>580M+</b> people speak it. <b>483M</b> were born into it. <b>20M</b> more start learning it every year.</p>
  </div>
</section>

<section class="section wine" aria-labelledby="hist-h">
  <div class="wrap">
    <div class="head">
      <h2 id="hist-h">Twenty-two years of <em>firsts</em>.</h2>
      <p>Founded on 15 December 2003 by Armenian economists with friends from Spain, Ecuador and Mexico. Since then, a film festival, a band, a radio show, an album and much more.</p>
    </div>
    {history()}
  </div>
</section>

<section class="section sun" aria-labelledby="team-h">
  <div class="wrap">
    <div class="head">
      <h2 id="team-h">The people behind <em>the Center</em>.</h2>
      <p>Qualified local and native-speaking teachers and a team who care about each student’s growth as a Spanish speaker.</p>
    </div>
    {people()}
  </div>
</section>

<section class="section visit" aria-labelledby="visit-h">
  {cut("892660", 1600, 900, "", cls="pattern")}
  <div class="wrap">
    <div>
      <h2 id="visit-h">Come say <span>¡hola!</span></h2>
      <div class="actions">
        <a class="btn" href="contacto.html">Write to us {ARROW}</a>
        <a class="btn btn--outline" href="https://maps.google.com/?q=Mashtots+Avenue+52%2F2,+Yerevan" rel="noopener">Open in Maps</a>
      </div>
    </div>
    <div class="card-info">
      <dl>
        <div><dt>Address</dt><dd>Mashtots Avenue 52/2, Yerevan 0009</dd></div>
        <div><dt>Opening hours</dt><dd>Mon–Fri 10:00–21:00 · Sat 11:00–19:00</dd></div>
        <div><dt>Phone</dt><dd><a href="tel:+37433547102">+374 33 547 102</a> · <a href="tel:+37491547102">+374 91 547 102</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:info@centrohispano.am">info@centrohispano.am</a></dd></div>
      </dl>
    </div>
  </div>
</section>
'''
page("index.html", "index.html", "Centro Hispano · Spanish courses and Hispanic culture in Yerevan",
     "Spanish courses from A1 to C2, DELE preparation and fiestas, film and music in Yerevan, Armenia, since 2003.", index_main, LIGHTBOX)

used_home = set(USED)
missing = [k for k in FULL if k not in used_home]
print("home photos used:", len(used_home), "of", len(FULL), "missing:", missing)
USED.clear()

# ---------------- cursos ----------------
LEVEL_ROWS = [
    ("A1", "Beginner", "36,000", "a", "Designed for students with no Spanish. You will express yourself understandably and answer simple questions in the present tense."),
    ("A2", "Elementary", "36,000", "a", "Communicate in everyday situations and understand frequent expressions in the present and past."),
    ("B1.1", "Basic initial", "48,000", "b", "Communicate simply in present and past, narrate short experiences and follow clear conversations on familiar topics."),
    ("B1.2", "Upper basic", "48,000", "b", "Talk about plans in present, past and future, recount fuller experiences, and discuss your interests more fluently."),
    ("B2.1", "Intermediate initial", "48,000", "b", "Understand and produce more complex texts and argue opinions, weighing pros and cons with a wider vocabulary."),
    ("B2.2", "Upper intermediate", "48,000", "b", "Defend your point of view clearly, react spontaneously in fluent conversation and express yourself precisely."),
    ("C1", "Advanced", "60,000", "c", "A rich vocabulary and grammar for competent, comfortable communication."),
    ("C2", "Proficiency", "60,000", "c", "Understand almost everything you hear or read and give your opinion fluently on any topic."),
]
rows = "".join(f'''<li class="level-row {g}" id="{c.lower().replace('.', '')}">
  <span class="badge">{c}</span>
  <div><h3>{n}</h3><p>{d}</p></div>
  <div class="price"><b>{p} AMD</b><span>per month · 2 months · 24 lessons</span></div>
</li>''' for c, n, p, g, d in LEVEL_ROWS)

PROGRAMS = [
    ("accelerated", "a9228c", "Students at a group lesson in a bright classroom", "Accelerated Spanish",
     ["Designed for those who need to master Spanish in a very short period of time."],
     [("Rhythm", "4× a week"), ("Lesson", "1.5 h"), ("Length", "2 months"), ("Fee", "64,000 AMD / month")]),
    ("passive", "be22ee", "A relaxed group class with the teacher at the board", "Passive Spanish",
     ["For general knowledge of Spanish, with an emphasis on the level needed for everyday communication."],
     [("Rhythm", "2× a week"), ("Lesson", "1.5 h"), ("Length", "4 months"), ("Fee", "32,000 AMD / month")]),
    ("conversational", "04f1b2", "Students talking around a table under a mural", "Conversational Spanish",
     ["For everyone who already speaks Spanish and wants to improve. Each lesson is a seminar or debate on a topic: education, culture, politics, sports, music. The teacher sends one to three pages beforehand so you arrive with the vocabulary.",
      "Lessons also include films, songs and discussion, taught exclusively by native Spanish speakers."],
     [("Rhythm", "2× a week"), ("Lesson", "1.5 h"), ("Length", "Continuous"), ("Fee", "24,000 AMD / month")]),
    ("individual", "3ad5b3", "A teacher working one-to-one with a student", "Individual Spanish",
     ["A programme built around your needs, written and spoken, for everyday or professional use, at any level. You choose the schedule."],
     [("Rhythm", "1–6× a week"), ("Lesson", "1 h"), ("Two people", "12,000 AMD"), ("Fee", "8,000 AMD / lesson")]),
    ("dele", "65bdac", "A Centro Hispano certificate of completion", "DELE preparation",
     ["Preparation for the Diploma of Spanish as a Foreign Language at your chosen level, with Instituto Cervantes materials. It covers reading, listening, writing and speaking.",
      "At the end you receive a certificate of completion for the level."],
     [("Covers", "All 4 skills"), ("Lesson", "1 h"), ("Ends with", "Certificate"), ("Fee", "8,000 AMD / lesson")]),
]
def facts(rs):
    return '<dl class="facts">' + "".join(f'<div{" class=\"is-fee\"" if k == "Fee" else ""}><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rs) + "</dl>"
programs = "".join(f'''<article class="program" id="{k}">
  <div class="pimg">{pic(p, 560, 420, alt)}</div>
  <div><h3>{t}</h3>{"".join(f"<p>{x}</p>" for x in ps)}{facts(fs)}</div>
</article>''' for k, p, alt, t, ps, fs in PROGRAMS)

cursos_main = f'''
<section class="page-hero">
  <div class="wrap">
    <div>
      <h1>Courses <span>&amp; prices</span></h1>
      <p>From your first word to C2, in groups or one-to-one, in person or online. Taught by qualified local and native-speaking teachers.</p>
      <ul class="jump" aria-label="On this page">
        <li><a href="#classical">Classical</a></li><li><a href="#accelerated">Accelerated</a></li><li><a href="#passive">Passive</a></li>
        <li><a href="#conversational">Conversational</a></li><li><a href="#individual">Individual</a></li><li><a href="#dele">DELE</a></li><li><a href="#conditions">Conditions</a></li>
      </ul>
    </div>
    {pic("c2c24b", 620, 426, "A group lesson around white tables in a red-walled classroom", eager=True)}
  </div>
</section>

<section class="section sun" id="classical" aria-labelledby="cl-h">
  <div class="wrap">
    <div class="head"><h2 id="cl-h">Classical Spanish, <em>A1 to C2</em>.</h2><p>Six levels, each two months, three times a week, 1.5 hours per lesson. Reading, writing and speaking, together.</p></div>
    {ladder()}
    <ol class="level-list mt">{rows}</ol>
  </div>
</section>

<section class="section" aria-labelledby="more-h">
  <div class="wrap">
    <div class="head"><h2 id="more-h">More ways to <em>learn</em>.</h2><p>Faster, gentler, conversation-only, one-to-one, or straight to the DELE exam.</p></div>
    {programs}
  </div>
</section>

<section class="section yellow" id="conditions" aria-labelledby="cond-h">
  <div class="wrap">
    <div class="head"><h2 id="cond-h">Registration &amp; cancellation</h2><p>Simple rules, so nothing surprises you.</p></div>
    <div class="rules">
      <article><h3>Registration</h3><p>Fill in the registration form and pay for your level at the first lesson, not in advance.</p><p>Above Beginner A1? Take the placement test and join the right group.</p></article>
      <article><h3>If we cancel</h3><p>A group needs at least four students. If it does not fill, you can take individual lessons or wait for new students to enrol.</p></article>
      <article><h3>If you cancel</h3><p>After paying you have up to six months to join another group. Missed lessons are not partially refunded.</p></article>
    </div>
    <p class="mt"><a class="btn btn--red" href="contacto.html?subject=Placement%20test">Book a placement test {ARROW}</a></p>
  </div>
</section>
'''
page("cursos.html", "cursos.html", "Courses and prices · Centro Hispano",
     "Spanish course levels A1 to C2, Accelerated, Passive, Conversational, Individual and DELE preparation, with prices in AMD.", cursos_main)

# ---------------- eventos ----------------
EV_EXTRA = [(p, alt, "Centro Hispano") for p, alt in RIB_A + RIB_B]
eventos_main = f'''
<section class="page-hero">
  <div class="wrap">
    <div>
      <h1>Fiestas, film <span>&amp; music</span></h1>
      <p>Since 2003: open-air gatherings, festivals of food, music and film, club evenings and much more.</p>
    </div>
    {pic("cccf80", 620, 426, "A crowd dancing at an open-air fiesta", eager=True)}
  </div>
</section>
<section class="section" aria-label="Photo gallery">
  <div class="wrap">
    {wall(WALL + EV_EXTRA)}
  </div>
</section>
<section class="section yellow" aria-labelledby="next-h">
  <div class="wrap diplomas">
    <div><h2 id="next-h">The next fiesta is announced on Instagram.</h2><p>Photos and videos of past events live there too. Follow along and come to the next one.</p></div>
    <div style="display:flex;flex-wrap:wrap;gap:12px">
      <a class="btn btn--red" href="https://www.instagram.com/centrohispano.am/" rel="noopener">Instagram {ARROW}</a>
      <a class="btn btn--white" href="https://www.facebook.com/centrohispano.am" rel="noopener">Facebook</a>
    </div>
  </div>
</section>
'''
page("eventos.html", "eventos.html", "Events · Centro Hispano",
     "Fiestas, concerts, film screenings, festivals and club evenings from Centro Hispano in Yerevan.", eventos_main, LIGHTBOX)

# ---------------- nosotros ----------------
TL = [
    ("2003", True, "Founded on 15 December by Armenian economists Ashot Parsyan and Vardan Asryan, with Néstor Martínez from Spain, Juan Carlos Flores from Ecuador and Carlos Antaramian from Mexico."),
    ("2004", False, "The first Spanish &amp; Latin American Film Festival in Armenia, at NPAK. Later: a Spanish film series at the Moscow Cinema (2006) and a Latin American Film Week at Narekatsi Art Institute (2009)."),
    ("2004", False, "The band “Son Latino” forms, with musicians from Colombia and Puerto Rico playing Caribbean son; debut at the Tigran Mets Hall of the Armenia Marriott."),
    ("2004", False, "“Tiempo Hispano”, a live radio show in Armenian and Spanish, the first of its kind; later “Corazón de Melón”, then “Radiofiesta”."),
    ("2005", True, "Spanish language courses begin, from beginner to the highest level."),
    ("2007", False, "Latin American folk dance classes with a Cuban instructor, and the Latin American Cuisine and Music Festival at The Club with Venezuelan musician Victor Rojas."),
    ("2008", False, "Brazilian Portuguese courses start, at the suggestion of the Brazilian Embassy, taught by Mateus Castello Branco."),
    ("2010", False, "The documentaries “Nectar of the Gods” and “Cuba in the Bottle”, broadcast on Public Television, H2 and ATV."),
    ("2011", False, "The album “I ♥ Latino”: salsa, bachata, merengue, cumbia and reggaeton."),
    ("2012", False, "“Aires de Tango” with Argentine singer Valeria Cherekian, and the start of the yearly Spanish Scholarship."),
    ("2013", False, "A master class by Colombian dancer Monica Conde, and the “I ♥ BCN” contest with a trip to Barcelona."),
    ("2014", False, "Acoustic evenings with David Rodriguez from Las Palmas de Gran Canaria."),
    ("2016", False, "A Cuban evening with a nine-member band, live music, dance and a master class."),
    ("2021", False, "Founder Ashot Parsyan is appointed Honorary Consul of Guatemala to Armenia; the consulate opens beside the Center (official ceremony, 23 October 2024)."),
    ("2024", True, "A new building with a film studio, seminar rooms and event spaces. From August 2024 to June 2025, a monthly Spanish Film Forum with the Embassy of Spain."),
    ("2025", False, "“Olé”, a Spanish restaurant, opens inside the Center in August."),
]
tl = "".join(f'<li{" class=\"major\"" if m else ""}><span class="yr">{y}</span><p>{t}</p></li>' for y, m, t in TL)
REASONS = [
    "It is the second language of international communication: more than 580 million speakers, second only to English.",
    "It is the second most spoken native language, on four continents, with nearly 483 million speakers.",
    "About 20 million people learn it every year, and demand keeps growing.",
    "It takes you to more than 20 Spanish-speaking countries, their culture and their food.",
    "Music, literature and cinema, in the original.",
    "It is the third most used language on the internet, after English and Chinese.",
    "Spain has Europe’s greatest biodiversity and is among the most visited countries in the world.",
    "It makes Portuguese, Italian, French or Romanian quicker to learn.",
    "It opens study at universities in Spain and across the Spanish-speaking world.",
    "It is a great way to meet people, make friends and grow professionally.",
]
nosotros_main = f'''
<section class="page-hero">
  <div class="wrap">
    <div>
      <h1>A bridge to the <span>Spanish-speaking world</span></h1>
      <p>Centro Hispano is an educational and cultural organisation founded on 15 December 2003 to bring the language and culture of the Spanish-speaking world to Armenia.</p>
    </div>
    {pic("860192", 620, 426, "The Center's building with its yellow doors", eager=True)}
  </div>
</section>
<section class="section" aria-label="Mission and vision">
  <div class="wrap mv">
    <article><h2>Mission</h2><p>Excellent Spanish training from beginner to advanced and professional levels, for students from anywhere, at each person’s own pace and style, with a dynamic, modern and culturally grounded method.</p><p>We teach more than the language: its cultural, historical and social richness.</p></article>
    <article><h2>Vision</h2><p>To be a leading school of Spanish as a foreign language, known for high standards, a personal approach and the ability to adapt, in person, online and hybrid.</p><p>A bridge that connects people, cultures and opportunities.</p></article>
  </div>
</section>
<section class="section sun" aria-labelledby="tl-h">
  <div class="wrap">
    <div class="head"><h2 id="tl-h">Our story, <em>year by year</em>.</h2><p>Yellow marks the milestones: founding, the first courses, the new building.</p></div>
    <ol class="timeline">{tl}</ol>
  </div>
</section>
<section class="section redfield" aria-labelledby="why-h">
  <div class="wrap">
    <div class="head"><h2 id="why-h">Ten reasons to <em>learn Spanish</em>.</h2><p>Spoken by 7.6% of the world’s population today.</p></div>
    <ol class="reasons" style="color:var(--ink)">{"".join(f"<li>{r}</li>" for r in REASONS)}</ol>
  </div>
</section>
<section class="section sun" aria-labelledby="team-h">
  <div class="wrap">
    <div class="head"><h2 id="team-h">Our <em>team</em>.</h2><p>Qualified specialists whose priority is each student’s growth as a Spanish speaker.</p></div>
    {people()}
  </div>
</section>
'''
page("nosotros.html", "nosotros.html", "About · Centro Hispano",
     "Centro Hispano, founded in 2003 in Yerevan: mission, vision, history and team.", nosotros_main)

# ---------------- contacto ----------------
contacto_main = f'''
<section class="page-hero">
  <div class="wrap">
    <div>
      <h1>Let’s talk, <span>¡hablemos!</span></h1>
      <p>Questions about a level, the next group or an event? Write, call, or come by Mashtots Avenue.</p>
    </div>
    {pic("5f8ed6", 620, 426, "Three students on bright beanbags with a laptop and books", eager=True)}
  </div>
</section>
<section class="section sun" aria-label="Contact details and form">
  <div class="wrap contact-grid">
    <div class="card-info">
      <dl>
        <div><dt>Address</dt><dd>Mashtots Avenue 52/2, Yerevan 0009</dd></div>
        <div><dt>Monday–Friday</dt><dd>10:00–21:00</dd></div>
        <div><dt>Saturday</dt><dd>11:00–19:00</dd></div>
        <div><dt>Sunday</dt><dd>Closed</dd></div>
        <div><dt>Phone</dt><dd><a href="tel:+37410547102">+374 10 547 102</a></dd></div>
        <div><dt>Mobile</dt><dd><a href="tel:+37491547102">+374 91 547 102</a> · <a href="tel:+37433547102">+374 33 547 102</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:info@centrohispano.am">info@centrohispano.am</a></dd></div>
      </dl>
      <p style="margin-top:24px"><a class="btn btn--red" href="https://maps.google.com/?q=Mashtots+Avenue+52%2F2,+Yerevan" rel="noopener">Open in Maps {ARROW}</a></p>
    </div>
    <form class="form" id="contact-form" novalidate>
      <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" autocomplete="name" required aria-describedby="e-name"><span class="err" id="e-name">Please add your name.</span></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="e-email"><span class="err" id="e-email">Please add an email we can reply to, like name@example.com.</span></div>
      <div class="field"><label for="f-subject">Subject <span>(optional)</span></label><input id="f-subject" name="subject" placeholder="e.g. B1.1 evening group"></div>
      <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required aria-describedby="e-msg"></textarea><span class="err" id="e-msg">Please write your message.</span></div>
      <div><button class="btn btn--red" type="submit">Send message {ARROW}</button></div>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''
page("contacto.html", "contacto.html", "Contact · Centro Hispano",
     "Address, opening hours, phone numbers and email of Centro Hispano in Yerevan.", contacto_main)
print("ok")

# ---------------- 404 ----------------
nf_main = f"""
<section class="nf">
  <div class="wrap nf-grid">
    <div>
      <p class="nf-code" aria-hidden="true"><span>4</span><span class="nf-zero">{pic("93fb63", 260, 260, "", eager=True, sizes="(max-width: 700px) 38vw, 260px")}</span><span>4</span></p>
      <h1>This page went <span>to the fiesta.</span></h1>
      <p class="nf-lede">The address may be mistyped, or the page has moved. Let’s get you back to class.</p>
      <div class="actions">
        <a class="btn" href="index.html">Back to home {ARROW}</a>
        <a class="btn btn--white" href="cursos.html">Courses and prices</a>
      </div>
      <p class="nf-more"><span>Or try:</span> <a href="eventos.html">Events</a> <a href="nosotros.html">About</a> <a href="contacto.html">Contact</a></p>
    </div>
  </div>
</section>
"""
page("404.html", "", "Page not found · Centro Hispano", "This page could not be found.", nf_main)
USED.clear()

# ---------------- localisation ----------------
import re, json
TEXT_RE = re.compile(r'>([^<]+)<')
ATTR_RE = re.compile(r'\b(alt|aria-label|content|placeholder|data-cap|title)="([^"]*)"')
SKIP = re.compile(r'^[\s\d.,:;+\-–—·/%×()©@|→]*$|^(A1|A2|B1\.1|B1\.2|B2\.1|B2\.2|C1|C2|AMD|DELE|Instagram|Facebook|Centro Hispano)$')

def strings(html):
    body = re.sub(r'<svg.*?</svg>', '', html, flags=re.S)
    out = []
    for m in TEXT_RE.finditer(body):
        s = m.group(1).strip()
        if s and not SKIP.match(s): out.append(s)
    for m in ATTR_RE.finditer(body):
        if m.group(1) == 'content' and not re.search(r'[a-z]{3}', m.group(2)): continue
        s = m.group(2).strip()
        if s and not SKIP.match(s) and not s.startswith(('width=', '#')): out.append(s)
    return out

HERE = pathlib.Path(__file__).parent
if len(sys.argv) > 2 and sys.argv[2] == '--extract':
    seen = []
    for f, h in PAGES.items():
        for s in strings(h):
            if s not in seen: seen.append(s)
    (HERE / 'strings.json').write_text(json.dumps(seen, ensure_ascii=False, indent=0), encoding='utf-8')
    print('strings:', len(seen)); sys.exit()

TR = {l: json.loads((HERE / f'i18n_{l}.json').read_text(encoding='utf-8')) for l in ('es', 'hy')}
LANGS = ('hy', 'en', 'es')
ROOT = 'hy'  # main language lives at the site root

def folder(l):
    return '' if l == ROOT else f'{l}/'

def hrefs(lang, file):
    up = '' if lang == ROOT else '../'
    return {l: (file if l == lang else up + folder(l) + file) for l in LANGS}

def localise(html, lang, file):
    h = hrefs(lang, file)
    for l in LANGS:
        html = html.replace(f'@@HREF_{l}@@', h[l]).replace(f'@@CUR_{l}@@', 'aria-current="true"' if l == lang else '')
    html = html.replace(f'<link rel="alternate" hreflang="{ROOT}" href="{h[ROOT]}">',
                        f'<link rel="alternate" hreflang="{ROOT}" href="{h[ROOT]}">\n<link rel="alternate" hreflang="x-default" href="{h[ROOT]}">')
    if lang != ROOT:
        html = html.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    if lang == 'en': return html, []
    d = TR[lang]; miss = []
    def tx(s):
        k = s.strip()
        if not k or SKIP.match(k): return s
        if k in d:
            return s.replace(k, d[k])
        miss.append(k); return s
    keep = []
    def stash(m):
        keep.append(m.group(0)); return f'<!--K{len(keep) - 1}-->'
    html = re.sub(r'<svg.*?</svg>|<script.*?</script>', stash, html, flags=re.S)
    sep = '.' if lang == 'es' else ' '
    def num(s):
        return re.sub(r'(\d{1,3}),(\d{3})', lambda m: m.group(1) + sep + m.group(2), s)
    html = TEXT_RE.sub(lambda m: '>' + num(tx(m.group(1))) + '<', html)
    html = ATTR_RE.sub(lambda m: f'{m.group(1)}="{tx(m.group(2))}"', html)
    html = re.sub(r'<!--K(\d+)-->', lambda m: keep[int(m.group(1))], html)
    html = html.replace('<html lang="en"', f'<html lang="{lang}"')
    if lang == 'hy':
        html = html.replace('&family=Figtree', '&family=Noto+Sans+Armenian:wght@400;500;600;700;800&family=Figtree')
    return html, miss

allmiss = {'es': set(), 'hy': set()}
for lang in LANGS:
    d = OUT / folder(lang) if folder(lang) else OUT
    d.mkdir(parents=True, exist_ok=True)
    for f, h in PAGES.items():
        out, miss = localise(h, lang, f)
        if lang != 'en': allmiss[lang].update(miss)
        if f == '404.html':  # served from any depth: make every local URL absolute
            from urllib.parse import urljoin
            base = 'http://x/' + folder(lang)
            out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|data:|/)([^"]+)"',
                         lambda m: f'{m.group(1)}="{urljoin(base, m.group(2))[len("http://x"):]}"', out)
            out = out.replace('<meta name="theme-color"', '<meta name="robots" content="noindex">' + chr(10) + '<meta name="theme-color"')
        (d / f).write_text(out, encoding='utf-8')
for l, m in allmiss.items():
    print(l, 'untranslated:', len(m), sorted(m)[:40])
