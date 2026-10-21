"""Build the graphite editorial edition. No private data or network requests.

The GIF is built separately with build_orbit_gif.cjs.
"""
from pathlib import Path
import html
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'v4'
OUT.mkdir(parents=True, exist_ok=True)
WHITE, MUTED, QUIET = '#e7edf2', '#a9b6c3', '#7f91a3'


def text(x, y, value, size=24, color=WHITE, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(value)}</text>'


def svg(name, content, height, title, width=1100):
    defs='''<defs>
    <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#171e26"/><stop offset=".6" stop-color="#10161d"/><stop offset="1" stop-color="#19212a"/></linearGradient>
    <linearGradient id="silver"><stop stop-color="#58697a" stop-opacity=".3"/><stop offset=".35" stop-color="#c2ccd5" stop-opacity=".7"/><stop offset=".75" stop-color="#667888" stop-opacity=".5"/><stop offset="1" stop-color="#58697a" stop-opacity=".15"/></linearGradient>
    <radialGradient id="glow"><stop stop-color="#c3d7e7" stop-opacity=".12"/><stop offset="1" stop-color="#c3d7e7" stop-opacity="0"/></radialGradient>
    </defs>'''
    doc=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{html.escape(title)}</title>{defs}{content}</svg>'
    ET.fromstring(doc)
    (OUT/name).write_text(doc, encoding='utf-8')


def panel(width,height):
    return f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="url(#surface)" stroke="#3c4b59" stroke-width="1.3"/>'


def particle(path,duration='9s',radius=3):
    return f'<circle r="{radius}" fill="#ecf4fb"><animateMotion path="{path}" dur="{duration}" repeatCount="indefinite"/></circle>'


def section(number,title,subtitle,name):
    s=text(0,39,number,18,QUIET,500,'letter-spacing="2"')
    s+=text(57,40,title,29,WHITE,600,'letter-spacing="1.6"')
    s+=text(1100,38,subtitle,15,MUTED,400,'text-anchor="end" letter-spacing="2"')
    s+='<path d="M0 67H1100" stroke="url(#silver)" stroke-width="1.5"/><path d="M0 71H1100" stroke="#536577" stroke-opacity=".12"/>'
    s+='<g transform="translate(1048 67)"><circle r="8" fill="#0d1117"/><path d="M-5 0L0-5 5 0 0 5Z" fill="#c5d2dd"/></g>'
    s+='<path d="M0 67H64" stroke="#d7e2eb" stroke-width="2"/>'
    s+=particle('M70 67H1030','21s',2)
    svg(name,s,92,title+' — '+subtitle)


def availability():
    s='<path d="M0 77H1100" stroke="url(#silver)"/>'
    s+='<circle cx="15" cy="32" r="6" fill="#d8e6f1"/><circle cx="15" cy="32" r="11" fill="none" stroke="#a7bdce" stroke-opacity=".3"><animate attributeName="r" values="9;15;9" dur="5s" repeatCount="indefinite"/></circle>'
    s+=text(38,40,'OPEN TO ML ENGINEERING INTERNSHIPS',23,WHITE,500,'letter-spacing="1.5"')
    s+=text(1100,39,'DSTU / ROSTOV-ON-DON',16,MUTED,400,'text-anchor="end" letter-spacing="1.7"')
    svg('availability.svg',s,80,'Open to ML engineering internships. DSTU, Rostov-on-Don.')


