"""Render the English Markdown collection into the blog's tracked static pages."""
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from html import escape
import re
import math
import argparse

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
TITLE = 'Computational Lithography Notes'
DESCRIPTION = 'A personal notebook on machine learning, computational lithography, and inverse lithography.'
parser = argparse.ArgumentParser(description='Build the English notebook for GitHub Pages or a local preview.')
parser.add_argument('--base-path', default='', help='Repository path, such as /repository-name. Leave empty for a user site.')
args = parser.parse_args()
BASE_PATH = '/' + args.base_path.strip('/') if args.base_path.strip('/') else ''
if BASE_PATH and not re.fullmatch(r'/[A-Za-z0-9._-]+', BASE_PATH):
    parser.error('--base-path must be a single repository path')

def site_url(path):
    return BASE_PATH + '/' + path.lstrip('/')
ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#060c17"/><ellipse cx="16" cy="16" rx="7" ry="12" transform="rotate(28 16 16)" fill="none" stroke="#94d9f3" stroke-width="2.5"/><path d="M7 24l18-16" stroke="#94d9f3" stroke-width="1.2"/></svg>'
MARK = '<svg class="brand-mark" viewBox="0 0 32 40" fill="none" aria-hidden="true"><ellipse cx="16" cy="20" rx="8" ry="17" transform="rotate(28 16 20)" stroke="currentColor" stroke-width="1.6"/><path d="M5 32L27 8" stroke="currentColor" stroke-width=".8"/></svg>'

def inline(text):
    text = escape(text, quote=False)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: '<a href="' + escape(__import__('html').unescape(m[2]), quote=True) + '">' + m[1] + '</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

def read_post(path):
    _, meta, content = path.read_text(encoding='utf-8').split('---', 2)
    field = lambda key: re.search(r'^'+key+r': "(.*)"$', meta, re.M)[1]
    body = content.split('\n---\n')[0]
    paragraphs = [p for p in body.split('\n\n') if p.strip() and not p.lstrip().startswith(('#','![','*Figure'))]
    word_count = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", '\n'.join(paragraphs)))
    return {'title':field('title'),'description':field('description'),'date':field('pubDate'),'slug':path.stem,'content':content,'words':word_count,'minutes':math.ceil(word_count/200),'url':site_url('notes/'+path.stem+'/')}

def head(title, description):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(ICON,safe='')}"><link rel="stylesheet" href="{site_url('styles.css')}"><script src="{site_url('site.js')}" defer></script></head><body><a class="skip-link" href="#main">Skip to content</a>'''

def header(home=False):
    return f'''<header class="site-header"><div class="shell nav-wrap"><a class="brand" href="{site_url('')}" aria-label="{escape(TITLE, quote=True)} home">{MARK}<span>{escape(TITLE)}</span></a><nav class="nav-links" aria-label="Main navigation"><a href="{site_url('')}#notes"{' aria-current="page"' if home else ''}>Notes</a><a href="{site_url('')}#about">About</a></nav></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="shell footer-inner"><div class="footer-left"><span>© 2026 {escape(TITLE)}</span></div><button class="signal-button" type="button" data-signal aria-label="Activate signal 117" aria-pressed="false">117</button></div></footer><div class="signal-message" data-signal-message role="status" aria-live="polite" aria-atomic="true"></div></body></html>'''

def render_article(post):
    blocks = [block.strip() for block in post['content'].strip().split('\n\n') if block.strip()]
    result=[]; i=0; sources=False
    while i<len(blocks):
        block=blocks[i]
        if block.startswith('# '): i+=1;continue
        if block=='---':
            result.append('<footer class="sources" aria-label="Sources and image credits">');sources=True
        elif block.startswith('!['):
            image=re.fullmatch(r'!\[([^\]]*)\]\(([^)]*)\)',block)
            caption=blocks[i+1]
            if not caption.startswith('*Figure'): raise ValueError('Figure caption missing')
            asset='/'+image[2].lstrip('/')
            if not (DIST/asset.lstrip('/')).is_file(): raise FileNotFoundError(asset)
            result.append(f'<figure><div class="figure-frame"><img src="{site_url(asset)}" alt="{escape(image[1],quote=True)}" loading="lazy" decoding="async"></div><figcaption>{inline(caption[1:-1])}</figcaption></figure>');i+=1
        else: result.append('<p>'+inline(block)+'</p>')
        i+=1
    if sources:result.append('</footer>')
    return ''.join(result)

