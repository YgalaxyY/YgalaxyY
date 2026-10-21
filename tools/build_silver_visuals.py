"""Graphite/silver edition of the profile's native SVG assets.

python tools/build_silver_visuals.py --stats /path/to/github-snapshot.json
The header photograph is embedded inline so the SVG requires no external image requests.
"""
from pathlib import Path
import argparse
import base64
import json
import re
import shutil
import xml.etree.ElementTree as ET
import build_visuals as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'v3'
OUT.mkdir(exist_ok=True, parents=True)
base.OUT = OUT
original_svg = base.svg


def steel_color(match):
    value=match.group(0)[1:]
    r,g,b=(int(value[i:i+2],16) for i in (0,2,4))
    light=.2126*r+.7152*g+.0722*b
    return '#'+''.join(f'{max(0,min(255,round(light*k))):02x}' for k in (.965,.995,1.035))


def silver_svg(name,content,height,title,width=1100):
    if name=='toolbelt.svg':
        content=re.sub(r'(<g transform="translate\([^\"]+scale\(1\.9\)" fill=")[^"]+',r'\g<1>#d9dfe5',content)
    original_svg(name,content,height,title,width)
    path=OUT/name
    markup=re.sub(r'#[0-9a-fA-F]{6}\b',steel_color,path.read_text(encoding='utf-8'))
    ET.fromstring(markup)
    path.write_text(markup,encoding='utf-8')


base.svg=silver_svg


def particle(path,duration,begin='0s',radius=3.5):
    return f'<circle r="{radius}" fill="#edf3fa"><animateMotion path="{path}" dur="{duration}" begin="{begin}" repeatCount="indefinite"/><animate attributeName="opacity" values=".15;.85;.15" dur="{duration}" begin="{begin}" repeatCount="indefinite"/></circle>'


def deep_motion():
    s=base.draw_deep()
    s+='<g transform="translate(785 115)">'
    s+=particle('M-117-37C-40-37-55 0 20 0H127','7s')
    s+=particle('M-117 47C-40 47-55 0 20 0H127','9s','-3s')
    s+='</g>'
    return s


def cardora_motion():
    s=base.draw_cardora()
    s+='<g transform="translate(735 55)">'
    s+=particle('M127 64H154','4.5s',radius=2.5)
    for i,(x,y) in enumerate([(178,34),(219,60),(259,86)]):
        s+=f'<rect x="{x}" y="{y}" width="25" height="9" rx="2" fill="#f0f5fa" opacity="0"><animate attributeName="opacity" values="0;0;.85;0;0" dur="7s" begin="-{i*2}s" repeatCount="indefinite"/></rect>'
    s+='</g>'
    return s


def bookmark_motion():
    return base.draw_bookmarks()+'<g transform="translate(720 54)">'+particle('M113 49H237','6s',radius=3)+'</g>'


def local_motion():
    s=base.draw_local()
    s+='<g transform="translate(780 112)"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="26s" repeatCount="indefinite"/><ellipse rx="106" ry="70" fill="none" stroke="#bbc7d1" stroke-opacity=".15"/><circle cx="106" r="5" fill="#dde5eb"/></g></g>'
    return s


def eco_motion():
    return base.draw_eco()+'<g transform="translate(716 55)">'+particle('M22 77L48 61 76 70 103 40 134 25','9s',radius=3)+'</g>'


def intro():
    s=base.panel(120)
    s+='<g transform="translate(142 60)"><circle r="8" fill="#e7edf2"/><ellipse rx="84" ry="28" transform="rotate(-12)" stroke="#a4b3c1" stroke-width="1.2" fill="none"/><ellipse rx="69" ry="32" transform="rotate(48)" stroke="#9babb9" stroke-opacity=".35" fill="none"/>'
    s+=particle('M84 0A84 28 0 1 1-84 0A84 28 0 1 1 84 0','17s',radius=4)
    s+='</g>'
    s+=base.text(300,52,'OPEN TO ML ENGINEERING INTERNSHIPS',25,'#dce4eb',500,'letter-spacing="1.8"')
    s+=base.text(300,83,'COMPUTER VISION  /  MULTIMODAL LEARNING',16,'#9eabb8',400,'letter-spacing="2"')
    for x,y in [(944,32),(988,76),(1032,44),(1065,88)]:
        s+=f'<circle cx="{x}" cy="{y}" r="2" fill="#cdd8e2"><animate attributeName="opacity" values=".2;.85;.2" dur="{5+(x%3)}s" repeatCount="indefinite"/></circle>'
    base.svg('availability.svg',s,120,'Open to ML engineering internships. Animated orbital signal.')


