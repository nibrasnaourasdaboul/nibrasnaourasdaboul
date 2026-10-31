# Generates all animated SVG assets. Edit the DATA section, then run: python3 tools/gen_assets.py
import random, math
random.seed(3)
A='assets/'
# ---------------- DATA (replace with real numbers) ----------------
STATS=[('Total Stars','128',.55,'#fbbf24'),('Total Commits','1,450',.9,'#a78bfa'),('Pull Requests','64',.35,'#22d3ee'),('Issues','37',.25,'#f472b6'),('Repositories','42',.45,'#34d399')]
LANGS=[('Python','38%',.38,'#3776ab'),('JavaScript','18%',.18,'#f7df1e'),('PHP','14%',.14,'#8892bf'),('Dart','12%',.12,'#22d3ee'),('SQL / PLSQL','10%',.10,'#f97316'),('Shell','8%',.08,'#4ade80')]
TROPHIES=[('Commits','SSS','#fbbf24'),('Stars','S','#a78bfa'),('Followers','A+','#22d3ee'),('Repos','AA','#34d399'),('PRs','A','#f472b6'),('Streak','S+','#fb923c')]
ACT=[3,5,2,8,6,9,4,7,12,10,6,14,9,11,8,15,13,10,17,12,9,14,18,16,11,13,19,15,20,17]
# -------------------------------------------------------------------
import json, os
BADGE='Live ✦ Demo'
if os.path.exists('data.json'):
    _d=json.load(open('data.json'));STATS=_d['stats'];LANGS=_d['langs'];TROPHIES=_d['trophies'];ACT=_d['activity'];BADGE='Updated '+_d['updated']
def wr(n,W,H,body,defs=''):
    s=(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}'
    '<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#22d3ee"/></linearGradient>'
    '<linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>'
    '<filter id="f" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    f'{body}</svg>')
    open(A+n,'w').write(s)
FONT='font-family="Segoe UI,Arial,sans-serif"'
# 1. HEADER
def header():
    W,H=1200,260
    d='<linearGradient id="bgh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset=".5" stop-color="#1e1b4b"/><stop offset="1" stop-color="#311b92"/></linearGradient><linearGradient id="sw"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".14"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    b=f'<rect width="{W}" height="{H}" fill="url(#bgh)"/>'
    for _ in range(50):
        x=random.randint(0,W);y=random.randint(10,200);r=random.uniform(1,3);t=random.uniform(3,7)
        b+=f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#c4b5fd"><animate attributeName="cy" values="{y};{y-25};{y}" dur="{t:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".2;1;.2" dur="{t:.1f}s" repeatCount="indefinite"/></circle>'
    for col,op,v in (('#7c3aed',.35,('M0 205 C300 165 600 245 900 205 S1200 175 1200 205 V260 H0Z','M0 215 C300 245 600 165 900 215 S1200 245 1200 215 V260 H0Z')),('#22d3ee',.25,('M0 225 C300 250 600 200 900 230 S1200 205 1200 230 V260 H0Z','M0 230 C300 205 600 250 900 225 S1200 250 1200 225 V260 H0Z'))):
        b+=f'<path d="{v[0]}" fill="{col}" opacity="{op}"><animate attributeName="d" values="{v[0]};{v[1]};{v[0]}" dur="7s" repeatCount="indefinite"/></path>'
    b+=f'<text x="600" y="108" text-anchor="middle" {FONT} font-size="54" font-weight="800" fill="url(#g)" filter="url(#f)">Nibras Daboul  ✦  Dana Hajjar<animate attributeName="opacity" values="1;.82;1" dur="3s" repeatCount="indefinite"/></text>'
    b+=f'<text x="600" y="152" text-anchor="middle" {FONT} font-size="21" fill="#e0e7ff" letter-spacing="2">Information Technology Engineers  •  AI &amp; Intelligence Systems</text>'
    b+=f'<text x="600" y="186" text-anchor="middle" {FONT} font-size="15" fill="#94a3b8" letter-spacing="3">DEEP LEARNING  ·  FULL-STACK  ·  DATABASES  ·  DEVOPS</text>'
    b+='<rect y="0" width="160" height="260" fill="url(#sw)"><animate attributeName="x" values="-200;1300" dur="5s" repeatCount="indefinite"/></rect>'
    wr('header.svg',W,H,b,d)
