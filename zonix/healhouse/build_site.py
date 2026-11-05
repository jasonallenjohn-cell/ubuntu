import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_model as m
s=m.site(); a,b,c=s["A"],s["B"],s["C"]; A=m.A
B='/root/.claude/skills/synced/f8734239-31ba-4ced-bc8b-cbf00346c7d5_28a6848d-eac9-43f7-925d-965e3f535b85/heal-house-brand/assets/'
svg=lambda k: open(B+f'healhouse-logo-{k}.svg').read().replace('<svg ',"<svg role='img' aria-label='Heal House' ",1)
css=re.search(r'<style>(.*?)</style>',open('Zonix_HealHouse_OnePager.html').read(),re.S).group(1)
M=lambda x:(f"(${-x/1e6:,.1f}M)" if x<0 else f"${x/1e6:,.1f}M"); N=lambda x:f"{x:,.0f}"; P=lambda x,k=0:f"{x*100:.{k}f}%"; K=lambda x:(f"${x/1e3:,.1f}K" if x<1e5 else f"${x/1e3:,.0f}K")
total=s['tdc_rent']+s['sunray']+c['cost']+c['land']
def hdr(pg): return f"<header class='mh'><div style='width:150px'>{svg('gold')}</div><span class='stamp'>Draft for discussion · HH-MODEL-0004 · {pg}</span></header>"
def foot(tag,src): return f"<footer><div style='width:110px;flex:none'>{svg('cream')}</div><div><div class='tag'>{tag}</div><div class='src'>{src}</div></div></footer>"
def stack_tbl(t,bof_label=True):
    rows=[("CMHC MLI Select — 4.25%, 50-yr",t['mli']),("Building Ontario Fund — patient capital",t['bof']) if t['bof'] else None,
          ("BCH contribution — vests Yrs 1–10",t['grant']),("BCH mezz — repaid at Year 10",t['mezz']),
          ("City of Markham",t['city']),("Sponsor equity — land + pre-development",t['sponsor'])]
    rows=[r for r in rows if r]
    body="".join(f"<tr><td>{l}</td><td class='n'>{M(v)}</td><td class='n'>{P(v/t['tdc'],1)}</td></tr>" for l,v in rows)
    return f"<div class='scroll'><table><thead><tr><th>Source</th><th class='n'>Amount</th><th class='n'>Share</th></tr></thead><tbody>{body}</tbody><tfoot><tr><td>Total cost</td><td class='n'>{M(t['tdc'])}</td><td class='n'>100%</td></tr></tfoot></table></div>"