def deep_feature():
    s=panel(1100,348)
    s+='<path d="M30 23H1070" stroke="url(#silver)"/>'
    s+=text(34,61,'01 / FEATURED RESEARCH',17,MUTED,500,'letter-spacing="2.3"')
    s+=text(34,121,'DeepSynth Research',45,WHITE,600)
    s+=text(34,166,'Quality-aware audio-visual',27,'#c4d0da')
    s+=text(34,202,'deepfake detection.',27,'#c4d0da')
    s+=text(34,249,'MY WORK  /  FUSION METHOD + EVALUATION PIPELINE',16,MUTED,500,'letter-spacing=".6"')
    s+=text(34,280,'Research prototype · benchmark rerun pending',19,QUIET)
    s+='<path d="M34 303H1066" stroke="#425365" stroke-opacity=".6"/>'
    s+=text(34,330,'PYTORCH  /  OPENCV  /  LIBROSA',17,MUTED,400,'letter-spacing="1.1"')
    s+=text(1060,332,'SOURCE + METHODOLOGY ↗',16,WHITE,500,'text-anchor="end" letter-spacing="1"')
    s+='<g transform="translate(855 157)"><ellipse rx="165" ry="108" fill="none" stroke="#7d91a2" stroke-opacity=".22"/><ellipse rx="165" ry="70" transform="rotate(-40)" fill="none" stroke="#718797" stroke-opacity=".12"/>'
    track1='M-126-53C-61-53-63 0 12 0H130'
    track2='M-126 55C-61 55-63 0 12 0H130'
    s+=f'<path d="{track1}M-126 55C-61 55-63 0 12 0" fill="none" stroke="#9daebb" stroke-width="1.8"/>'
    s+=particle(track1,'7s',3.5)+particle(track2,'9s',3.5)
    for x,y,label in [(-126,-53,'V'),(-126,55,'A'),(12,0,'Q')]:
        s+=f'<circle cx="{x}" cy="{y}" r="25" fill="#1d2731" stroke="#a6b9c9"/>'
        s+=text(x,y+8,label,23,WHITE,500,'text-anchor="middle"')
    s+='<circle cx="132" r="8" fill="#d8e7f2"/></g>'
    s+=text(855,287,'VIDEO  +  AUDIO  +  QUALITY',15,MUTED,400,'text-anchor="middle" letter-spacing="1.3"')
    svg('featured-deepsynth.svg',s,348,'DeepSynth Research. Quality-aware audio-visual deepfake detection. Fusion method and evaluation pipeline. Research prototype; benchmark rerun pending.')


def mini_icon(kind):
    start='<g transform="translate(457 56)" fill="none" stroke="#b6c8d6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    if kind=='desktop':
        p='<rect x="-23" y="-15" width="46" height="31" rx="4"/><path d="M-8 24H8M0 16V24M-15 6L-7-3 0 3 9-7 16 6"/>'
    elif kind=='links':
        p='<rect x="-24" y="-18" width="48" height="34" rx="7"/><path d="M-15 16L-18 25-5 16M-13-5H13M-13 3H6"/>'
    elif kind=='server':
        p='<rect x="-22" y="-22" width="44" height="18" rx="4"/><rect x="-22" y="3" width="44" height="18" rx="4"/><path d="M-7-13H14M-7 12H14"/><circle cx="-14" cy="-13" r="1"/><circle cx="-14" cy="12" r="1"/>'
    else:
        p='<path d="M-23 17V-17H23V17Z M-14 9L-3-3 6 2 16-10"/><path d="M-8 23H8"/>'
    return start+p+'</g>'


def card(name,category,title,lines,contribution,stack,status,icon):
    s=panel(540,328)
    s+=text(26,48,category,15,MUTED,500,'letter-spacing="1.5"')
    s+=mini_icon(icon)
    s+=text(26,109,title,33,WHITE,600)
    for i,line in enumerate(lines):s+=text(26,150+i*29,line,22,'#c5d0da')
    s+=text(26,225,contribution,17,MUTED)
    s+='<path d="M26 248H514" stroke="#485d70" stroke-opacity=".5"/>'
    s+=text(26,276,stack,15,MUTED,400,'letter-spacing=".2"')
    s+=text(26,307,status,13,QUIET,500,'letter-spacing="1"')
    s+=text(510,309,'↗',24,WHITE,400,'text-anchor="end"')
    svg(name,s,328,title+'. '+'. '.join(lines)+'. '+contribution+'. '+status,width=540)


def workflow():
    s=panel(1100,174)
    values=[('01','ASK','A clear research question'),('02','BUILD','An inspectable implementation'),('03','CHECK','Tests and explicit limits'),('04','EXPLAIN','Reproduction steps and docs')]
    for i,(n,title,subtitle) in enumerate(values):
        x=29+i*277
        s+=text(x,42,n,15,QUIET,500,'letter-spacing="1"')
        s+=text(x,86,title,27,WHITE,600,'letter-spacing="2.5"')
        s+=text(x,130,subtitle,16,MUTED)
        if i<3:
            s+=f'<path d="M{x+195} 77H{x+238}M{x+230} 71L{x+238} 77 {x+230} 83" stroke="#6c8296" fill="none" stroke-width="1.5"/>'
    svg('workflow.svg',s,174,'What I value: a clear research question, an inspectable implementation, tests and explicit limits, reproduction steps and documentation.')


