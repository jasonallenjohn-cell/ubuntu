import sys, os, re, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seniors_model as S
hy=S.hybrid(); d=hy['d']; A=S.A; HH=S.HH; SU=S.SUITES; PO=S.PODIUM
B='/root/.claude/skills/synced/f8734239-31ba-4ced-bc8b-cbf00346c7d5_28a6848d-eac9-43f7-925d-965e3f535b85/heal-house-brand/assets/'
svg=lambda c: open(B+f'healhouse-logo-{c}.svg').read().replace('<svg ',"<svg role='img' aria-label='Heal House' ",1)
css=re.search(r'<style>(.*?)</style>',open('Zonix_HealHouse_OnePager.html').read(),re.S).group(1)
M=lambda x:(f"(${-x/1e6:,.1f}M)" if x<0 else f"${x/1e6:,.1f}M"); N=lambda x:f"{x:,.0f}"; P=lambda x,k=0:f"{x*100:.{k}f}%"; K=lambda x:(f"${x/1e3:,.1f}K" if x<1e5 else f"${x/1e3:,.0f}K")
# funding split
sponsor=hy['sponsor']
# rent-premium sensitivity
base=copy.deepcopy(S.MIX); sens=[]
for p in (0,0.10,0.15):
    S.MIX=[(l,n,sf,mmr,mkt*(1+p),dc) for l,n,sf,mmr,mkt,dc in base]; x=S.hybrid()
    sens.append((p,x['dscr'],x['surplus'],x['mult'],x['irr']))
