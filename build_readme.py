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

# The page styles the language <nav> and <h1> as plain monospace lines above
# the <pre>; GitHub would render <h1> as a large heading, so fold both into it.
m = re.match(
    r"(?:<nav[^>]*>(.*?)</nav>\s*)?<h1[^>]*>(.*?)</h1>\s*<pre[^>]*>\n?(.*)</pre>\s*$",
    body, re.S)
if not m:
    sys.exit("unexpected page structure: expected [<nav>] <h1> <pre>")
nav, title, pre = m.group(1), m.group(2).strip(), m.group(3)
if nav:
    title = nav.strip() + "\n\n" + title


def absolutize(match):
    url = match.group(2)
    if not re.match(r"^(?:[a-z]+:|#)", url):
        url = urljoin(BASE, url)
    return f'{match.group(1)}"{url}"'


title, pre = (re.sub(r'(\b(?:href|src)=)"([^"]*)"', absolutize, t)
              for t in (title, pre))

with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"<pre>{title}\n{pre}</pre>\n")