def footer():
    s='<ellipse cx="550" cy="120" rx="330" ry="112" fill="url(#glow)"/>'
    s+='<g transform="translate(550 36)"><ellipse rx="31" ry="11" transform="rotate(-18)" fill="none" stroke="#a9bece"/><ellipse rx="31" ry="11" transform="rotate(48)" fill="none" stroke="#a9bece" stroke-opacity=".4"/><circle r="4" fill="#eef4f8"/>'
    s+=particle('M31 0A31 11 0 1 1-31 0A31 11 0 1 1 31 0','12s',2.5)+'</g>'
    s+=text(550,111,"LET'S BUILD SOMETHING USEFUL.",31,WHITE,500,'text-anchor="middle" letter-spacing="3.1"')
    s+=text(550,155,'Open to ML engineering internships',23,MUTED,400,'text-anchor="middle"')
    s+=text(550,194,'COMPUTER VISION  /  MULTIMODAL LEARNING  /  LOCAL LLMS',15,QUIET,400,'text-anchor="middle" letter-spacing="1.9"')
    svg('footer.svg',s,218,"Let's build something useful. Open to ML engineering internships.")


def main():
    for number,title,subtitle,name in [
        ('01','DIRECTION','A LITTLE CONTEXT','section-about.svg'),
        ('02','SELECTED WORK','RESEARCH + ENGINEERING','section-projects.svg'),
        ('03','WORKING PRINCIPLES','FROM QUESTION TO CODE','section-workflow.svg'),
        ('04','TOOLKIT','TOOLS BEHIND THE WORK','section-tech.svg'),
        ('05','CONTACT','START A CONVERSATION','section-contact.svg')]:section(number,title,subtitle,name)
    availability();deep_feature();workflow();footer()
    cards=[
        ('card-cardora.svg','02 / DESKTOP AUTOMATION','Cardora',['Image, Photoshop and','spreadsheet workflows.'],'MY WORK / workflow + integration','PYTHON  ·  QT  ·  PHOTOSHOP','PUBLIC REPO: PRODUCT SHOWCASE','desktop'),
        ('card-bookmarks.svg','03 / APPLIED LLMS','BookMarkCore',['Telegram links turned into','organized knowledge.'],'MY WORK / Python bot + LLM pipeline','PYTHON  ·  AIOGRAM  ·  LLM API','PUBLIC CODE','links'),
        ('card-local-llm.svg','04 / LOCAL INFERENCE','Local LLM Lab',['Local roleplay models with','a focused chat interface.'],'MY WORK / CleanUI + local/LAN setup','JAVASCRIPT  ·  LOCAL MODEL APIS','BUILT AROUND UPSTREAM SILLYTAVERN','server'),
        ('card-eco.svg','05 / APPLICATION ENGINEERING','Eco Banking Tracker',['An educational full-stack','finance dashboard.'],'MY WORK / React + Express prototype','REACT  ·  TYPESCRIPT  ·  SQLITE','SIMULATED FINANCE DATA','chart')]
    for args in cards:card(*args)
    for name in ['toolbelt.svg','activity.svg','contact-telegram.svg','contact-research.svg','contact-repos.svg','contact-russian.svg']:
        shutil.copy2(ROOT/'assets/v3'/name,OUT/name)
    (OUT/'DESIGN-NOTES.txt').write_text('Original graphite/silver editorial layout. Astronaut source: built-in image_gen; scene, orbit and seamless GIF motion authored programmatically. Source alpha and body pose preserved. No copied third-party GIFs or live-stat services. SVG diagrams are descriptive illustrations, not measurements. Activity chart remains an explicitly dated historical API snapshot. Tool icons from Simple Icons, CC0-1.0; see ../v3/icons/LICENSE.md.\n',encoding='utf-8')
    print('Built',len(list(OUT.glob('*.svg'))),'editorial SVG assets.')


if __name__=='__main__':main()
