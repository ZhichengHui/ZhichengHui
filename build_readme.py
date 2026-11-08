"""Generate README.md for the GitHub profile from https://zhichenghui.github.io/."""
import re
import sys
import urllib.request
from urllib.parse import urljoin

BASE = "https://zhichenghui.github.io/"

html = urllib.request.urlopen(BASE, timeout=30).read().decode("utf-8")
body = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
if not body:
    sys.exit("no <body> found")
body = body.group(1).strip()

# The page styles <h1> as a plain monospace line directly above the <pre>;
# GitHub would render it as a large heading, so fold it into the <pre>.
m = re.match(r"<h1[^>]*>(.*?)</h1>\s*<pre[^>]*>\n?(.*)</pre>\s*$", body, re.S)
if not m:
    sys.exit("unexpected page structure: expected <h1> followed by <pre>")
title, pre = m.group(1).strip(), m.group(2)


def absolutize(match):
    url = match.group(2)
    if not re.match(r"^(?:[a-z]+:|#)", url):
        url = urljoin(BASE, url)
    return f'{match.group(1)}"{url}"'


pre = re.sub(r'(\b(?:href|src)=)"([^"]*)"', absolutize, pre)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"<pre>{title}\n{pre}</pre>\n")
