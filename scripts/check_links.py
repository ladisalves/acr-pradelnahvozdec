#!/usr/bin/env python3
"""Check local HTML/CSS links; optionally probe external URLs with --external."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'data-href') and value:
                self.links.append(value)
            if key in ('id', 'name') and value:
                self.ids.add(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external', action='store_true')
    args = parser.parse_args()
    pages = {}
    refs = []
    for path in sorted(ROOT.glob('*.html')):
        page = Links()
        text = path.read_text(encoding='utf-8')
        page.feed(text)
        assert '<?php' not in text, path
        pages[path] = page
        refs.extend((path, link) for link in page.links)
    for path in ROOT.glob('css/*.css'):
        refs.extend((path, link) for link in re.findall(r'url\([\'"]?([^\)\'\"]+)', path.read_text()))
    # Assets loaded dynamically by the existing gallery scripts.
    for path in ROOT.glob('js/*.js'):
        refs.extend((ROOT/'index.html', link) for link in re.findall(r"['\"](images/[^'\"]+)['\"]", path.read_text()))
    refs.extend((ROOT/'index.html', 'js/'+name+'.js') for name in ('builder', 'effects'))
    errors = []
    external = set()
    checked = 0
    for source, link in refs:
        url = urlsplit(link)
        if url.scheme in ('http', 'https') or url.netloc:
            external.add(link)
            continue
        if url.scheme:
            continue
        target = (ROOT / unquote(url.path.lstrip('/')) if url.path.startswith('/') else source.parent / unquote(url.path)).resolve() if url.path else source
        checked += 1
        if not target.exists():
            errors.append(f'{source.relative_to(ROOT)}: missing {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{source.relative_to(ROOT)}: missing anchor {link}')
    print(f'Checked {len(pages)} HTML pages and {checked} local references; {len(errors)} errors.')
    for error in errors:
        print(error)
    if args.external:
        def probe(url):
            try:
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (site link audit)'})
                with urlopen(req, timeout=15) as response:
                    return f'{response.status}\t{url}\t{response.url}'
            except Exception as error:
                return f'UNVERIFIED\t{url}\t{error}'
        with ThreadPoolExecutor(max_workers=12) as pool:
            for result in pool.map(probe, sorted(external)):
                print(result)
    else:
        print(f'{len(external)} unique external URLs; use --external to probe them.')
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
