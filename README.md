# Prádelna Hvozdec static website

The seven pages are plain HTML with UTF-8 text. No PHP, build step, database,
or package installation is required. CSS, images, downloads, and the existing
JavaScript gallery are kept in their original directories.

## Preview

Run `python3 -m http.server 8000` from this directory and open
`http://localhost:8000/`.

## Check links

Run `python3 scripts/check_links.py` to check local page links, anchors, CSS
assets, and gallery assets. Add `--external` to probe external URLs. External
failures can also mean a site blocks automated requests; inspect them manually
before removing content.

## Hosting

Upload the HTML pages plus `css/`, `js/`, `images/`, and `files/` to any static
web host. Apache can use the included `.htaccess` to redirect old `.php` URLs
to `.html` with HTTP 301. Other hosts need equivalent redirect rules for
`index`, `services`, `order`, `partners`, `footprint`, `contact`, and `bazar`.

The footer is embedded in each HTML page; edit each copy when changing it.
The order page remains the original placeholder and does not submit orders.
