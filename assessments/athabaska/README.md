# Athabaska assessment — protected sister site

Password-protected landowner assessment for 18–28 Athabaska Ave, under the
Ubuntu Land Trust Common Ground Initiative. Self-contained static site
(Google Fonts only). Intended subdomain: **athabaska.ubuntultd.com**.

## Contents
- `index.html` — landing (model, flow, project, numbers, land draw, documents)
- `docs/` — one-pagers, holistic, landowner package, development pro forma,
  the BCH assessment, and the XLSX model

## Deploy (Vercel) + lock it
1. Deploy this folder to Vercel (drag-drop on vercel.com/new, or connect a repo).
2. Project → Settings → **Domains** → add `athabaska.ubuntultd.com`
   (then add the CNAME Vercel shows you in GoDaddy: host `athabaska` → `cname.vercel-dns.com`).
3. Project → Settings → **Deployment Protection** → turn on **Password Protection**
   (Vercel Pro) and set the shared password to hand the landowner.
   (Free alternative: put it behind Cloudflare Access with email one-time-PIN.)

No build step; Vercel serves the files as-is.
