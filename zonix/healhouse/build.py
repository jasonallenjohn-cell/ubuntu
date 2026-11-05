import re, sys
sys.path.insert(0,'.')
from model import run, SRC, ACQ, HOTEL, PODIUM, HH, A
d=run()
B='/root/.claude/skills/synced/f8734239-31ba-4ced-bc8b-cbf00346c7d5_28a6848d-eac9-43f7-925d-965e3f535b85/heal-house-brand/assets/'
tokens=open(B+'tokens.css').read()
def svg(c): return open(B+f'healhouse-logo-{c}.svg').read().replace('<svg ',"<svg role='img' aria-label='Heal House' ",1)
M=lambda x:(f"(${-x/1e6:,.1f}M)" if x<0 else f"${x/1e6:,.1f}M"); N=lambda x:f"{x:,.0f}"; P=lambda x,k=0:f"{x*100:.{k}f}%"
ta,sn=d['ta'],d['sn']; hh=d['hh']
import model as _m, copy
_m.PODIUM['amenity']=False; d['dscr_leased']=_m.run()['dscr']; _m.PODIUM['amenity']=True
html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zonix Heal House</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Belleza&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Montserrat:wght@400;500;600;700&display=swap">
<style>{tokens}
/* one-pager scale: brand type stepped down to fit a single Letter page */
body{{font-size:10.5px;line-height:1.45}}
.page{{max-width:8.5in;margin:0 auto;background:var(--cream)}}
.in{{padding:0 .5in}}
header.mh{{display:flex;justify-content:space-between;align-items:center;padding:.26in .5in .1in;border-bottom:1px solid var(--line-soft)}}
.stamp{{font-size:8.5px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--brown);border:1px solid var(--brown);border-radius:30px;padding:5px 11px}}
h1{{font-size:30px;line-height:1.08;margin:10px 0 5px}}
h2{{font-size:16px;line-height:1.1;margin:0 0 6px}}
.sub{{font-family:var(--editorial);font-style:italic;font-size:12.5px;color:var(--ink-soft);margin:0 0 10px;max-width:none}}
.pb{{height:0}} .kpis{{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:0 0 12px;background:var(--sage-pale)}}
.kpis div{{padding:8px 10px;border-right:1px solid var(--line)}} .kpis div:last-child{{border-right:0}}
.kpis b{{display:block;font-family:var(--display);font-weight:400;font-size:19px;color:var(--ink);line-height:1.1}}
.kpis span{{font-size:7.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)}}
.grid{{display:grid;grid-template-columns:1.05fr 1fr;gap:14px}}
.eyebrow{{font-size:8px;letter-spacing:.22em;margin-bottom:3px}}
table{{font-size:9.5px}} th{{font-size:7.5px;letter-spacing:.14em;padding:5px 8px}} td{{padding:4px 8px;line-height:1.3}}
.scroll{{border-radius:10px;margin-bottom:10px}}
.callout{{padding:10px 13px;border-radius:12px;margin-bottom:10px}}
.raise{{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;margin-top:4px}}
.raise b{{font-family:var(--display);font-weight:400;font-size:20px;color:var(--ink);display:block;line-height:1.1}}
.raise small{{font-size:8.5px;color:var(--ink-soft);display:block}}
ol{{margin:2px 0 0;padding-left:15px;color:var(--ink-soft)}} ol li{{margin:0 0 3px}}
ul.c{{margin:2px 0 0;padding-left:13px;color:var(--ink-soft)}} ul.c li{{margin:0 0 2.5px}}
p{{font-size:10px;margin:0 0 6px;max-width:none}}
footer{{padding:12px .5in;display:flex;gap:16px;align-items:flex-start;margin-top:8px}}
footer .src{{font-size:7.2px;line-height:1.4;color:var(--cream)}}
footer .tag{{font-size:12px}}
@media print{{.pb{{break-after:page}} @page{{size:Letter;margin:0}} body{{background:var(--cream)}}}}
@media(max-width:700px){{.grid,.pb{{height:0}} .kpis{{grid-template-columns:1fr}} .kpis div{{border-right:0;border-bottom:1px solid var(--line)}} .in,header.mh,footer{{padding-left:16px;padding-right:16px}}}}
</style></head><body><div class="page">
<header class="mh"><div style="width:150px">{svg('gold')}</div><span class="stamp">Draft for discussion · HH-MODEL-0001 · Nov 5 2026</span></header>
<div class="in">
<span class="eyebrow" style="margin-top:12px">36–48 Steeles Ave E / 37–49 Highland Park Blvd · Markham · in receivership</span>
<h1>Health and housing, <em>together</em>, at Yonge &amp; Steeles</h1>
<p class="sub">An approved two-tower site, bought out of receivership with a pension-backed guarantee and built through the Common Ground Initiative: affordable and market rental, 55+ living with Heal House programs, a Heal House wellness podium, and short-stay suites.</p>
<div class="kpis">
<div><b>{M(d['tdc'])}</b><span>Total project cost</span></div>
<div><b>{N(d['res_units'])} homes</b><span>{N(d['aff'])} affordable · +{HOTEL['keys']} keys</span></div>
<div><b>{M(d['noi'])}</b><span>Stabilized NOI</span></div>
<div><b>{d['dscr']:.2f}x</b><span>Debt coverage, Yr 1</span></div>
<div><b>Yr 20</b><span>{'BCH mezz repaid by Yr-20 refi' if d['mezz_resid']>0 else 'BCH mezz fully repaid'}</span></div>
</div>
<div class="grid"><div>
<span class="eyebrow">01 · Program</span>
<div class="scroll"><table><thead><tr><th>Component</th><th class="n">Size</th><th class="n">NOI</th></tr></thead><tbody>
<tr><td>Tower A — affordable + market rental</td><td class="n">{N(ta['units'])} units ({N(ta['aff'])} aff.)</td><td class="n">{M(ta['noi'])}</td></tr>
<tr><td>Tower B — 55+ rental with Heal House programs</td><td class="n">{N(sn['units'])} suites ({N(sn['aff'])} aff.)</td><td class="n">{M(sn['noi'])}</td></tr>
<tr><td>Heal House podium — part of the building, no rent</td><td class="n">{N(PODIUM['sf'])} sf</td><td class="n">{M(d['p_noi'])}</td></tr>
<tr><td>Short-stay / recovery suites</td><td class="n">{HOTEL['keys']} keys</td><td class="n">{M(d['h_noi'])}</td></tr>
</tbody><tfoot><tr><td>Total · approved {N(858648)} sf GFA</td><td class="n"></td><td class="n">{M(d['noi'])}</td></tr></tfoot></table></div>
<span class="eyebrow">02 · Capital stack at construction close</span>
<div class="scroll"><table><thead><tr><th>Source</th><th class="n">Amount</th><th class="n">Share</th></tr></thead><tbody>
<tr><td>CMHC MLI Select — 4.25%, 50-yr amortization</td><td class="n">{M(d['mli'])}</td><td class="n">50%</td></tr>
<tr><td>BCH contribution — vests Yrs 1–10 vs affordable homes</td><td class="n">{M(d['grant'])}</td><td class="n">{P(d['grant']/d['tdc'],1)}</td></tr>
<tr><td>BCH mezz — no payments to Yr 10, repaid Yrs 11–20</td><td class="n">{M(d['mezz'])}</td><td class="n">{P(d['mezz']/d['tdc'],1)}</td></tr>
<tr><td>City of Markham</td><td class="n">{M(d['city'])}</td><td class="n">{P(d['city']/d['tdc'],1)}</td></tr>
<tr><td>Land equity (retained seat)</td><td class="n">{M(d['land_eq'])}</td><td class="n">{P(d['land_eq']/d['tdc'],1)}</td></tr>
</tbody><tfoot><tr><td>Total project cost</td><td class="n">{M(d['tdc'])}</td><td class="n">100%</td></tr></tfoot></table></div>
<span class="eyebrow">03 · How the land gets bought</span>
<ol>
<li><b>LiUNA pension invests in Nesting Ground</b>, building its Affordable Housing Guarantee Pool.</li>
<li><b>The guarantee lifts the land loan</b> from {M(d['unguar'])} (65% of value) to the full {M(ACQ['price'])} price — a {M(d['guar_top'])} top-up guarantee.</li>
<li><b>We buy from the receiver</b> and pay out the secured lenders (~$30.3M owing).</li>
<li><b>At construction close</b>, the Common Ground stack pays the {M(d['draw'])} Day-1 land draw against the loan; the raise retires the remaining {M(d['land_gap'])}.</li>
<li><b>Nesting Ground owns and operates</b> the rental; Heal House runs the programs; LiUNA builds.</li>
</ol>
</div><div>
<div class="callout"><span class="eyebrow">04 · What we need to raise</span>
<div class="raise">
<div><b>{M(d['eq_at_acq'])}</b><small>Equity at purchase — transfer tax {M(d['ltt'])}, legal {M(ACQ['legal'])}, 18-mo carry {M(d['carry'])}, pre-development {M(ACQ['predev'])}</small></div>
<div><b>{M(d['land_gap'])}</b><small>Equity at construction close — land loan left after the Day-1 draw</small></div>
<div><b>{M(d['peak'])}</b><small>Peak equity; {M(d['perm'])} stays in after pre-development is reimbursed</small></div>
<div><b>{M(d['guar_top'])}</b><small>Land-loan guarantee (LiUNA via Nesting Ground)</small></div>
<div><b>~{M(d['cmhc_nw'])}</b><small>Guarantor net worth for CMHC (≈25% of loan) — confirm current rule</small></div>
<div><b>~{M(d['cmhc_liq'])}</b><small>Guarantor liquidity for CMHC (≈10% of loan) — confirm current rule</small></div>
</div></div>
<span class="eyebrow">05 · What the equity earns</span>
<div class="scroll"><table><tbody>
<tr><td>60% of cash flow after debt, Yrs 1–10</td><td class="n">{M(d['lo_cf'])}</td></tr>
<tr><td>Year-10 buyout of the land seat</td><td class="n">{M(d['buyout'])}</td></tr>
</tbody><tfoot><tr><td>Back to equity · {d['mult']:.1f}x on {M(d['perm'])} · ~{P(d['irr'])} IRR</td><td class="n">{M(d['back'])}</td></tr></tfoot></table></div>
<p>Nesting Ground keeps 40% of cash flow, takes fee-simple land at Year 10, and owns the whole asset by Year 20. Year-10 refinance coverage: <b>{d['dscr10']:.2f}x</b> (needs 1.10x).</p>
<span class="eyebrow">06 · Stated openly</span>
<ul class="c">
<li><b>Assumes MLI Select and BCH fund the short-stay suites.</b> CMHC normally excludes short-stay space; if it holds that line, the suites need separate cash (e.g. Sunray). The podium is resident amenity space, which CMHC normally accepts.</li>
<li><b>55+ must stay independent rental.</b> Two bundled care services trigger Ontario's Retirement Homes Act and move CMHC to a lower-leverage product.</li>
<li><b>BCH contribution is ${d['grant_per_aff']/1e3:,.0f}K per affordable home</b> — high; phasing Tower A first lowers the first ask.</li>
<li><b>Development charges ({M(d['dc'])}) are estimates</b>; approvals, stamped drawings and final GFA are unverified. Clinic and short-stay uses need a zoning amendment.</li>
<li>Project value at stabilization ({M(d['value'])}) is below cost; the BCH contribution closes the gap.</li>
</ul>
</div></div></div>
<footer><div style="width:110px;flex:none">{svg('cream')}</div><div><div class="tag">A sanctuary for healing.</div>
<div class="src">Sources: {' · '.join(SRC[k] for k in ['gfa','constr','rents','cmhc','tax','dc','land','hotel','podium','stack'])}. Bid {M(ACQ['price'])}; guaranteed land loan at {ACQ['loan_rate']*100:.1f}%. Illustrative scenario for discussion — not an appraisal, offer, commitment or financial advice. Subject to receiver and court approval, CMHC, BCH and City of Markham approvals, LiUNA trustee approval, and legal review.</div></div></footer>

