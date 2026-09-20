"""Render the English Markdown collection into the blog's tracked static pages."""
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
from html import escape
import re
import math
import argparse
import hashlib
import json

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

def asset_url(path):
    version = hashlib.sha256((DIST / path).read_bytes()).hexdigest()[:12]
    return site_url(path) + '?v=' + version
ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#060c17"/><ellipse cx="16" cy="16" rx="7" ry="12" transform="rotate(28 16 16)" fill="none" stroke="#94d9f3" stroke-width="2.5"/><path d="M7 24l18-16" stroke="#94d9f3" stroke-width="1.2"/></svg>'

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
    tags_field = re.search(r'^tags:\s*(.+)$', meta, re.M)
    tags = json.loads(tags_field[1]) if tags_field else []
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        raise ValueError(f'{path.name}: tags must be a JSON array of strings')
    return {'title':field('title'),'description':field('description'),'date':field('pubDate'),'tags':tags,'slug':path.stem,'content':content,'words':word_count,'minutes':math.ceil(word_count/200),'url':site_url('notes/'+path.stem+'/')}

def head(title, description):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(ICON,safe='')}"><link rel="stylesheet" href="{asset_url('styles.css')}"><script src="{asset_url('site.js')}" defer></script><script type="module" src="{asset_url('likes.mjs')}"></script></head><body><a class="skip-link" href="#main">Skip to content</a>'''

def header(home=False):
    return f'''<header class="site-header"><div class="shell nav-wrap"><a class="brand" href="{site_url('')}" aria-label="{escape(TITLE, quote=True)} home"><span>{escape(TITLE)}</span></a><span class="header-art" aria-hidden="true"><img src="{site_url('assets/cortana-ring-background.png')}" width="1920" height="1200" alt=""></span></div></header>'''

def likes(post):
    key = 'cln_likes_' + hashlib.sha256(('ltmz1248.github.io:' + post['slug']).encode()).hexdigest()[:32]
    return f'''<div class="article-likes" data-like-key="{key}" data-like-title="{escape(post['title'], quote=True)}"><div class="like-controls"><button class="like-button" type="button" data-like-button title="Like this note" aria-label="Like {escape(post['title'], quote=True)}" aria-pressed="false" disabled><svg class="energy-sword" viewBox="0 0 40 40" fill="none" stroke-width="1.25" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><g transform="rotate(32 20 20)"><g class="sword-blades"><path d="M16 3C10 8 7.5 14 9.5 20L16.5 28 19 25.5 14 17.5C11.7 13.4 12.6 8.8 16 3Z"/><path d="M24 3C30 8 32.5 14 30.5 20L23.5 28 21 25.5 26 17.5C28.3 13.4 27.4 8.8 24 3Z"/></g><g class="sword-core" stroke-width=".75"><path d="M14.6 6.7C11 12 10.8 15.4 12.4 18.8L16.9 25.1"/><path d="M25.4 6.7C29 12 29.2 15.4 27.6 18.8L23.1 25.1"/></g><path class="sword-hilt" d="m17.5 27.5-1 2.5 1.5 3h4l1.5-3-1-2.5Zm.5 2.5h4"/></g></svg><span data-like-label>Like</span></button><span class="like-total" aria-live="polite" aria-atomic="true"><span data-like-count>—</span> <span data-like-unit>likes</span></span></div><p class="like-status" data-like-status role="status"></p><noscript><p class="like-status">Enable JavaScript to see likes and like this note.</p></noscript></div>'''

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
    tags_html = '<ul class="tags" aria-label="Topics">' + ''.join('<li>' + escape(tag) + '</li>' for tag in post['tags']) + '</ul>' if post['tags'] else ''
    entries.append(f'''<article class="entry"><div class="entry-index">{number:02d}</div><div><div class="entry-meta"><span class="entry-category">Course notes</span><span aria-hidden="true">/</span><time datetime="{post['date']}">{date}</time></div><h3><a href="{post['url']}">{escape(post['title'])}</a></h3><p class="entry-description">{escape(post['description'])}</p><div class="entry-actions">{tags_html}{likes(post)}</div></div></article>''')
    page=head(post['title']+' — '+TITLE,post['description'])+header()
    page+=f'''<main id="main"><section class="post-top"><div class="shell"><div class="post-heading"><a class="back-link" href="{site_url('')}#notes">← All notes</a><p class="eyebrow">Course notes / Lithography · 001</p><h1>{escape(post['title'])}</h1><div class="post-meta"><time datetime="{post['date']}">{date}</time></div></div></div></section><article class="article-body">{render_article(post)}<div class="post-likes">{likes(post)}</div><div class="article-end"><a class="text-link" href="{site_url('')}#notes">Back to the notebook <span aria-hidden="true">↗</span></a><span class="series-label">Semiconductor lithography<br>Course notes · 001</span></div></article></main>'''+footer()
    target=DIST/'notes'/post['slug']/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(page,encoding='utf-8')

latest=posts[0]
home=head(TITLE,DESCRIPTION)+header(True)
home+=f'''<main id="main"><div class="shell index-layout"><section id="notes" aria-labelledby="notes-title"><div class="section-heading"><h1 id="notes-title">Course notes</h1><span class="count">{len(posts):02d} entry</span></div>{''.join(entries)}</section><aside class="about" id="about" aria-labelledby="about-title"><h2 id="about-title">Behind the notes</h2><p>I'm a PhD student researching <span class="research">machine learning for computational and inverse lithography.</span></p><p class="note">This is where I collect course notes and work through the ideas behind the patterns.</p></aside></div></main>'''+footer()
(DIST/'index.html').write_text(home,encoding='utf-8')
missing=head('Signal not found — '+TITLE,'This page is not in the notebook.')+header()+f'''<main id="main" class="shell not-found"><p class="eyebrow">404 / Signal lost</p><h1>Not in this notebook.</h1><p>The page may have moved. The notebook is a good place to pick up the trail.</p><a class="text-link" href="{site_url('')}">Return to the notebook ↗</a></main>'''+footer()
(DIST/'404.html').write_text(missing,encoding='utf-8')
(DIST/'.nojekyll').touch()
print(f'Rendered home, {len(posts)} English article, and 404 page. First article: {latest["words"]} words.')
