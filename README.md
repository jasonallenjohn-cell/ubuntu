# Common Ground Initiative — standalone site

A self-contained static website for Ubuntu Land Trust & Developments and the
28 Athabaska Avenue project. No build step, no dependencies (Google Fonts only).

```
ubuntu-site/
├── index.html         # homepage (the site)
├── vercel.json        # static deploy config
└── docs/              # linked documents + the model
    ├── UBUNTU-ATHABASKA-HOW-IT-WORKS.html
    ├── UBUNTU-ATHABASKA-LANDOWNER-ONEPAGER.html
    ├── UBUNTU-ATHABASKA-LENDER-ONEPAGER.html
    ├── UBUNTU-ATHABASKA-LANDOWNER-PACKAGE.html
    ├── UBUNTU-ATHABASKA-PROFORMA.html
    └── UBUNTU-ATHABASKA-PROFORMA-MODEL.xlsx
```

## Preview locally
```bash
cd ubuntu-site && python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy it as its own site (own domain, e.g. ubuntultd.ca)

**Vercel** (recommended)
```bash
cd ubuntu-site
npx vercel            # first run: create a NEW project (not the k0re one)
npx vercel --prod     # promote to production, then add your domain in the dashboard
```

**Netlify** — drag the `ubuntu-site/` folder onto https://app.netlify.com/drop, or:
```bash
cd ubuntu-site && npx netlify-cli deploy --prod --dir .
```

**GitHub Pages** — push `ubuntu-site/` to a repo and enable Pages on that folder.

All three serve the folder as-is. Point your domain at the new project in the host's dashboard.
