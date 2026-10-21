"""Build the profile's self-contained SVG layout from a GitHub data snapshot.

Usage: python tools/build_visuals.py --stats /path/to/github-api-snapshot.json
No external SVG images, scripts, trackers or runtime dependencies are required.
"""
from pathlib import Path
from collections import Counter
import argparse
import html
import json
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'v2'
OUT.mkdir(exist_ok=True, parents=True)
WHITE = '#edf0fa'
MUTED = '#a9b2c8'
VIOLET = '#bc9bfa'


def text(x, y, value, size=24, color=WHITE, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(str(value))}</text>'


def svg(name, content, height, title, width=1100):
    head = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title, quote=True)}">
<title>{html.escape(title)}</title><defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1b2033"/><stop offset=".55" stop-color="#121723"/><stop offset="1" stop-color="#1b172b"/></linearGradient>
<linearGradient id="line"><stop stop-color="#7e6eae" stop-opacity="0"/><stop offset=".5" stop-color="#c7a7ff" stop-opacity=".8"/><stop offset="1" stop-color="#7e6eae" stop-opacity="0"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#a57ce7" stop-opacity=".24"/><stop offset="1" stop-color="#986ade" stop-opacity="0"/></radialGradient>
<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#af8ee5" stop-opacity=".4"/><stop offset="1" stop-color="#af8ee5" stop-opacity="0"/></linearGradient>
</defs>'''
    body = head + content + '</svg>'
    ET.fromstring(body)
    (OUT / name).write_text(body, encoding='utf-8')


def panel(height):
    return f'<rect x="1" y="1" width="1098" height="{height-2}" rx="22" fill="url(#panel)" stroke="#3a3a52"/><ellipse cx="965" cy="{height/2}" rx="220" ry="{height}" fill="url(#glow)"/>'


def section(number, title, subtitle, filename):
    content = '<path d="M0 69H1100" stroke="url(#line)"/>'
    content += text(0, 39, number, 18, VIOLET, 500, 'letter-spacing="3"')
    content += text(60, 40, title, 30, WHITE, 600, 'letter-spacing="1.4"')
    content += text(1100, 38, subtitle, 17, MUTED, 400, 'text-anchor="end" letter-spacing="2"')
    svg(filename, content, 86, title)


def draw_deep():
    s = '<g transform="translate(785 115)">'
    s += '<ellipse rx="132" ry="77" fill="none" stroke="#65597d" stroke-opacity=".5"/>'
    s += '<ellipse rx="83" ry="119" transform="rotate(60)" fill="none" stroke="#a98ddd" stroke-opacity=".25"/>'
    s += '<path d="M-117-37C-40-37-55 0 20 0M-117 47C-40 47-55 0 20 0" stroke="#b99eea" stroke-width="2" fill="none"/>'
    s += '<path d="M20 0H127" stroke="#d4c4f0" stroke-width="2" stroke-dasharray="5 14"><animate attributeName="stroke-dashoffset" from="0" to="-95" dur="6s" repeatCount="indefinite"/></path>'
    for x, y, label in [(-117,-37,'V'),(-117,47,'A'),(23,0,'Q')]:
        s += f'<circle cx="{x}" cy="{y}" r="25" fill="#242435" stroke="#9d88c2"/>' + text(x,y+7,label,21,WHITE,500,'text-anchor="middle"')
    s += '<circle cx="130" r="7" fill="#d2b9fa"><animate attributeName="opacity" values=".45;1;.45" dur="4s" repeatCount="indefinite"/></circle></g>'
    return s


def draw_cardora():
    s = '<g transform="translate(735 55)">'
    s += '<rect x="0" y="15" width="118" height="99" rx="10" fill="#282538" stroke="#9b81b8"/><path d="M12 100L42 62 62 78 85 48 106 100Z" fill="#84719f"/><circle cx="32" cy="40" r="9" fill="#dfc7b4"/>'
    s += '<path d="M127 64H154" stroke="#c7b2e7" stroke-width="2"/><path d="M148 58L155 64 148 70" fill="none" stroke="#c7b2e7" stroke-width="2"/>'
    s += '<rect x="165" y="-4" width="140" height="124" rx="10" fill="#1c2431" stroke="#8799b3"/>'
    s += '<path d="M178 22H290M178 48H290M178 74H290M178 100H290M211 12V110M251 12V110" stroke="#576178"/>'
    s += '<rect x="178" y="34" width="25" height="9" rx="2" fill="#af8cde"/><rect x="219" y="60" width="24" height="9" rx="2" fill="#cbafec"/><rect x="259" y="86" width="25" height="9" rx="2" fill="#a3b9c8"/></g>'
    return s


def draw_bookmarks():
    s = '<g transform="translate(720 54)"><rect x="0" y="7" width="102" height="76" rx="16" fill="#202e3d" stroke="#8dadd1"/><path d="M18 81L14 103 40 83" fill="#202e3d" stroke="#8dadd1"/><path d="M25 30H78M25 45H65M25 60H72" stroke="#a2b8cf" stroke-width="3" stroke-linecap="round"/>'
    s += '<path d="M113 49H151M202 49H237" stroke="#b49ad8" stroke-dasharray="4 8"><animate attributeName="stroke-dashoffset" from="0" to="-48" dur="5s" repeatCount="indefinite"/></path>'
    s += '<path d="M177 25L201 49 177 73 153 49Z" fill="#30253f" stroke="#ba9fdf"/>'
    s += '<rect x="247" y="-8" width="85" height="121" rx="10" fill="#1e2635" stroke="#8e9db5"/><path d="M266 17H312M266 43H312M266 69H304M266 95H311" stroke="#9faac1" stroke-width="3"/></g>'
    return s


def draw_local():
    s = '<g transform="translate(780 112)"><ellipse rx="106" ry="70" fill="none" stroke="#76648e"/>'
    s += '<ellipse rx="106" ry="70" transform="rotate(65)" fill="none" stroke="#7e6a9d" stroke-opacity=".5"/>'
    for y in [-47,-9,29]:
        s += f'<rect x="-57" y="{y}" width="114" height="28" rx="7" fill="#252337" stroke="#b09ccf"/><circle cx="-39" cy="{y+14}" r="3" fill="#cfb8f0"/><path d="M-23 {y+14}H38" stroke="#827390"/>'
    s += '<circle cx="106" r="5" fill="#e6d3ff"><animate attributeName="opacity" values=".3;1;.3" dur="3.8s" repeatCount="indefinite"/></circle></g>'
    return s


def draw_eco():
    s='<g transform="translate(716 55)"><rect width="157" height="102" rx="12" fill="#233136" stroke="#809c9e"/>'
    s+='<path d="M22 77L48 61 76 70 103 40 134 25" stroke="#9ac2bd" stroke-width="3" fill="none"/><path d="M22 86H136" stroke="#536568"/>'
    s+='<path d="M232 113C202 75 207 16 282 0 289 67 267 102 232 113Z" fill="#374746" stroke="#a5bfac"/><path d="M230 104L266 28M246 74L270 67M240 89L226 60" fill="none" stroke="#afc5b9" stroke-width="2"/></g>'
    return s


def project(filename, number, title, subtitle, stack, category, drawing, highlight=False):
    s=panel(218)
    s+='<path d="M27 24H1070" stroke="url(#line)"/>'
    s+=text(35, 49, number+' / '+category, 17, VIOLET, 500,'letter-spacing="2.5"')
    s+=text(35, 103, title, 40, WHITE,600)
    s+=text(35, 141, subtitle, 23, '#c3c9d8')
    s+=text(35, 184, stack, 19, MUTED,400,'letter-spacing=".3"')
    s+=drawing()
    s+=text(1062, 193, '↗', 29, '#cab1ec',400,'text-anchor="end"')
    svg(filename,s,218,title+' — '+subtitle)


def toolbelt():
    rows=[
        [('python','Python','#5eabdc'),('pytorch','PyTorch','#ee775d'),('opencv','OpenCV','#a791f5'),('numpy','NumPy','#74b7cf'),('pandas','pandas','#c5a6e8'),('scikitlearn','scikit-learn','#e0ac72')],
        [('typescript','TypeScript','#73a7dc'),('react','React','#80c9dd'),('nodedotjs','Node.js','#97bb89'),('sqlite','SQLite','#8fb7d5'),('git','Git','#df8b76'),('javascript','JavaScript','#d0bd7b')],
    ]
    s=panel(370)
    for row,icons in enumerate(rows):
        s+=text(30,39+row*177,'ML & DATA' if row==0 else 'APPLICATIONS & TOOLS',16,MUTED,500,'letter-spacing="2"')
        for col,(slug,label,color) in enumerate(icons):
            x=25+col*177; y=58+row*177
            s+=f'<rect x="{x}" y="{y}" width="165" height="108" rx="12" fill="#1b2030" stroke="#34394d"/>'
            icon=ET.parse(OUT/'icons'/f'{slug}.svg').getroot()
            paths=''.join(ET.tostring(p,encoding='unicode') for p in icon if p.tag.endswith('path'))
            s+=f'<g transform="translate({x+60} {y+13}) scale(1.9)" fill="{color}">{paths}</g>'
            s+=text(x+82.5,y+91,label,21,WHITE,400,'text-anchor="middle"')
    svg('toolbelt.svg',s,370,'ML tools: Python, PyTorch, OpenCV, NumPy, pandas, scikit-learn. Applications: TypeScript, React, Node.js, SQLite, Git, JavaScript.')


def buttons():
    labels=[('contact-telegram.svg','TELEGRAM','M30 31L48 24 43 44 37 35 32 36 30 31Z M37 35L45 28'),('contact-research.svg','RESEARCH','M27 26H49V43H27Z M32 31H44M32 36H41'),('contact-repos.svg','PROJECTS','M27 25H36L39 29H49V43H27Z'),('contact-russian.svg','РУССКИЙ','M27 27H49V42H27Z M32 31H44M32 36H41')]
    for filename,label,path in labels:
        body='<rect x="1" y="1" width="208" height="66" rx="12" fill="#171b2a" stroke="#514263"/>'
        body+=f'<path d="{path}" fill="none" stroke="#c2a6e6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        body+=text(68,40,label,16,WHITE,500,'letter-spacing="1"')
        svg(filename,body,68,label,width=210)


def signal():
    s='<circle cx="250" cy="25" r="10" fill="#aa8bcf" opacity=".22"><animate attributeName="r" values="8;16;8" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".2;.07;.2" dur="4s" repeatCount="indefinite"/></circle><circle cx="250" cy="25" r="4" fill="#dbcbf0"/>'
    s+=text(550,32,'OPEN TO ML ENGINEERING INTERNSHIPS',23,'#c6b2e8',500,'text-anchor="middle" letter-spacing="2.3"')
    svg('availability.svg',s,54,'Open to ML engineering internships')


def activity(data):
    user=data['data']['user']; cal=user['contributionsCollection']['contributionCalendar']
    months=Counter()
    for week in cal['weeks']:
        for day in week['contributionDays']:
            months[day['date'][:7]]+=day['contributionCount']
    keys=sorted(months)[-12:];values=[months[k] for k in keys]
    s=panel(390)
    s+=text(34,50,'GITHUB / ACTIVITY',20,VIOLET,500,'letter-spacing="2"')
    s+=text(35,139,cal['totalContributions'],72,WHITE,500)
    s+=text(35,174,'contributions in the last year',20,MUTED)
    s+=text(35,259,user['publicRepositories']['totalCount'],57,WHITE,500)
    s+=text(35,292,'public repositories',20,MUTED)
    s+='<path d="M350 45V325" stroke="#464059"/>'
    x0,x1,y0,y1=400,1055,105,283; vmax=max(values) or 1
    points=[(x0+i*(x1-x0)/(len(values)-1), y1-v/vmax*(y1-y0)) for i,v in enumerate(values)]
    for y in [105,164,223,283]:s+=f'<path d="M400 {y}H1055" stroke="#4c435c" stroke-opacity=".4" stroke-dasharray="3 9"/>'
    line=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    s+=f'<polygon points="400,283 {line} 1055,283" fill="url(#area)"/><polyline points="{line}" fill="none" stroke="#bea0ec" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    for (x,y),v,k in zip(points,values,keys):
        s+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#e0ccff"><title>{k}: {v} contributions</title></circle>'
        label=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'][int(k[-2:])-1]
        s+=text(round(x,2),310,label,14,MUTED,400,'text-anchor="middle"')
    s+=text(400,64,'MONTHLY CONTRIBUTIONS',17,MUTED,500,'letter-spacing="1.4"')
    s+=text(35,359,'SOURCE: GITHUB  /  SNAPSHOT: 21 OCT 2026',15,'#929ab1',400,'letter-spacing="1.2"')
    svg('activity.svg',s,390,'GitHub activity: '+str(cal['totalContributions'])+' contributions in the last year, '+str(user['publicRepositories']['totalCount'])+' public repositories. Snapshot 21 October 2026.')


def footer():
    s='<path d="M0 1H1100" stroke="url(#line)"/><ellipse cx="550" cy="121" rx="270" ry="100" fill="url(#glow)"/>'
    s+='<g transform="translate(550 38)"><ellipse rx="29" ry="10" fill="none" stroke="#b196d6"/><ellipse rx="29" ry="10" transform="rotate(65)" fill="none" stroke="#b196d6" stroke-opacity=".6"/><circle r="4" fill="#e0cafa"/></g>'
    s+=text(550,105,'RESEARCH. BUILD. ITERATE.',31,WHITE,500,'text-anchor="middle" letter-spacing="4"')
    s+=text(550,148,'Computer vision  /  Multimodal learning  /  Applied LLMs',20,MUTED,400,'text-anchor="middle"')
    svg('footer.svg',s,185,'Research. Build. Iterate. Computer vision, multimodal learning, applied LLMs.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stats',type=Path,required=True);args=parser.parse_args()
    for number,title,subtitle,filename in [('01','ABOUT ME','DENIS / GALAXY','section-about.svg'),('02','SELECTED PROJECTS','RESEARCH & ENGINEERING','section-projects.svg'),('03','TECHNOLOGIES','MY TOOLKIT','section-tech.svg'),('04','ACTIVITY','FROM GITHUB','section-activity.svg')]:section(number,title,subtitle,filename)
    project('project-deepsynth.svg','01','DeepSynth','Quality-aware audio-visual deepfake detection','PYTORCH  /  OPENCV  /  LIBROSA','RESEARCH',draw_deep)
    project('project-cardora.svg','02','Cardora','A desktop workflow for images and product content','PYTHON  /  QT  /  PHOTOSHOP  /  EXCEL','APPLICATION SHOWCASE',draw_cardora)
    project('project-bookmarks.svg','03','BookMarkCore','From Telegram links to an organized knowledge page','PYTHON  /  AIOGRAM  /  LLM API  /  GITHUB','APPLIED LLM',draw_bookmarks)
    project('project-local-llm.svg','04','Local LLM Lab','Local roleplay models and a focused chat interface','SILLYTAVERN INTEGRATION  /  JAVASCRIPT','LOCAL INFERENCE',draw_local)
    project('project-eco.svg','05','Eco Banking Tracker','An educational full-stack finance dashboard','REACT  /  TYPESCRIPT  /  EXPRESS  /  SQLITE','FULL-STACK PROTOTYPE',draw_eco)
    toolbelt();buttons();signal();activity(json.loads(args.stats.read_text(encoding='utf-8')));footer()
    (OUT/'DESIGN-NOTES.txt').write_text('Custom native SVG layout and diagrams by the profile owner with Codex assistance. Technology paths: Simple Icons, CC0-1.0; see icons/LICENSE.md. GitHub activity is a dated API snapshot, not a fabricated score. Artwork files are separately generated. SVG animation uses only decorative paths and opacity, no JavaScript or external resources.\n',encoding='utf-8')
    print('Generated',len(list(OUT.glob('*.svg'))),'self-contained SVG assets.')


if __name__=='__main__':main()