<div class="pb"></div>
<header class="mh"><div style="width:150px">{svg('gold')}</div><span class="stamp">Draft for discussion · HH-MODEL-0001 · page 2</span></header>
<div class="in">
<span class="eyebrow" style="margin-top:12px">Heal House operating economics · Zonix</span>
<h1>Heal House, built into the <em>building</em></h1>
<p class="sub">The podium is part of the building: funded in the capital stack, carried by the building's budget, and operated by Heal House rent-free. Heal House brings the members, the programs and the wellness days.</p>
<div class="kpis">
<div><b>{N(hh['base']['members'])}</b><span>Members · {P(HH['uptake'])} of homes</span></div>
<div><b>{M(hh['total_rev'])}</b><span>Heal House revenue / yr</span></div>
<div><b>{M(hh['total_e'])}</b><span>Heal House EBITDA · {P(hh['total_e']/hh['total_rev'])}</span></div>
<div><b>{M(hh['ti'])}</b><span>Clinic build-out, in the stack</span></div>
<div><b>{d['dscr']:.2f}x</b><span>Building coverage, still strong</span></div>
</div>
<div class="grid"><div>
<span class="eyebrow">01 · Heal House P&amp;L at Zonix, stabilized</span>
<div class="scroll"><table><tbody>
<tr><td>Membership — {N(hh['base']['members'])} × ${HH['fee']}/mo</td><td class="n">{M(hh['base']['rev'])}</td></tr>
<tr><td>Wellness days — {P(HH['day_capture'])} of short-stay guests × ${HH['day_price']}</td><td class="n">{M(hh['day_rev'])}</td></tr>
<tr><td>Cost of services ({P(HH['cogs'])})</td><td class="n">({M(HH['cogs']*hh['total_rev'])})</td></tr>
<tr><td>Local overhead ({P(HH['local_oh'])})</td><td class="n">({M(HH['local_oh']*hh['total_rev'])})</td></tr>
<tr><td>Rent and occupancy — carried by the building</td><td class="n">$0.0M</td></tr>
</tbody><tfoot><tr><td>EBITDA</td><td class="n">{M(hh['total_e'])}</td></tr></tfoot></table></div>
<span class="eyebrow">02 · What Heal House is worth from this one building</span>
<div class="scroll"><table><thead><tr><th>Method</th><th class="n">Value</th></tr></thead><tbody>
<tr><td>8x EBITDA — health-services low</td><td class="n">{M(8*hh['total_e'])}</td></tr>
<tr><td>12x EBITDA — health-services high</td><td class="n">{M(12*hh['total_e'])}</td></tr>
<tr><td>2.5x recurring revenue</td><td class="n">{M(2.5*hh['total_rev'])}</td></tr>
<tr><td>5.5x revenue — Heal House business plan, Series A</td><td class="n">{M(5.5*hh['total_rev'])}</td></tr>
</tbody><tfoot><tr><td>Plus a clinic Heal House did not pay for</td><td class="n">{M(hh['ti'])}</td></tr></tfoot></table></div>
<span class="eyebrow">03 · If fewer residents join</span>
<p>At {P(HH['low_seniors'])} of seniors and {P(HH['low_towerA'])} of Tower A ({N(hh['low']['members'])} members), membership earns {M(hh['low']['rev'])} and {M(hh['low']['ebitda'])} EBITDA — still profitable, because Heal House carries no rent.</p>
</div><div>
<div class="callout"><span class="eyebrow">04 · The path to 2,000 seniors' homes</span>
<div class="raise">
<div><b>{N(hh['port']['members'])}</b><small>Members at {P(HH['uptake'])} of 2,000 homes</small></div>
<div><b>{M(hh['port']['rev'])}</b><small>Membership revenue a year</small></div>
<div><b>{M(hh['port']['ebitda'])}</b><small>Heal House EBITDA, space provided by each building</small></div>
<div><b>{M(8*hh['port']['ebitda'])}–{M(12*hh['port']['ebitda'])}</b><small>Heal House value at 8–12x EBITDA</small></div>
<div><b>{M(2000*hh['noi_per_senior'])}</b><small>Housing NOI a year at Zonix's ${hh['noi_per_senior']/1e3:,.1f}K per suite</small></div>
<div><b>{M(2000*hh['noi_per_senior']/A['cap_res'])}</b><small>Housing value at a {P(A['cap_res'],2)} cap, before debt</small></div>
</div></div>
<span class="eyebrow">05 · What it does to the building</span>
<p>Giving Heal House the podium rent-free and carrying its operating cost moves Year-1 coverage from {d['dscr_leased']:.2f}x (leased) to <b>{d['dscr']:.2f}x</b>; Year-10 refinance coverage is {d['dscr10']:.2f}x. Short-stay and rental income fund the podium. The building stays well above lender minimums.</p>
<span class="eyebrow">06 · Stated openly</span>
<ul class="c">
<li><b>{P(HH['uptake'])} uptake across all homes is a sponsor assumption.</b> Seniors at that level is credible; families in Tower A are more likely 15–30%.</li>
<li><b>Membership is optional and separate from the lease.</b> If mandatory, CMHC and BCH count it as rent; bundled care services trigger the Retirement Homes Act.</li>
<li><b>${HH['fee']} is about {P(HH['fee']/round(1720*A['aff_factor']))} of an affordable 1-bed rent.</b> Offer a subsidized tier for the {N(d['aff'])} affordable homes.</li>
<li><b>Revenue multiples above 2–3x</b> rely on the HealConnect platform and insurer revenue being real; lead with EBITDA.</li>
<li><b>Common Ground homes are owned by the non-profit</b> and carry affordability covenants; a saleable portfolio needs market seniors' buildings held outside the structure.</li>
</ul>
</div></div></div>
<footer><div style="width:110px;flex:none">{svg('cream')}</div><div><div class="tag">Expert care, tailored to you — in a tranquil, nurturing space where healing can flourish.</div>
<div class="src">Sources: {SRC['hh']} · Wellness days: ASSUMPTION, {P(HH['day_capture'])} of {HOTEL['keys']} keys at {P(HOTEL['occ'])} occupancy buying a ${HH['day_price']} day · Building figures from page 1. Illustrative scenario for discussion — not a valuation, offer, or financial advice.</div></div></footer>
</div></body></html>"""
open('Zonix_HealHouse_OnePager.html','w').write(html)
print("ok")
