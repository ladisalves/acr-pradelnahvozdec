# Link check — 2026-11-05

`python3 scripts/check_links.py --external`

- Seven HTML pages; 189 local references checked; no missing files or anchors.
- Sixteen unique external URLs checked after fixes: fifteen returned HTTP 200
  (including redirects); Miele returned HTTP 403 and remains unverified.
- Acron redirects to a wholesale login page; its existing link is retained.
- Removed the missing `images/back.gif` background reference; the solid fallback remains.
- Updated links to the confirmed destinations for Baghirra, Girbau, Bezema/CHT,
  Holiday Inn, Mandarin Oriental, and the laundry's Facebook page.
- Three Girbau product URLs returned 404. Those links now go to the manufacturer
  homepage because replacement pages for the old models were not established.
- The Klaro PDF URL redirected to its homepage. The link now explicitly uses
  that homepage.
- The Hudy Havlíčkova domain did not resolve. Removed the dead article links
  and their “read more” sentence; retained the service description.
- Replaced the unavailable Facebook share script and legacy sharing widgets
  with a plain Facebook share link.
- Map and carbon calculator iframe URLs now use HTTPS.

An HTTP 200 response confirms reachability, not the accuracy of third-party
content or that an iframe allows embedding. The legacy Skype script is reachable;
its calling service was not functionally tested. No browser was available for
visual verification. Apache redirects require mod_rewrite and AllowOverride;
they must be verified on the target host.
