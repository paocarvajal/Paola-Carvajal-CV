#!/usr/bin/env python3
"""Build the static website and three-page PDF from cv.json."""
import json
from pathlib import Path
from html import escape as e
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / 'cv.json').read_text())
def bullets(items):
    return '<ul class="bullets">' + ''.join('<li>'+e(x)+'</li>' for x in items) + '</ul>'
def section_heading(n,title,desc=''):
    return f'<div class="section-heading"><h2><span class="section-number">{n}</span>{title}</h2><p>{desc}</p></div>'
def project(p):
    note=f'<p class="note">{e(p["note"])}</p>' if p.get('note') else ''
    return f'<article class="project"><p class="client">{e(p["client"])}</p><h4>{e(p["title"])}</h4><p class="scope">{e(p["scope"])}</p><p class="project-date">{e(p["dates"])}</p>{note}{bullets(p["bullets"])}</article>'
projects=d['pwc']['projects']
head=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paola Carvajal | Operations Strategy &amp; Program Leadership</title>
<meta name="description" content="Paola Carvajal, MBA, MIB. Operations strategy, supply chain transformation and program leadership. 15+ years across consulting and industry.">
<meta name="theme-color" content="#4a6d6a"><meta property="og:title" content="Paola Carvajal | Operations Strategy &amp; Program Leadership"><meta property="og:description" content="Operations strategy. Supply chain transformation. Program leadership. Explore experience, career impact and credentials."><meta property="og:type" content="profile">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="wrap nav"><a class="brand" href="#main" aria-label="Paola Carvajal, home"><span class="monogram" aria-hidden="true">pc</span><span class="brand-text">PAOLA CARVAJAL</span></a><nav aria-label="Main navigation"><a href="#experience">Experience</a><a href="#expertise">Expertise</a><a href="#credentials">Credentials</a><a class="nav-contact" href="#contact">Contact</a></nav></div></header>
<main id="main"><section class="hero wrap" aria-labelledby="name"><p class="eyebrow">Operations strategy &amp; transformation</p><div class="hero-grid"><div><h1 id="name">Paola<span>Carvajal.</span></h1><p class="degrees">MBA &nbsp;/&nbsp; MIB</p><p class="headline">Operations Strategy<br>Supply Chain Transformation<br>Program Leadership</p><div class="actions"><a class="button primary" href="PCS%20CV.pdf" download="Paola_Carvajal_CV_2026.pdf">Download CV <span aria-hidden="true">↗</span></a><a class="button" href="{d['linkedin']}" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a></div></div><div class="hero-aside"><div class="experience-mark">15+ years<span>ACROSS CONSULTING &amp; INDUSTRY</span></div><p>{e(d['summary'])}</p><p>{e(d['summary_detail'])}</p></div></div><div class="contact-line"><span>{e(d['location'])}</span><a href="tel:+522224807474">{e(d['phone'])}</a><a href="mailto:{d['email']}">{d['email']}</a></div></section>
<section class="impact" aria-label="Selected career impact"><div class="wrap"><p class="eyebrow">Selected career impact</p><div class="metric-grid">'''
html=head+''.join(f'<div class="metric"><strong>{m["value"]}</strong><b>{m["label"]}</b><small>{e(m["context"])}</small></div>' for m in d['metrics'])+'</div></div></section>'
html+='<section class="section wrap" id="experience">'+section_heading('01 / EXPERIENCE','Strategy into execution.','Consulting programs, operational change and measurable business outcomes.')
html+=f'<div class="employer"><div><h3>{e(d["pwc"]["company"])}</h3><p>{e(d["pwc"]["role"])}</p></div><span class="date">{e(d["pwc"]["dates"])}</span></div><div class="feature-grid">'+''.join(project(x) for x in projects[:2])+'</div><div class="project-list">'
for p in projects[2:]:
    html+=f'<details{(" open" if p["client"]=="Duracell" else "")}><summary><span><span class="title">{e(p["client"])} · {e(p["title"])}</span><span class="sub">{e(p["scope"])} · {e(p["dates"])}</span></span></summary>{bullets(p["bullets"])}</details>'
html+='</div><aside class="recognition"><h3>Recognition &amp; people leadership</h3>'+bullets(d['recognition'])+'</aside></section>'
html+='<section class="section wrap" aria-labelledby="earlier-heading"><div class="section-heading"><h2 id="earlier-heading"><span class="section-number">02 / EARLIER LEADERSHIP</span>Built on operating experience.</h2><p>Country management, commercial growth and end-to-end supply chains.</p></div>'
for x in d['earlier']:
    html+=f'<article class="timeline"><div><h3>{e(x["company"])}</h3><span class="date">{e(x["dates"])}</span><div class="location">{e(x["location"])}</div></div><div><h4>{e(x["role"])}</h4>{bullets(x["bullets"])}</div></article>'
html+='</section><section class="section wrap" id="expertise">'+section_heading('03 / EXPERTISE','A connected view of the business.')+'<div class="expertise-grid">'
for g in d['expertise']:
    html+=f'<div><h3>{e(g["title"])}</h3><ul class="plain-list">'+''.join('<li>'+e(x)+'</li>' for x in g['items'])+'</ul></div>'
html+='</div><div class="tech"><h3>Technology &amp; transformation exposure</h3><ul class="plain-list">'+''.join('<li>'+e(x)+'</li>' for x in d['technology'])+'</ul></div></section>'
html+='<section class="section wrap" id="credentials">'+section_heading('04 / CREDENTIALS','Continuous development.')+'<div class="education-grid"><div>'
for x in d['education']:
    html+='<article class="education-item">'+('<span class="tag">In progress</span>' if x.get('status') else '')+f'<h3>{e(x["degree"])}</h3><p>'+e(' · '.join(x[k] for k in ['institution','dates'] if x.get(k)))+'</p></article>'
html+='</div><div><h3 class="subheading">Certification &amp; training</h3>'
for x in d['training']:
    html+=f'<article class="credential"><span class="tag">{e(x["type"])}</span><h4>{e(x["title"])}</h4><p>{e(x["detail"])}</p></article>'
html+='<h3 class="subheading">Languages</h3><ul class="plain-list">'+''.join('<li>'+e(x)+'</li>' for x in d['languages'])+'</ul></div></div></section></main>'
html+=f'<footer class="footer wrap" id="contact"><div class="footer-grid"><div><h2>Let’s connect.</h2><p><a href="mailto:{d["email"]}">{d["email"]}</a><br>{d["location"]} · <a href="tel:+522224807474">{d["phone"]}</a></p></div><a class="button" href="{d["linkedin"]}" target="_blank" rel="noopener noreferrer">View LinkedIn profile <span aria-hidden="true">↗</span></a></div><div class="footer-meta"><span>Paola Carvajal · MBA, MIB</span><span>Updated {d["updated"]}</span></div></footer></body></html>'
(ROOT/'index.html').write_text(html,encoding='utf-8')
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="#284642"/><text x="32" y="44" text-anchor="middle" fill="white" font-family="Georgia,serif" font-size="42">p</text></svg>')

# Searchable, single-column PDF with deliberate page boundaries.
font_dir = Path(reportlab.__file__).parent / 'fonts'
pdfmetrics.registerFont(TTFont('CVSans', str(font_dir / 'Vera.ttf')))
pdfmetrics.registerFont(TTFont('CVSans-Bold', str(font_dir / 'VeraBd.ttf')))
G=colors.HexColor('#4A6D6A'); INK=colors.HexColor('#283331'); MUTED=colors.HexColor('#58635F'); LINE=colors.HexColor('#D4DCD6')
styles={
 'name':ParagraphStyle('name',fontName='CVSans-Bold',fontSize=26,leading=29,textColor=INK,spaceAfter=6),
 'headline':ParagraphStyle('headline',fontName='CVSans-Bold',fontSize=10,leading=14,textColor=G,spaceAfter=5),
 'contact':ParagraphStyle('contact',fontName='CVSans',fontSize=8,leading=11,textColor=MUTED,spaceAfter=11),
 'section':ParagraphStyle('section',fontName='CVSans-Bold',fontSize=10,leading=13,textColor=G,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'title':ParagraphStyle('title',fontName='CVSans-Bold',fontSize=10,leading=13,textColor=INK,spaceBefore=7,spaceAfter=3,keepWithNext=True),
 'meta':ParagraphStyle('meta',fontName='CVSans',fontSize=8.2,leading=11,textColor=MUTED,spaceAfter=4,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='CVSans',fontSize=9,leading=12.3,textColor=INK,spaceAfter=5),
 'bullet':ParagraphStyle('bullet',fontName='CVSans',fontSize=9,leading=12.3,textColor=INK,leftIndent=9,firstLineIndent=-9,spaceAfter=4),
 'metric':ParagraphStyle('metric',fontName='CVSans-Bold',fontSize=18,leading=21,textColor=G),
 'small':ParagraphStyle('small',fontName='CVSans',fontSize=7.6,leading=10,textColor=MUTED),
}
def clean(t): return e(t.replace('·',' | ').replace('’',"'")).replace('\n','<br/>')
def P(t,style='body'): return Paragraph(clean(t),styles[style])
def PB(items): return [Paragraph('•  '+clean(t),styles['bullet']) for t in items]
def sec(t): return P(t.upper(),'section')
def proj(p):
    title=p['client']+' | '+p['title']
    meta=p['scope']+' | '+p['dates']
    if p.get('note'): meta+=' | '+p['note']
    return [P(title,'title'),P(meta,'meta')]+PB(p['bullets'])
def early(x):
    return [P(x['company']+' | '+x['role'],'title'),P(x['location']+' | '+x['dates'],'meta')]+PB(x['bullets'])
W,H=A4
story=[P(d['name'].upper(),'name'),P(d['headline'],'headline'),P('MBA, MIB | '+d['location']+' | '+d['phone']+' | '+d['email'],'contact')]
story += [Paragraph(f'<link href="{d["linkedin"]}" color="#4A6D6A">linkedin.com/in/paola-carvajal-senior-manager</link>',styles['contact']),P(d['summary']),P(d['summary_detail'])]
rows=[[P(x['value'],'metric') for x in d['metrics']],[P(x['label'],'small') for x in d['metrics']]]
t=Table(rows,colWidths=[(W-84)/4]*4);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#EDF1EC')),('LEFTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,0),8),('BOTTOMPADDING',(0,-1),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]))
story += [Spacer(1,5),t,sec('Professional experience'),P(d['pwc']['company']+' | '+d['pwc']['role'],'title'),P(d['pwc']['dates'],'meta')]
story+=proj(projects[0])+proj(projects[1])
story+=[PageBreak(),sec('PwC engagements | continued')]
for p in projects[2:]: story+=proj(p)
story+=[sec('Earlier leadership')]+early(d['earlier'][0])+early(d['earlier'][1])
story+=[PageBreak(),sec('Earlier leadership | continued')]
for x in d['earlier'][2:]:story+=early(x)
story+=[sec('Core expertise'),P(' | '.join(item for g in d['expertise'] for item in g['items']))]
story+=[sec('Education')]
for x in d['education']:
    story.append(P(x['degree']+(' - '+x['institution'] if x.get('institution') else '')+(' | '+x['dates'] if x.get('dates') else '')))
story+=[sec('Certification & professional training')]
for x in d['training']: story.append(P(x['title']+' | '+x['type']+' | '+x['detail']))
story+=[sec('Technology & transformation exposure'),P(' | '.join(d['technology'])),sec('Languages'),P(' | '.join(d['languages']))]
def chrome(c,doc):
    c.setStrokeColor(G);c.setLineWidth(3);c.line(42,H-31,W-42,H-31)
    if doc.page>1:
        c.setFont('CVSans-Bold',8);c.setFillColor(G);c.drawString(42,H-45,'PAOLA CARVAJAL  /  MBA, MIB')
    c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(42,34,W-42,34)
    c.setFont('CVSans',7);c.setFillColor(MUTED);c.drawString(42,23,'Paola Carvajal | Operations Strategy & Program Leadership')
    c.drawRightString(W-42,23,f'{d["updated"]}  |  {doc.page}')
pdf=SimpleDocTemplate(str(ROOT/'PCS CV.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=55,bottomMargin=44,title='Paola Carvajal | Operations Strategy & Program Leadership',author='Paola Carvajal',subject='Professional CV - September 2026')
pdf.build(story,onFirstPage=chrome,onLaterPages=chrome)
print('Built index.html and PCS CV.pdf')