posts=sorted((read_post(p) for p in (ROOT/'content').glob('*.md')),key=lambda p:p['date'],reverse=True)
if not posts:raise ValueError('No blog posts')
entries=[]
for number,post in enumerate(posts,1):
    date=datetime.strptime(post['date'],'%Y-%m-%d').strftime('%d %b %Y')
    entries.append(f'''<article class="entry"><div class="entry-index">{number:02d}</div><div><div class="entry-meta"><span class="entry-category">Course notes</span><span aria-hidden="true">/</span><time datetime="{post['date']}">{date}</time><span>· {post['minutes']} min read</span></div><h3><a href="{post['url']}">{escape(post['title'])}</a></h3><p class="entry-description">{escape(post['description'])}</p><ul class="tags" aria-label="Topics"><li>Lithography</li><li>OPC</li><li>ILT</li></ul></div></article>''')
    page=head(post['title']+' — '+TITLE,post['description'])+header()
    page+=f'''<main id="main"><section class="post-top"><div class="shell"><div class="post-heading"><a class="back-link" href="{site_url('')}#notes">← All notes</a><p class="eyebrow">Course notes / Lithography · 001</p><h1>{escape(post['title'])}</h1><div class="post-meta"><time datetime="{post['date']}">{date}</time><span>{post['minutes']} min read</span><span>{post['words']:,} words</span></div></div></div></section><article class="article-body">{render_article(post)}<div class="article-end"><a class="text-link" href="{site_url('')}#notes">Back to the notebook <span aria-hidden="true">↗</span></a><span class="series-label">Semiconductor lithography<br>Course notes · 001</span></div></article></main>'''+footer()
    target=DIST/'notes'/post['slug']/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page,encoding='utf-8')

latest=posts[0]
home=head(TITLE+' — Light, patterns & learning',DESCRIPTION)+header(True)
home+=f'''<main id="main"><section class="hero" aria-labelledby="hero-title"><img class="hero-art" src="{site_url('assets/cortana-background.png')}" alt="" aria-hidden="true" fetchpriority="high"><div class="shell hero-inner"><p class="eyebrow">Research & course notes</p><h1 id="hero-title">Notes on light,<br>patterns & learning.</h1><p class="hero-copy">A personal notebook on computational lithography, inverse problems, and what I learn along the way.</p><a class="text-link" href="{latest['url']}">Read the first note <span class="arrow" aria-hidden="true">↗</span></a></div></section><div class="shell index-layout"><section id="notes" aria-labelledby="notes-title"><div class="section-heading"><h2 id="notes-title">The notebook</h2><span class="count">{len(posts):02d} entry</span></div>{''.join(entries)}</section><aside class="about" id="about" aria-labelledby="about-title"><h2 id="about-title">Behind the notes</h2><p>I'm a PhD student researching <span class="research">machine learning for computational and inverse lithography.</span></p><p class="note">This is where I collect course notes and work through the ideas behind the patterns.</p></aside></div></main>'''+footer()
(DIST/'index.html').write_text(home,encoding='utf-8')
missing=head('Signal not found — '+TITLE,'This page is not in the notebook.')+header()+f'''<main id="main" class="shell not-found"><p class="eyebrow">404 / Signal lost</p><h1>Not in this notebook.</h1><p>The page may have moved. The notebook is a good place to pick up the trail.</p><a class="text-link" href="{site_url('')}">Return to the notebook ↗</a></main>'''+footer()
(DIST/'404.html').write_text(missing,encoding='utf-8')
(DIST/'.nojekyll').touch()
print(f'Rendered home, {len(posts)} English article, and 404 page. First article: {latest["words"]} words.')