def yr10(t):
    return f"""<div class='scroll'><table><tbody>
<tr><td>Year-11 NOI · value</td><td class='n'>{M(t['noi11'])} · {M(t['val10'])}</td></tr>
<tr><td>New MLI Select loan at {A['refi_dscr']:.2f}x</td><td class='n'>{M(t['refi'])}</td></tr>
<tr><td>Repays mortgage, BCH mezz{', the Fund' if t['bof'] else ''}</td><td class='n'>({M(t['payoff'])})</td></tr>
</tbody><tfoot><tr><td>Cash to sponsor · sponsor return</td><td class='n'>{M(t['surplus'])} · {t['mult']:.1f}x</td></tr></tfoot></table></div>"""
srcline=' · '.join(m.SRC[k] for k in m.SRC)
html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Zonix Health Community</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Belleza&family=Lora:ital,wght@0,400;0,500;1,400;1,500&family=Montserrat:wght@400;500;600;700&display=swap">
<style>{css} td{{padding:3.2px 8px}} .kpis div{{padding:6px 10px}} .sub{{margin-bottom:8px}} footer{{padding:9px .5in}} header.mh{{padding:.22in .5in .08in}}</style></head><body><div class="page">
{hdr('Nov 5 2026')}
<div class="in">
<span class="eyebrow" style="margin-top:12px">36–48 Steeles Ave E / 37–49 Highland Park Blvd · Markham · in receivership</span>
<h1>Three towers, one <em>healing</em> community</h1>
<p class="sub">An approved two-tower site at Yonge &amp; Steeles, bought out of receivership: affordable and market rental, a Heal House retirement residence with wellness stays, and a boutique condo tower — anchored by the Building Ontario Fund, BCH and CMHC.</p>
<div class="kpis">
<div><b>{N(s['homes'])} homes</b><span>{N(s['aff'])} affordable · +{b['keys']} suites</span></div>
<div><b>{M(total)}</b><span>Total program cost</span></div>
<div><b>{M(s['bof'])}</b><span>Building Ontario Fund</span></div>
<div><b>{M(s['bch'])}</b><span>BCH, mezz repaid Yr 10</span></div>
<div><b>{M(s['sponsor'])}</b><span>Sponsor equity, rental towers</span></div>
</div>
<div class="grid"><div>
<span class="eyebrow">01 · The three towers</span>
<div class="scroll"><table><thead><tr><th>Tower</th><th class="n">Homes</th><th class="n">Cost</th><th class="n">Yr-1 NOI / profit</th></tr></thead><tbody>
<tr><td><b>A</b> · 44 storeys · affordable + market rental</td><td class="n">{N(a['units'])} ({N(a['aff'])} aff.)</td><td class="n">{M(a['tdc'])}</td><td class="n">{M(a['noi'])}</td></tr>
<tr><td><b>B</b> · 40 storeys · Heal House retirement residence</td><td class="n">{N(b['units'])} ({N(b['aff'])} aff.)</td><td class="n">{M(b['tdc'])}</td><td class="n">{M(b['noi'])}</td></tr>
<tr><td><b>B</b> · wellness-stay suites + Heal House podium</td><td class="n">{b['keys']} keys</td><td class="n">{M(b['s_cost'])}</td><td class="n">{M(b['s_noi'])}</td></tr>
<tr><td><b>C</b> · 23 storeys · boutique condo (to be approved)</td><td class="n">{N(c['units'])}</td><td class="n">{M(c['cost']+c['land'])}</td><td class="n">{M(c['profit'])} profit</td></tr>
</tbody><tfoot><tr><td>Total</td><td class="n">{N(s['homes'])}</td><td class="n">{M(total)}</td><td class="n"></td></tr></tfoot></table></div>
<span class="eyebrow">02 · How the site comes together</span>
<ol>
<li><b>LiUNA's pension backs Nesting Ground's guarantee pool</b>, lifting the land loan from {M(s['unguar'])} to the full {M(A['price'])} price — an {M(s['guar'])} guarantee.</li>
<li><b>Buy from the receiver</b> and pay out the secured lenders; {M(s['acq_eq'])} of equity at purchase covers transfer tax, carry and pre-development.</li>
<li><b>Tower A and Tower B close construction financing</b>; each tower's stack retires its share of the land loan.</li>
<li><b>Sunray funds the wellness-stay suites</b> ({M(s['sunray'])}); <b>Tower C</b> follows once rezoned, sold through presales.</li>
<li><b>At Year 10</b>, refinancing repays BCH's mezzanine and the Fund; the sponsors keep the buildings.</li>
</ol>
</div><div>
<div class="callout"><span class="eyebrow">03 · What we need to raise</span>
<div class="raise">
<div><b>{M(s['bof'])}</b><small>Building Ontario Fund — Tower B, {K(75500)}/home</small></div>
<div><b>{M(s['bch'])}</b><small>BCH — {M(a['grant']+b['grant'])} contribution + {M(a['mezz']+b['mezz'])} mezz</small></div>
<div><b>{M(s['mli'])}</b><small>CMHC MLI Select, Towers A + B</small></div>
<div><b>{M(s['city'])}</b><small>City of Markham — incentives / DC relief</small></div>
<div><b>{M(s['sponsor'])}</b><small>Sponsor equity — {M(s['acq_eq'])} at purchase, rest at construction close</small></div>
<div><b>{M(s['guar'])}</b><small>Land-loan guarantee — LiUNA via Nesting Ground</small></div>
<div><b>{M(s['sunray'])}</b><small>Sunray — wellness-stay suites</small></div>
<div><b>{M(s['condo_eq'])}</b><small>Tower C equity (20% of cost), later phase</small></div>
</div></div>
<span class="eyebrow">04 · What it returns</span>
<div class="scroll"><table><tbody>
<tr><td>Tower A — Year-10 cash · sponsor multiple</td><td class="n">{M(a['surplus'])} · {a['mult']:.1f}x</td></tr>
<tr><td>Tower B — Year-10 cash · sponsor multiple</td><td class="n">{M(b['surplus'])} · {b['mult']:.1f}x</td></tr>
<tr><td>Tower C — condo profit at ${c['psf']:,}/sf</td><td class="n">{M(c['profit'])} · {P(c['margin'])}</td></tr>
<tr><td>Heal House — fees, wellness days, memberships</td><td class="n">{M(s['hh_e'])} EBITDA/yr</td></tr>
</tbody></table></div>
<p>BCH and the Fund are repaid in full at Year 10 in both rental towers. The sponsors then own Tower A ({M(a['equity10'])} equity) and Tower B ({M(b['equity10'])} equity).</p>
</div></div></div>
{foot('A sanctuary for healing.', 'Sources: '+srcline+'. Illustrative scenario for discussion — not a valuation, offer, commitment or financial advice. Subject to receiver and court approval, CMHC, BCH, Building Ontario Fund and City of Markham approvals, LiUNA trustee approval and legal review.')}
<div class="pb"></div>
{hdr('page 2 · Tower B')}
<div class="in">
<span class="eyebrow" style="margin-top:12px">Tower B · Heal House retirement residence · Building Ontario Fund</span>
<h1>Retirement living, with care <em>built in</em></h1>
<p class="sub">{N(b['units'])} retirement suites with two services — {N(b['aff'])} held affordable for 40 years — over a Heal House podium, with {b['keys']} wellness-stay suites for families, recovery and wellness days.</p>
<div class="kpis">
<div><b>{M(b['egi'])}</b><span>Revenue, rent + services</span></div>
<div><b>{M(b['noi'])}</b><span>NOI after {P(m.tower_b.__defaults__[1])} expenses</span></div>
<div><b>{b['dscr']:.2f}x</b><span>Debt coverage, Yr 1</span></div>
<div><b>{M(b['bof'])}</b><span>Building Ontario Fund</span></div>
<div><b>{M(b['surplus'])}</b><span>Cash at Yr-10 refi</span></div>
</div>
<div class="grid"><div>
<span class="eyebrow">01 · Capital stack — Tower B residence</span>
{stack_tbl(b)}
<span class="eyebrow">02 · Year 10 — BCH and the Fund repaid</span>
{yr10(b)}
</div><div>
<span class="eyebrow">03 · Heal House income on the site</span>
<div class="scroll"><table><tbody>
<tr><td>Management fee — 5% of Tower B revenue</td><td class="n">{M(b['hh_fee'])}</td></tr>
<tr><td>Wellness days — 25% of suite guests × $150 (50% margin)</td><td class="n">{M(b['hh_days'])}</td></tr>
<tr><td>Tower A memberships — {N(s['hh_members_a'])} × $350/mo (50% margin)</td><td class="n">{M(0.5*s['hh_members_a']*350*12)}</td></tr>
</tbody><tfoot><tr><td>Heal House EBITDA · podium rent-free</td><td class="n">{M(s['hh_e'])}</td></tr></tfoot></table></div>
<span class="eyebrow">04 · If it runs leaner</span>
<p>At 65% expenses and 90% occupancy, NOI is {M(m.tower_b(opex_ratio=0.65,occ=0.90)['noi'])}, coverage {m.tower_b(opex_ratio=0.65,occ=0.90)['dscr']:.2f}x, and the Year-10 refinance still repays BCH and the Fund with {M(m.tower_b(opex_ratio=0.65,occ=0.90)['surplus'])} to spare.</p>
<span class="eyebrow">05 · Stated openly</span>
<ul class="c">
<li><b>Licensed retirement home</b> under Ontario's Retirement Homes Act, like Heal House Listowel; an experienced operator or management contract until Heal House has a track record.</li>
<li><b>Rents of $6,000 / $7,800 all-in need a Markham market study.</b> Earlier Listowel/Barrie figures (~$14,000/room) are well above market and are not used.</li>
<li><b>BCH contribution is {K(b['grant_per_aff'])} per affordable home</b> — a hard ask for care housing; a larger Fund share would reduce it.</li>
<li>The Fund's {P(A['bof_pref'])} return and Year-10 exit are placeholders; CMHC's retirement-home route to be confirmed.</li>
</ul>
</div></div></div>
{foot('Expert care, tailored to you — in a tranquil, nurturing space where healing can flourish.', 'Sources: '+m.SRC['ret']+' · '+m.SRC['bof']+' · '+m.SRC['suites']+'. Illustrative scenario for discussion.')}
<div class="pb"></div>
{hdr('page 3 · Towers A and C')}
<div class="in">
<span class="eyebrow" style="margin-top:12px">Tower A · affordable + market rental · Tower C · boutique condo</span>
<h1>Homes for every <em>stage</em> of life</h1>
<p class="sub">Tower A carries the affordable and market rental on the existing approval. Tower C adds a boutique condo tower once rezoned — the condo profit is the program's upside.</p>
<div class="grid"><div>
<span class="eyebrow">01 · Tower A — {N(a['units'])} rental homes, {N(a['aff'])} affordable</span>
<div class="kpis" style="grid-template-columns:repeat(3,1fr)">
<div><b>{M(a['noi'])}</b><span>Stabilized NOI</span></div><div><b>{a['dscr']:.2f}x</b><span>Coverage, Yr 1</span></div><div><b>{M(a['value'])}</b><span>Value at 4.25%</span></div></div>
{stack_tbl(a)}
<span class="eyebrow">02 · Tower A at Year 10</span>
{yr10(a)}
</div><div>
<span class="eyebrow">03 · Tower C — {N(c['units'])} boutique condos</span>
<div class="scroll"><table><tbody>
<tr><td>Sales — {N(c['nsa'])} sf at ${c['psf']:,}/sf</td><td class="n">{M(c['rev'])}</td></tr>
<tr><td>Construction — {N(c['gfa'])} sf at $340/sf</td><td class="n">({M(c['hard'])})</td></tr>
<tr><td>Soft costs, financing, rezoning</td><td class="n">({M(c['soft']+c['fin']+c['rezone'])})</td></tr>
<tr><td>Development charges (estimate)</td><td class="n">({M(c['dc'])})</td></tr>
<tr><td>Sales and marketing (6%)</td><td class="n">({M(c['sell'])})</td></tr>
<tr><td>Land for the added density ($35/sf)</td><td class="n">({M(c['land'])})</td></tr>
</tbody><tfoot><tr><td>Profit · margin on sales</td><td class="n">{M(c['profit'])} · {P(c['margin'])}</td></tr></tfoot></table></div>
<span class="eyebrow">04 · Condo pricing decides it</span>
<div class="scroll"><table><thead><tr><th>Sale price</th><th class="n">Profit</th><th class="n">Margin</th></tr></thead><tbody>
{''.join(f"<tr><td>${p:,}/sf{' — Arterial income value' if p==712 else ''}</td><td class='n'>{M(m.tower_c(p)['profit'])}</td><td class='n'>{P(m.tower_c(p)['margin'])}</td></tr>" for p in (712,900,1050,1200))}
</tbody></table></div>
<span class="eyebrow">05 · Stated openly</span>
<ul class="c">
<li><b>Tower C is not approved.</b> Markham staff raised concerns about the 49/44/24-storey version; rezoning takes 12–24 months.</li>
<li><b>GTA condo presales are weak;</b> lenders want 60–70% presold. Below ~$900/sf the tower is better held as rental.</li>
<li>Tower A's Year-10 cash relies on the BCH contribution ({K(a['grant_per_aff'])} per affordable home); Tower A can also run under Ubuntu's Common Ground structure.</li>
<li>Development charges are estimates; tower floor areas are split by storeys pending stamped drawings.</li>
</ul>
</div></div></div>
{foot('Heal the whole person.', 'Sources: '+m.SRC['cost']+' · '+m.SRC['rents']+' · '+m.SRC['cmhc']+' · '+m.SRC['condo']+' · '+m.SRC['dc']+'. Illustrative scenario for discussion — not a valuation, offer, or financial advice.')}
</div></body></html>"""
open('Zonix_Site_Package.html','w').write(html); print('ok', M(total))