def header():
    data=base64.b64encode((OUT/'hero.jpg').read_bytes()).decode('ascii')
    s=f'<image x="0" y="0" width="2172" height="724" href="data:image/jpeg;base64,{data}"/>'
    s+='<defs><radialGradient id="star-glow"><stop stop-color="#e8f0f7" stop-opacity=".65"/><stop offset="1" stop-color="#dce8f5" stop-opacity="0"/></radialGradient></defs>'
    stars=[(887,67),(1047,134),(1229,85),(1326,181),(1469,93),(1074,249),(876,205),(1580,36)]
    for i,(x,y) in enumerate(stars):
        s+=f'<g transform="translate({x} {y})"><circle r="12" fill="url(#star-glow)"><animate attributeName="opacity" values=".05;.4;.05" dur="{5+i%4}s" begin="-{i%5}s" repeatCount="indefinite"/></circle><circle r="1.5" fill="#f4f8fc"><animate attributeName="opacity" values=".25;.9;.25" dur="{5+i%4}s" begin="-{i%5}s" repeatCount="indefinite"/></circle></g>'
    track='M930 427C1102 233 1322 136 1638 49'
    s+=f'<path d="{track}" fill="none" stroke="#d3e0ec" stroke-width=".7" stroke-opacity=".15"/>'
    s+=particle(track,'22s',radius=4)
    base.svg('hero-animated.svg',s,724,'Denis Bm — Machine Learning / Computer Vision. Graphite and silver galaxy with softly moving stars.',width=2172)


def animated_sections():
    for name in ['section-about.svg','section-projects.svg','section-tech.svg','section-activity.svg']:
        p=OUT/name;s=p.read_text(encoding='utf-8')
        accent='<circle cy="69" r="2.3" fill="#d8e1e9" opacity=".6"><animate attributeName="cx" from="-10" to="1110" dur="18s" repeatCount="indefinite"/></circle>'
        s=s.replace('</svg>',accent+'</svg>');ET.fromstring(s);p.write_text(s,encoding='utf-8')


def animated_footer():
    p=OUT/'footer.svg';s=p.read_text(encoding='utf-8')
    star='<g transform="translate(550 38)">'+particle('M29 0A29 10 0 1 1-29 0A29 10 0 1 1 29 0','12s',radius=2)+'</g>'
    s=s.replace('</svg>',star+'</svg>');ET.fromstring(s);p.write_text(s,encoding='utf-8')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stats',type=Path,required=True);args=parser.parse_args()
    if not (OUT/'icons').exists():shutil.copytree(ROOT/'assets/v2/icons',OUT/'icons')
    for number,title,subtitle,filename in [('01','ABOUT ME','DENIS / GALAXY','section-about.svg'),('02','SELECTED PROJECTS','RESEARCH & ENGINEERING','section-projects.svg'),('03','TECHNOLOGIES','MY TOOLKIT','section-tech.svg'),('04','ACTIVITY','FROM GITHUB','section-activity.svg')]:base.section(number,title,subtitle,filename)
    projects=[('project-deepsynth.svg','01','DeepSynth','Quality-aware audio-visual deepfake detection','PYTORCH  /  OPENCV  /  LIBROSA','RESEARCH',deep_motion),('project-cardora.svg','02','Cardora','A desktop workflow for images and product content','PYTHON  /  QT  /  PHOTOSHOP  /  EXCEL','APPLICATION SHOWCASE',cardora_motion),('project-bookmarks.svg','03','BookMarkCore','From Telegram links to an organized knowledge page','PYTHON  /  AIOGRAM  /  LLM API  /  GITHUB','APPLIED LLM',bookmark_motion),('project-local-llm.svg','04','Local LLM Lab','Local roleplay models and a focused chat interface','SILLYTAVERN INTEGRATION  /  JAVASCRIPT','LOCAL INFERENCE',local_motion),('project-eco.svg','05','Eco Banking Tracker','An educational full-stack finance dashboard','REACT  /  TYPESCRIPT  /  EXPRESS  /  SQLITE','FULL-STACK PROTOTYPE',eco_motion)]
    for values in projects:base.project(*values)
    base.toolbelt();base.buttons();intro();base.activity(json.loads(args.stats.read_text(encoding='utf-8')));base.footer();header();animated_sections();animated_footer()
    (OUT/'DESIGN-NOTES.txt').write_text('Graphite and cold silver edition. Header artwork is the user-selected reference, embedded in an SVG with decorative star and orbit motion. The original raster is preserved. Card, section and orbital animation uses native SVG, no JavaScript or external resources. Icons: Simple Icons, CC0-1.0; see icons/LICENSE.md. Activity is a dated real GitHub snapshot.\n',encoding='utf-8')
    print('Built',len(list(OUT.glob('*.svg'))),'silver SVG assets.')


if __name__=='__main__':main()