S.MIX=base
mix_rows="".join(f"<tr><td>55+ {l}</td><td class='n'>{N(n)}</td><td class='n'>{N(sf)} sf</td><td class='n'>${mkt:,.0f}</td><td class='n'>${round(mmr*A['aff_factor']):,}</td></tr>" for l,n,sf,mmr,mkt,dc in S.MIX)
sens_rows="".join(f"<tr><td>{'Market comps' if p==0 else '+'+P(p)+' seniors premium'}</td><td class='n'>{dc:.2f}x</td><td class='n'>{M(sp)}</td><td class='n'>{mu:.1f}x · {P(ir,1)}</td></tr>" for p,dc,sp,mu,ir in sens)
html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zonix Seniors Living</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Belleza&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Montserrat:wght@400;500;600;700&display=swap">
<style>{css} td{{padding:3px 8px}} footer{{padding:9px .5in}} header.mh{{padding:.22in .5in .08in}} .kpis div{{padding:6px 10px}} .sub{{margin-bottom:8px}}</style></head><body><div class="page">
<header class="mh"><div style="width:150px">{svg('gold')}</div><span class="stamp">Draft for discussion · HH-MODEL-0003 · Nov 5 2026</span></header>
<div class="in">
<span class="eyebrow" style="margin-top:12px">Heal House Seniors Living Program · York Region · 36–48 Steeles Ave E, Markham</span>
<h1>Seniors' living at Yonge &amp; Steeles, with care <em>built in</em></h1>
<p class="sub">Tower B of an approved two-tower site, bought out of receivership: {N(d['units'])} independent-living seniors' homes, {N(d['aff'])} held affordable for 40 years, over a Heal House wellness podium. A York Region site for the Building Ontario Fund program.</p>
<div class="kpis">
<div><b>{N(d['units'])} homes</b><span>{N(d['aff'])} affordable · 40 yrs</span></div>
<div><b>{M(d['tdc'])}</b><span>Project cost · {K(d['cost_per'])}/home</span></div>
<div><b>{M(d['noi'])}</b><span>Stabilized NOI</span></div>
<div><b>{hy['dscr']:.2f}x</b><span>Debt coverage, Yr 1</span></div>
<div><b>{M(d['bof'])}</b><span>Building Ontario Fund</span></div>
</div>
<div class="grid"><div>
<span class="eyebrow">01 · Program — Tower B</span>
<div class="scroll"><table><thead><tr><th>Home</th><th class="n">Count</th><th class="n">Size</th><th class="n">Market</th><th class="n">Affordable</th></tr></thead><tbody>{mix_rows}
<tr><td>Heal House podium (in the building)</td><td class="n">—</td><td class="n">{N(PO['sf'])} sf</td><td class="n" colspan="2">no rent</td></tr>
</tbody><tfoot><tr><td>Total · {N(d['gfa'])} sf GFA</td><td class="n">{N(d['units'])}</td><td class="n"></td><td class="n" colspan="2">{N(d['aff'])} at {P(A['aff_factor'])} of CMHC rent</td></tr></tfoot></table></div>
<span class="eyebrow">02 · Capital stack</span>
<div class="scroll"><table><thead><tr><th>Source</th><th class="n">Amount</th><th class="n">Share</th></tr></thead><tbody>
<tr><td>CMHC MLI Select — 4.25%, 50-yr amortization</td><td class="n">{M(hy['mli'])}</td><td class="n">{P(hy['mli']/hy['tdc'],1)}</td></tr>
<tr><td><b>Building Ontario Fund</b> — {K(A['bof_per_home'])}/home, {P(S.H['bof_pref'])} current return</td><td class="n">{M(hy['bof'])}</td><td class="n">{P(hy['bof']/hy['tdc'],1)}</td></tr>
<tr><td>BCH contribution — vests Yrs 1–10 vs affordable homes</td><td class="n">{M(hy['grant'])}</td><td class="n">{P(hy['grant']/hy['tdc'],1)}</td></tr>
<tr><td>BCH mezz — no payments, repaid at Year 10</td><td class="n">{M(hy['mezz'])}</td><td class="n">{P(hy['mezz']/hy['tdc'],1)}</td></tr>
<tr><td>City of Markham — incentives / DC relief</td><td class="n">{M(hy['city'])}</td><td class="n">{P(hy['city']/hy['tdc'],1)}</td></tr>
<tr><td>Sponsor equity — land share + pre-development</td><td class="n">{M(sponsor)}</td><td class="n">{P(sponsor/hy['tdc'],1)}</td></tr>
</tbody><tfoot><tr><td>Total project cost</td><td class="n">{M(d['tdc'])}</td><td class="n">100%</td></tr></tfoot></table></div>
<span class="eyebrow">03 · How the site comes together</span>
<ol>
<li><b>LiUNA's pension backs Nesting Ground's guarantee pool</b>, which lifts the land loan to the full {M(A['price'])} price.</li>
<li><b>The site is bought from the receiver</b>; Tower B carries {M(d['land_B'])} of the all-in land cost by floor area.</li>
<li><b>Tower A</b> proceeds separately as rental with its own partner; <b>80 family &amp; recovery suites</b> ({M(d['s_cost'])}) are funded outside this stack (Sunray).</li>
<li><b>At construction close</b>, the stack retires the land loan and funds the build.</li><li><b>At Year 10</b>, an MLI Select refinance repays BCH and the Fund; Heal House keeps the building.</li>
</ol>
</div><div>
<div class="callout"><span class="eyebrow">04 · Year 10: BCH and the Fund are repaid</span>
<div class="scroll" style="margin:6px 0 6px"><table><tbody>
<tr><td>Year-11 NOI · value at {P(A['cap'],2)}</td><td class="n">{M(hy['noi11'])} · {M(hy['val10'])}</td></tr>
<tr><td>New MLI Select loan at {S.H['refi_dscr']:.2f}x</td><td class="n">{M(hy['refi'])}</td></tr>
<tr><td>Repays first mortgage balance</td><td class="n">({M(hy['mli10'])})</td></tr>
<tr><td>Repays BCH mezz</td><td class="n">({M(hy['mezz10'])})</td></tr>
<tr><td>Repays the Building Ontario Fund</td><td class="n">({M(hy['bof'])})</td></tr>
</tbody><tfoot><tr><td>Cash back to sponsor at Year 10</td><td class="n">{M(hy['surplus'])}</td></tr></tfoot></table></div>
<p style="margin:0 0 4px">Sponsor: {M(sponsor)} in → {M(hy['to_sponsor'])} cash flow + {M(hy['surplus'])} at refinance = <b>{hy['mult']:.1f}x, {P(hy['irr'],1)} IRR</b>, and Heal House owns a {M(hy['val10'])} building with {M(hy['val10']-hy['refi'])} of equity. A seniors' rent premium lifts it:</p>
<div class="scroll" style="margin-bottom:0"><table><thead><tr><th>Market rent</th><th class="n">Coverage</th><th class="n">Yr-10 cash</th><th class="n">Sponsor</th></tr></thead><tbody>{sens_rows}</tbody></table></div></div>
<span class="eyebrow">05 · Why the Building Ontario Fund</span>
<ul class="c">
<li><b>Patient capital makes the 40-year covenant viable</b> for the {N(d['aff'])} affordable homes.</li>
<li><b>Pension partner alongside:</b> LiUNA, through Nesting Ground's guarantee pool.</li>
<li><b>Shovel-ready land:</b> zoning approved, priced through a court process, transit at Yonge &amp; Steeles.</li>
<li><b>Fits the program:</b> {N(d['units'])} of the ~2,000 homes, at the program's {K(A['bof_per_home'])} per home.</li>
</ul>
<span class="eyebrow">06 · Stated openly</span>
<ul class="c">
<li>The Fund's {P(S.H['bof_pref'])} return and Year-10 repayment are placeholders to set with the Fund.</li><li>BCH mezz modelled interest-free to Year 10, as in Common Ground; at 4.5% accrual the Year-10 cash falls to {M(S.hybrid(0.045)['surplus'])}.</li><li>BCH contribution is {K(hy['grant_per_aff'])} per affordable home; BCH may want a non-profit co-owner on the affordable homes.</li>
<li>Development charges ({M(d['dc'])}) are estimates; approvals, stamped drawings and the Tower B floor-area split are unverified.</li>
</ul>
</div></div></div>
<footer><div style="width:110px;flex:none">{svg('cream')}</div><div><div class="tag">A sanctuary for healing.</div>
<div class="src">Sources: {' · '.join(S.SRC[k] for k in ['gfa','constr','rents','cmhc','tax','dc','bof','aff','hybrid'])}. Illustrative scenario for discussion — not a valuation, offer, commitment or financial advice. Subject to receiver and court approval, CMHC, Building Ontario Fund, BCH and City of Markham approvals, and LiUNA trustee approval.</div></div></footer>
<div class="pb"></div>
<header class="mh"><div style="width:150px">{svg('gold')}</div><span class="stamp">Draft for discussion · HH-MODEL-0003 · page 2</span></header>
<div class="in">
<span class="eyebrow" style="margin-top:12px">Heal House operating economics · Tower B</span>
<h1>Heal House, built into the <em>building</em></h1>
<p class="sub">The podium is funded in the capital stack and carried by the building's budget. Heal House operates it rent-free and brings the members, the programs and the wellness days.</p>
<div class="kpis">
<div><b>{N(d['mem'])}</b><span>Members · {P(HH['uptake'])} of residents</span></div>
<div><b>{M(d['hh_rev'])}</b><span>Heal House revenue / yr</span></div>
<div><b>{M(d['hh_e'])}</b><span>EBITDA · {P(d['hh_e']/d['hh_rev'])}</span></div>
<div><b>{M(PO['sf']*PO['ti'])}</b><span>Clinic build-out, in the stack</span></div>
<div><b>$0</b><span>Rent to Heal House</span></div>
</div>
<div class="grid"><div>
<span class="eyebrow">01 · Heal House P&amp;L at Tower B</span>
<div class="scroll"><table><tbody>
<tr><td>Membership — {N(d['mem'])} × ${HH['fee']}/mo</td><td class="n">{M(d['m_rev'])}</td></tr>
<tr><td>Wellness days — {P(HH['day_capture'])} of suite guests × ${HH['day_price']}</td><td class="n">{M(d['d_rev'])}</td></tr>
<tr><td>Cost of services ({P(HH['cogs'])})</td><td class="n">({M(HH['cogs']*d['hh_rev'])})</td></tr>
<tr><td>Local overhead ({P(HH['oh'])})</td><td class="n">({M(HH['oh']*d['hh_rev'])})</td></tr>
<tr><td>Rent and occupancy — carried by the building</td><td class="n">$0.0M</td></tr>
</tbody><tfoot><tr><td>EBITDA</td><td class="n">{M(d['hh_e'])}</td></tr></tfoot></table></div>
<span class="eyebrow">02 · Value to Heal House from this site</span>
<div class="scroll"><table><tbody>
<tr><td>8x EBITDA</td><td class="n">{M(8*d['hh_e'])}</td></tr>
<tr><td>12x EBITDA</td><td class="n">{M(12*d['hh_e'])}</td></tr>
</tbody><tfoot><tr><td>Plus a clinic Heal House did not pay for</td><td class="n">{M(PO['sf']*PO['ti'])}</td></tr></tfoot></table></div>
</div><div>
<span class="eyebrow">03 · Toward 2,000 homes</span>
<div class="scroll"><table><tbody>
<tr><td>Members at {P(HH['uptake'])} of 2,000 homes</td><td class="n">{N(round(HH['uptake']*2000))}</td></tr>
<tr><td>Membership revenue / yr</td><td class="n">{M(round(HH['uptake']*2000)*HH['fee']*12)}</td></tr>
<tr><td>EBITDA, space provided by each building</td><td class="n">{M(round(HH['uptake']*2000)*HH['fee']*12*(1-HH['cogs']-HH['oh']))}</td></tr>
<tr><td>Housing NOI at Tower B's per-home rate</td><td class="n">{M(2000*d['noi']/d['units'])}</td></tr>
</tbody></table></div>
<span class="eyebrow">04 · Stated openly</span>
<ul class="c">
<li>{P(HH['uptake'])} uptake is a sponsor assumption; membership is optional and separate from the lease.</li>
<li>${HH['fee']} is about {P(HH['fee']/round(1720*A['aff_factor']))} of an affordable 1-bed rent — offer a subsidized tier.</li>
<li>Cost of services and margins follow the Heal House 15-year plan.</li>
<li>Independent living only — bundling two care services triggers Ontario's Retirement Homes Act.</li>
<li>Tower A's partner must fund its share of the land at closing.</li>
</ul>
</div></div></div>
<footer><div style="width:110px;flex:none">{svg('cream')}</div><div><div class="tag">Expert care, tailored to you — in a tranquil, nurturing space where healing can flourish.</div>
<div class="src">Sources: {S.SRC['hh']} · {S.SRC['suites']}. Illustrative scenario for discussion — not a valuation, offer, or financial advice.</div></div></footer>
</div></body></html>"""
open('Zonix_TowerB_Seniors_BOF.html','w').write(html); print('ok')