# 2/3. BAR CARDS
def bars(fn,title,rows,badge):
    W=560;H=70+len(rows)*36
    b=f'<rect width="{W}" height="{H}" rx="16" fill="url(#card)" stroke="#4c1d95"/>'
    b+=f'<text x="24" y="38" {FONT} font-size="20" font-weight="700" fill="url(#g)">{title}</text>'
    b+=f'<rect x="{W-110}" y="18" width="86" height="26" rx="13" fill="#7c3aed" opacity=".25"><animate attributeName="opacity" values=".15;.5;.15" dur="2.5s" repeatCount="indefinite"/></rect><text x="{W-67}" y="36" text-anchor="middle" {FONT} font-size="13" fill="#ddd6fe">{badge}</text>'
    for i,(l,v,fr,c) in enumerate(rows):
        y=68+i*36;w=round(290*fr/max(r[2] for r in rows),1)
        b+=f'<text x="24" y="{y+10}" {FONT} font-size="14" fill="#cbd5e1">{l}</text><rect x="170" y="{y}" width="290" height="12" rx="6" fill="#1e293b"/>'
        b+=f'<rect x="170" y="{y}" height="12" rx="6" fill="{c}" filter="url(#f)"><animate attributeName="width" values="0;{w};{w};0" keyTimes="0;.25;.9;1" dur="8s" begin="{i*.2}s" repeatCount="indefinite"/></rect>'
        b+=f'<text x="{W-24}" y="{y+11}" text-anchor="end" {FONT} font-size="14" font-weight="700" fill="{c}">{v}</text>'
    wr(fn,W,H,b)
# 4. TROPHIES
def trophies():
    W,H=840,190;b=f'<rect width="{W}" height="{H}" rx="16" fill="url(#card)" stroke="#4c1d95"/>'
    for i,(n,r,c) in enumerate(TROPHIES):
        x=20+i*134;cx=x+57
        b+=f'<rect x="{x}" y="22" width="114" height="146" rx="14" fill="#0b1020" stroke="{c}" stroke-opacity=".5"/>'
        b+=(f'<g transform="translate({cx},78)"><animateTransform attributeName="transform" type="translate" values="{cx},78;{cx},70;{cx},78" dur="{3+i*.4}s" repeatCount="indefinite"/>'
            f'<path d="M-22 -26h44v18a22 22 0 0 1 -44 0z" fill="{c}" filter="url(#f)"/><path d="M-22 -20h-10a10 12 0 0 0 12 20M22 -20h10a10 12 0 0 1 -12 20" fill="none" stroke="{c}" stroke-width="4"/>'
            f'<rect x="-5" y="12" width="10" height="14" fill="{c}"/><rect x="-18" y="26" width="36" height="8" rx="3" fill="{c}"/>'
            '<path d="M0 -16l3 7h7l-5.500 4 2 7-6.500-4.500-6.500 4.500 2-7-5.500-4h7z" fill="#0b1020" opacity=".55"/></g>')
        b+=f'<rect x="{x}" y="22" width="30" height="146" rx="14" fill="url(#sw2)"><animate attributeName="x" values="{x-40};{x+120};{x+120}" dur="4s" begin="{i*.5}s" repeatCount="indefinite"/></rect>'
        b+=f'<text x="{cx}" y="132" text-anchor="middle" {FONT} font-size="20" font-weight="800" fill="{c}">{r}</text><text x="{cx}" y="154" text-anchor="middle" {FONT} font-size="13" fill="#94a3b8">{n}</text>'
    d='<linearGradient id="sw2"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".2"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    wr('trophies.svg',W,H,b,d)
