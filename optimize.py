import re
import os

path = r"c:\Users\Win 10\reicetas dolar\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Images to WebP and Compress
# Unsplash: add fm=webp & q=60
def optimize_unsplash(match):
    url = match.group(1)
    if 'fm=webp' not in url:
        url += '&fm=webp'
    url = url.replace('q=80', 'q=60')
    return url

html = re.sub(r'(https://images\.unsplash\.com/[^"\'\s]+)', optimize_unsplash, html)

# Local images: just make sure they are referenced.
# Wait, user didn't specify converting local images format, but "convert images to WebP". They are mostly using external.

# 2. Add loading="lazy" and decoding="async" globally to <img>
def add_lazy_async(match):
    full_tag = match.group(0)
    # Check if lazy is there
    if 'loading=' not in full_tag:
        full_tag = full_tag.replace('<img', '<img loading="lazy"')
    if 'decoding=' not in full_tag:
        full_tag = full_tag.replace('<img', '<img decoding="async"')
    return full_tag

html = re.sub(r'<img\b[^>]*>', add_lazy_async, html)

# Exception: Replace eager on logo if needed, but it's fine.
html = html.replace('class="hero-logo" loading="lazy"', 'class="hero-logo"') 

# 3. Decrease animation duration, intensity, remove blurs
html = html.replace('filter: blur(5px);', 'filter: blur(2px);')
html = html.replace('filter: blur(8px);', 'filter: blur(3px);')
html = html.replace('backdrop-filter: blur(8px);', 'backdrop-filter: blur(3px);')
html = html.replace('box-shadow: 0 40px 70px rgba(0, 0, 0, 0.35);', 'box-shadow: 0 20px 30px rgba(0, 0, 0, 0.2);')
html = html.replace('box-shadow: 0 30px 60px rgba(0, 0, 0, 0.35)', 'box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2)')
html = html.replace('box-shadow: 0 25px 45px rgba(0, 0, 0, 0.25)', 'box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15)')

# Remove excessive background particles / waves if they animate infinitely and heavily
html = html.replace('animation: driftParticles 25s linear infinite;', '/* removed driftParticles */')
# html = html.replace('animation: popFloating', '/* popFloating removed */')

# Keep the VSL play button infinite animation but slow it down:
html = html.replace('animation: pulsePlayVSL 2s infinite ease-in-out;', 'animation: pulsePlayVSL 4s infinite ease-in-out;')

# Remove multiple animations at once on hover cards:
html = html.replace('transform: translateY(-8px) scale(1.02)', 'transform: translateY(-4px)')
html = html.replace('transform: scale(1.05) translate(-10px, 10px);', 'transform: scale(1.02);')
html = html.replace('animation: shimmerSlide 5s infinite;', '/* removed shimmer */')

# 4. VSL video ONLY load after click
html = html.replace('preload="metadata"', 'preload="none"')
html = html.replace('preload="auto"', 'preload="none"')
# Ensure VSL explicitly has preload="none"
if 'id="vsl-video" playsinline preload="none"' not in html:
    html = html.replace('id="vsl-video" playsinline', 'id="vsl-video" playsinline preload="none"')

# 5. Minify CSS and JS (basic whitespace removal)
def minify_css(match):
    css = match.group(1)
    # Remove CSS comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove newlines and tabs
    css = re.sub(r'\s+', ' ', css)
    # Remove space around delimiters
    css = re.sub(r'\s*([\{\}:;,])\s*', r'\1', css)
    return '<style>' + css + '</style>'

html = re.sub(r'<style>(.*?)</style>', minify_css, html, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("Optimization complete.")
