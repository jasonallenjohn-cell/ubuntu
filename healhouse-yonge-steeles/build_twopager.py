"""Heal House at Yonge & Steeles — two-page summary. Every figure imports from site_model."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_model as m
s=m.site(); a,b,c,h=s["A"],s["B"],s["C"],s["hh"]; A=m.A
LOGO='/root/.claude/skills/synced/f8734239-31ba-4ced-bc8b-cbf00346c7d5_28a6848d-eac9-43f7-925d-965e3f535b85/heal-house-brand/assets/'
svg=lambda k: open(LOGO+f'healhouse-logo-{k}.svg').read().replace('<svg ',"<svg role='img' aria-label='Heal House' ",1)
css=open('page.css').read()
M=lambda x:(f"(${-x/1e6:,.1f}M)" if x<0 else f"${x/1e6:,.1f}M"); N=lambda x:f"{x:,.0f}"; P=lambda x:f"{x*100:.0f}%"
total=s['tdc_rent']+s['sunray']+c['cost']+c['land']
lean=m.tower_b(opex_ratio=0.65,occ=0.90)
def hdr(pg): return f"<header class='mh'><div style='width:140px'>{svg('gold')}</div><span class='stamp'>Draft for discussion · HH-MODEL-0006 · {pg}</span></header>"
def foot(tag,src): return f"<footer><div style='width:100px;flex:none'>{svg('cream')}</div><div><div class='tag'>{tag}</div><div class='src'>{src}</div></div></footer>"
rows=lambda items: "".join(f"<tr><td>{l}</td><td class='n'>{v}</td></tr>" for l,v in items)
html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Heal House Yonge Steeles</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Belleza&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Montserrat:wght@400;500;600;700&display=swap">
<style>{css}
td{{padding:3px 8px}} .kpis div{{padding:6px 9px}} .kpis b{{font-size:18px}} .sub{{margin-bottom:8px}} footer{{padding:9px .5in}} header.mh{{padding:.2in .5in .08in}}
h1{{font-size:28px}} .img{{width:100%;border-radius:10px;border:1px solid var(--line);display:block;object-fit:cover}}
.cap{{font-size:7.5px;color:var(--ink-faint);margin:3px 0 8px}}
.dark{{background:var(--ink);color:var(--cream);border-radius:12px;padding:10px 13px;margin-bottom:10px}}
.dark .eyebrow{{color:var(--sage-pale)}} .dark b{{font-family:var(--display);font-weight:400;font-size:26px;display:block;line-height:1.1}}
.dark small{{font-size:8.5px;color:var(--cream-2)}}
</style></head><body><div class="page">
{hdr('Nov 2026')}
<div class="in">
<span class="eyebrow" style="margin-top:10px">Heal House at Yonge &amp; Steeles · Markham · Investment summary</span>
<h1>Three towers, one <em>healing</em> community</h1>
<p class="sub">An approved site one block from Yonge, bought from the court-appointed receiver at about $31M: affordable and market rental, a Heal House retirement residence with wellness stays, a 40,000 sq ft Heal House open to the community, and a boutique condo tower as upside.</p>
<div class="kpis">
<div><b>{N(s['homes'])} homes</b><span>{N(s['aff'])} affordable · +{b['keys']} suites</span></div>
<div><b>{M(total)}</b><span>Total program</span></div>
<div><b>{M(s['hh_e'])}</b><span>Heal House EBITDA / yr</span></div>
<div><b>{M(s['bch'])}</b><span>BCH · all repaid Yr 10</span></div>
<div><b>{M(s['bof'])}</b><span>Building Ontario Fund</span></div>
</div>
<div class="grid"><div>
<img class="img" src="approved_rendering.png" alt="Approved towers" style="height:250px;object-position:center 30%">
<p class="cap">Approved two-tower scheme · OLT final order May 7, 2024 · 44 + 40 storeys · 1,060 units · 74,467 m² · 510 parking. Rendering from the vendor’s 2026 marketing.</p>
<span class="eyebrow">01 · The program</span>
<div class="scroll"><table><thead><tr><th>Tower</th><th class="n">Homes</th><th class="n">Cost</th><th class="n">NOI / profit</th></tr></thead><tbody>
<tr><td><b>A</b> · 44 st · affordable + market rental</td><td class="n">{N(a['units'])} ({N(a['aff'])} aff.)</td><td class="n">{M(a['tdc'])}</td><td class="n">{M(a['noi'])}</td></tr>
<tr><td><b>B</b> · 40 st · Heal House retirement residence</td><td class="n">{N(b['units'])} ({N(b['aff'])} aff.)</td><td class="n">{M(b['tdc'])}</td><td class="n">{M(b['noi'])}</td></tr>
<tr><td><b>B</b> · wellness-stay suites (Sunray)</td><td class="n">{b['keys']} keys</td><td class="n">{M(b['s_cost'])}</td><td class="n">{M(b['s_noi'])}</td></tr>
<tr><td><b>C</b> · 23 st · boutique condo, to be rezoned</td><td class="n">{N(c['units'])}</td><td class="n">{M(c['cost']+c['land'])}</td><td class="n">{M(c['profit'])} profit</td></tr>
</tbody><tfoot><tr><td>Total</td><td class="n">{N(s['homes'])}</td><td class="n">{M(total)}</td><td class="n"></td></tr></tfoot></table></div>
</div><div>
<div class="callout"><span class="eyebrow">02 · What we need to raise</span>
<div class="raise">
<div><b>{M(s['bof'])}</b><small>Building Ontario Fund — Tower B, 4% a year, repaid Year 20</small></div>
<div><b>{M(s['bch'])}</b><small>BCH — 10-year loan, repaid in full at Year 10</small></div>
<div><b>{M(s['mli'])}</b><small>CMHC MLI Select, Towers A + B</small></div>
<div><b>{M(s['city'])}</b><small>City of Markham — incentives / DC relief</small></div>
<div><b>{M(s['sponsor'])}</b><small>Sponsor equity — {M(s['acq_eq'])} at purchase</small></div>
<div><b>{M(s['guar'])}</b><small>Land guarantee — LiUNA via Nesting Ground</small></div>
<div><b>{M(s['sunray'])}</b><small>Sunray — wellness-stay suites</small></div>
<div><b>{M(s['condo_eq'])}</b><small>Tower C equity — later phase</small></div>
</div></div>
<div class="dark"><span class="eyebrow">03 · BCH gets every dollar back</span>
<b>{M(s['bch'])} repaid at Year 10</b>
<small>From a Year-10 CMHC refinance at {A['refi_dscr']:.2f}x: {M(a['surplus'])} left on Tower A and {M(b['surplus'])} on Tower B after BCH. Still repaid at 4.5% interest.</small></div>
<span class="eyebrow">04 · What it returns</span>
<div class="scroll"><table><tbody>{rows([
 ("Tower A — sponsor multiple · equity at Yr 10", f"{a['mult']:.1f}x · {M(a['equity10'])}"),
 ("Tower B — sponsor multiple · equity at Yr 10", f"{b['mult']:.1f}x · {M(b['equity10'])}"),
 ("Tower C — condo profit at $1,050/sf", f"{M(c['profit'])} · {P(c['margin'])}"),
 ("Heal House — EBITDA at maturity · value 8–12x", f"{M(h['ebitda'])} · {M(8*h['ebitda'])}–{M(12*h['ebitda'])}"),
])}</tbody></table></div>
</div></div></div>
{foot('A sanctuary for healing.', 'Sources: '+m.SRC['gfa']+' · '+m.SRC['cost']+' · '+m.SRC['rents']+' · '+m.SRC['dc']+' · '+m.SRC['stack']+'. Illustrative scenario for discussion — not a valuation, offer, commitment or financial advice. Subject to receiver and court approval, CMHC, BCH, Building Ontario Fund and City of Markham approvals, and LiUNA trustee approval.')}
<div class="pb"></div>
{hdr('page 2')}
<div class="in">
<span class="eyebrow" style="margin-top:10px">How it is funded, and what Heal House earns</span>
<h1>Capital that comes <em>back</em></h1>
<p class="sub">CMHC carries half of each rental tower, BCH is a 10-year loan repaid at the Year-10 refinance, and the Building Ontario Fund is the patient capital on Tower B through Year 20.</p>
<div class="grid"><div>
<span class="eyebrow">01 · Capital stack</span>
<div class="scroll"><table><thead><tr><th>Source</th><th class="n">Tower A</th><th class="n">Tower B</th></tr></thead><tbody>
<tr><td>CMHC MLI Select · 4.25%, 50-yr</td><td class="n">{M(a['mli'])}</td><td class="n">{M(b['mli'])}</td></tr>
<tr><td>BCH · repaid Year 10</td><td class="n">{M(a['bch'])}</td><td class="n">{M(b['bch'])}</td></tr>
<tr><td>Building Ontario Fund · to Year 20</td><td class="n">—</td><td class="n">{M(b['bof'])}</td></tr>
<tr><td>City of Markham</td><td class="n">{M(a['city'])}</td><td class="n">{M(b['city'])}</td></tr>
<tr><td>Sponsor equity · land + pre-development</td><td class="n">{M(a['sponsor'])}</td><td class="n">{M(b['sponsor'])}</td></tr>
</tbody><tfoot><tr><td>Total cost · debt coverage Yr 1</td><td class="n">{M(a['tdc'])} · {a['dscr']:.2f}x</td><td class="n">{M(b['tdc'])} · {b['dscr']:.2f}x</td></tr></tfoot></table></div>
<span class="eyebrow">02 · Year 10 — BCH repaid in full</span>
<div class="scroll"><table><thead><tr><th>Refinance</th><th class="n">Tower A</th><th class="n">Tower B</th></tr></thead><tbody>
<tr><td>Value at Year 10</td><td class="n">{M(a['val10'])}</td><td class="n">{M(b['val10'])}</td></tr>
<tr><td>New CMHC loan at {A['refi_dscr']:.2f}x</td><td class="n">{M(a['refi'])}</td><td class="n">{M(b['refi'])}</td></tr>
<tr><td>Repays first mortgage</td><td class="n">({M(a['mli10'])})</td><td class="n">({M(b['mli10'])})</td></tr>
<tr><td>Repays BCH in full</td><td class="n">({M(a['bch10'])})</td><td class="n">({M(b['bch10'])})</td></tr>
</tbody><tfoot><tr><td>Left over</td><td class="n">{M(a['surplus'])}</td><td class="n">{M(b['surplus'])}</td></tr></tfoot></table></div>
<span class="eyebrow">03 · Year 20 — the Fund repaid</span>
<p>The Fund is paid 4% a year (~{M(b['bof_pay'])}) from Year-11 cash flow of {M(b['cf11'])}. A Year-20 refinance frees {M(b['free20'])} against {M(b['bof'])} owed, leaving {M(b['bof_cover20'])}.</p>
</div><div>
<span class="eyebrow">04 · Tower B and Heal House</span>
<div class="scroll"><table><tbody>
<tr><td>Retirement suites, two services · {N(b['aff'])} affordable 40 yrs</td><td class="n">{N(b['units'])}</td></tr>
<tr><td>Revenue (rent + services) · NOI after 62% expenses</td><td class="n">{M(b['egi'])} · {M(b['noi'])}</td></tr>
<tr><td>Leaner case (65% expenses, 90% occupancy)</td><td class="n">{M(lean['noi'])} · {lean['dscr']:.2f}x</td></tr>
{''.join(f"<tr><td>Heal House · {k}</td><td class='n'>{M(v)}</td></tr>" for k,v in h['lines'].items())}
<tr><td>Heal House · management fee (5% of Tower B revenue)</td><td class="n">{M(h['fee'])}</td></tr>
</tbody><tfoot><tr><td>Heal House EBITDA · rent-free podium</td><td class="n">{M(h['ebitda'])}</td></tr></tfoot></table></div>
<img class="img" src="siteplan.jpg" alt="Approved site plan" style="height:150px;object-fit:contain;background:#fff">
<p class="cap">Approved site plan: Tower A west, Tower B east, six-storey podium, strata park and POPS. An office entry off the drop-off court suits the Heal House front door.</p>
<span class="eyebrow">05 · Stated openly</span>
<ul class="c">
<li>Zoning is residential only; the clinic podium needs an amendment. Hold removal, minor variance and consent come before site plan.</li>
<li>Rents of $6,000 / $7,800 need a Markham market study; development charges are estimates.</li>
<li>The Fund at ${b['bof']/b['units']/1e3:,.0f}K/home is above the program’s $75.5K; Tower C is not approved.</li>
<li>The existing conditional buyer’s financing condition lapsed Oct 9; confirm its status with the receiver.</li>
</ul>
</div></div></div>
{foot('Expert care, tailored to you — in a tranquil, nurturing space where healing can flourish.', 'Sources: '+m.SRC['ret']+' · '+m.SRC['hh']+' · '+m.SRC['bof']+' · '+m.SRC['suites']+' · '+m.SRC['condo']+'. Illustrative scenario for discussion.')}
</div></body></html>"""
open('HealHouse_YongeSteeles_TwoPager.html','w').write(html); print('ok')
