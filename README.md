# GraphTheory landing page

<p><strong>Docs:</strong> <a href="https://graphtheory.xyz/">https://graphtheory.xyz/</a></p>

Static cyberpunk landing page for GraphTheory.

## Preview

```bash
python3 -m http.server 4173
open http://127.0.0.1:4173/
```

## Files

- `index.html`: landing page with embedded CSS and no build step.
- `assets/graphtheory-profile.webp`: optimized hero image (local source file not committed).
- `assets/demos/*.gif`: 30s VHS terminal demos synced from project repos (`scripts/sync_demo_gifs.sh`).
- `assets/og-image.png`: 1200x630 share card.
- `assets/favicon.svg`, `assets/favicon.png`, `assets/apple-touch-icon.png`, `assets/site.webmanifest`: identity assets.
- `robots.txt`, `sitemap.xml`, `404.html`: deployment basics.

## Link TODOs

The page intentionally does not invent unverified repository URLs.

Verified social links:

- X: https://x.com/graphtheory
- GitHub: https://github.com/codegraphtheory

Search for `link-needed` and replace the pending anchors with verified URLs for:

- RAGhelm repository
- Gateproof.ai repository
- Proof Bundles repository, if public
- Agent Release Lab repository, if public

The GitHub namespace currently points to `https://github.com/codegraphtheory` and the Hermes Profile Template card points to `https://github.com/codegraphtheory/hermes-profile-template`.
