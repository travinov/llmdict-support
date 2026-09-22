#!/usr/bin/env python3
"""Build the four static, accessible pages. No runtime dependencies or tracking."""
from pathlib import Path
import html
import json
from urllib.parse import urlencode, quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
site = json.loads((ROOT / 'content/site.json').read_text())
if not site.get('owner'):
    raise SystemExit('Set the verified developer name in content/site.json before building.')
esc = html.escape

def render(lang, kind, data):
    path = ('' if lang == 'ru' else 'en/') + ('' if kind == 'support' else 'privacy/')
    prefix = '../' * len(Path(path).parts) if path else './'
    route = lambda page, language=lang: prefix + ('' if language == 'ru' else 'en/') + ('' if page == 'support' else 'privacy/')
    if not route('support').endswith('/'): raise ValueError('Expected directory URL')
    title = data['title' if kind == 'support' else 'privacy_title']
    description = data['description' if kind == 'support' else 'privacy_description']
    nav = ''.join(f'<a href="{route(p)}"'+(' aria-current="page"' if p == kind else '')+f'>{data[p+"_label"]}</a>' for p in ['support','privacy'])
    languages = ''.join(f'<a href="{route(kind,l)}" lang="{l}" hreflang="{l}" aria-label="{name}"'+(' aria-current="true"' if l==lang else '')+f'>{label}</a>' for l,name,label in [('ru','Русский','RU'),('en','English','EN')])
    mail = 'mailto:' + site['email'] + '?' + urlencode({'subject':data['email_subject'],'body':data['email_body']}, quote_via=quote)
    email_label = esc(site['email']).replace('@', '<wbr>@')
    if kind == 'support':
        questions = ''.join(f'<details><summary>{esc(q[0])}</summary><div class="answer">{q[1]}</div></details>' for q in data['faq'])
        body = f'''<div class="intro"><div><p class="eyebrow">{data['eyebrow']}</p><h1>{title}</h1><p class="lead">{data['intro']}</p></div>
<aside class="contact" aria-labelledby="contact-title"><h2 id="contact-title">{data['contact_title']}</h2><p>{data['contact_intro']}</p>
<div class="email-line"><a class="email" href="{esc(mail,quote=True)}">{email_label}</a><button class="copy" type="button" data-copy-email="{site['email']}" data-success="{data['copied']}" data-fallback="{data['copy_fallback']}" aria-label="{data['copy_label']}" aria-describedby="copy-status"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M15 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h3"/></svg></button></div>
<a class="primary" href="{esc(mail,quote=True)}">{data['email_button']} <span aria-hidden="true">↗</span></a><span id="copy-status" class="copy-status" role="status" aria-live="polite"></span><p class="small">{data['contact_note']}</p></aside></div>
<section class="faq" aria-labelledby="faq-title"><p class="section-label">{data['faq_label']}</p><h2 id="faq-title">{data['faq_title']}</h2>{questions}</section>
<p class="note">{data['privacy_note']} <a href="{route('privacy')}">{data['privacy_link']}</a></p>'''
    else:
        sections=data.get('privacy_sections',[])
        toc=''.join(f'<a href="#{s[0]}">{s[1]}</a>' for s in sections)
        article=''.join(f'<section aria-labelledby="{s[0]}"><h2 id="{s[0]}">{s[1]}</h2>{s[2]}</section>' for s in sections)
        owner = esc(site['owner'])
        body=f'''<div class="legal-head"><p class="updated">{data['updated_label']}</p><h1>{title}</h1><p class="lead">{data['privacy_intro']}</p><p class="owner">{data['owner_label']}: {owner}. <a href="mailto:{site['email']}">{site['email']}</a></p></div><div class="legal-layout"><nav class="contents" aria-label="{data['contents_label']}"><p>{data['contents_label']}</p>{toc}</nav><article class="legal">{article}</article></div>'''
    html_text=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#112b49"><title>{esc(title)} · LLM Dict</title><meta name="description" content="{esc(description,quote=True)}"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="canonical" href="{site['url']+path}"><link rel="alternate" hreflang="ru" href="{site['url']+('' if kind=='support' else 'privacy/')}"><link rel="alternate" hreflang="en" href="{site['url']+'en/'+('' if kind=='support' else 'privacy/')}"><link rel="icon" type="image/png" href="{prefix}assets/app-icon.png"><link rel="apple-touch-icon" href="{prefix}assets/app-icon.png"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script></head>
<body><a class="skip" href="#main">{data['skip']}</a><div class="wrap"><header class="header"><a class="brand" href="{route('support')}"><img src="{prefix}assets/app-icon.png" alt="" width="42" height="42">LLM Dict</a><nav class="nav" aria-label="{data['nav_label']}">{nav}<div class="languages" aria-label="{data['language_label']}">{languages}</div></nav></header>
<main id="main">{body}</main><footer class="footer"><p>LLM Dict · {data['footer']}</p><div class="footer-links"><a href="{route('privacy')}">{data['privacy_label']}</a><a href="mailto:{site['email']}">{site['email']}</a></div></footer></div></body></html>
'''
    dest=OUT/path/'index.html'; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(html_text)

for lang in ['ru','en']:
    data=json.loads((ROOT/f'content/{lang}.json').read_text())
    for kind in ['support','privacy']: render(lang,kind,data)
(OUT/'.nojekyll').touch()
print('Built RU/EN support and privacy pages.')