# 5. ACTIVITY
def activity():
    W,H=840,260;L,R,T,B=50,810,50,210;mx=max(ACT)+2
    pts=[(L+i*(R-L)/(len(ACT)-1),B-(v/mx)*(B-T)) for i,v in enumerate(ACT)]
    line='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
    ln=sum(math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1))+10
    b=f'<rect width="{W}" height="{H}" rx="16" fill="url(#card)" stroke="#4c1d95"/><text x="24" y="34" {FONT} font-size="20" font-weight="700" fill="url(#g)">Contribution Activity · Last 30 Days</text>'
    for k in range(5):
        y=T+k*(B-T)/4;b+=f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="#334155" stroke-dasharray="3 6"/><text x="{L-10}" y="{y+4}" text-anchor="end" {FONT} font-size="11" fill="#64748b">{round(mx-k*mx/4)}</text>'
    b+=f'<path d="{line} L{R} {B} L{L} {B}Z" fill="url(#ar)"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.2;.5;.9;1" dur="8s" repeatCount="indefinite"/></path>'
    b+=f'<path d="{line}" fill="none" stroke="url(#g)" stroke-width="3.500" stroke-linejoin="round" stroke-dasharray="{ln:.0f}" filter="url(#f)"><animate attributeName="stroke-dashoffset" values="{ln:.0f};0;0;{ln:.0f}" keyTimes="0;.45;.9;1" dur="8s" repeatCount="indefinite"/></path>'
    for x,y in pts[::3]:b+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.500" fill="#0b1020" stroke="#22d3ee" stroke-width="2"/>'
    x,y=pts[-1];b+=f'<circle cx="{x}" cy="{y}" r="6" fill="#22d3ee"><animate attributeName="r" values="5;12;5" dur="1.600s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.2;1" dur="1.600s" repeatCount="indefinite"/></circle>'
    d='<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c3aed" stop-opacity=".5"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></linearGradient>'
    wr('activity.svg',W,H,b,d)
# 6. ANIMATED PIPELINE DIAGRAM
def pipeline():
    W,H=900,230;N=[('Data','📥','#a78bfa'),('Model','🧠','#818cf8'),('API','⚙️','#38bdf8'),('UI','🎨','#22d3ee'),('Users','👤','#34d399')]
    b=f'<rect width="{W}" height="{H}" rx="16" fill="url(#card)" stroke="#4c1d95"/>';xs=[90+i*180 for i in range(5)]
    for i in range(4):
        x1,x2=xs[i]+38,xs[i+1]-38;b+=f'<line x1="{x1}" y1="105" x2="{x2}" y2="105" stroke="#334155" stroke-width="3"/>'
        for k in range(2):b+=f'<circle r="5" fill="{N[i][2]}" filter="url(#f)"><animateMotion path="M{x1} 105 L{x2} 105" dur="2s" begin="{k+i*.3}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="2s" begin="{k+i*.3}s" repeatCount="indefinite"/></circle>'
    for (n,e,c),x in zip(N,xs):
        b+=f'<circle cx="{x}" cy="105" r="38" fill="#0b1020" stroke="{c}" stroke-width="3" filter="url(#f)"/><circle cx="{x}" cy="105" r="38" fill="none" stroke="{c}"><animate attributeName="r" values="38;56;38" dur="3s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0;.7" dur="3s" repeatCount="indefinite"/></circle>'
        b+=f'<text x="{x}" y="115" text-anchor="middle" font-size="30">{e}</text><text x="{x}" y="180" text-anchor="middle" {FONT} font-size="16" font-weight="700" fill="{c}">{n}</text>'
    wr('pipeline.svg',W,H,b)
header();bars('stats.svg','GitHub Stats',STATS,BADGE);bars('languages.svg','Top Languages',LANGS,'Tech Mix');trophies();activity();pipeline();print('ok')
