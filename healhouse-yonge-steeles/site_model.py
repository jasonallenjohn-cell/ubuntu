"""Heal House at Yonge & Steeles — full site: Tower A rental, Tower B Heal House retirement + wellness stays,
Tower C boutique condo. One model drives every figure in the package. Stack per tower: CMHC MLI Select +
BCH 10-year loan (repaid in full at Year 10) + Building Ontario Fund (Tower B, to Year 20) + City + sponsor equity."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ltt import ltt

GFA=801_556; SHARE_A=44/84; SHARE_B=40/84   # OLT Interim Decision (Oct 17 2023) para 9: 74,467 m2
SRC={
 "gfa":"Approved 44/40-storey scheme: 74,467 m2 / ~801,556 sf GFA, 1,060 units, 510 parking (OLT Interim Decision Oct 17 2023, para 9; final order May 7 2024). Colliers brochure states 858,648 sf. GFA split between towers by storeys; unit counts scaled to GFA",
 "cost":"Arterial hard cost: $370/sf (40–60 storeys), $340/sf (20–40 storeys), Markham (Nov 4–5 2026)",
 "rents":"Arterial comps, Yonge/Steeles leasing: 1BR $2,338 (5), 2BR $2,963 (4); 3BR $3,500 adj. from 1 comp",
 "cmhc":"CMHC Markham zone avg rents 1BR $1,720 · 2BR $1,850 · 3BR $1,834 via Arterial",
 "tax":"Markham multi-res tax 0.8397% (Arterial, 2025)",
 "dc":"ESTIMATE — no Arterial Markham/York DC data; affordable homes assumed DC-exempt",
 "ret":"ASSUMPTION — licensed retirement home with two services: 1-bed $6,000, 2-bed $7,800/mo all-in; 92% occ.; 62% expenses incl. 5% Heal House management fee; 6.0% cap",
 "bof":"Heal House GR brief (Nov 3 2026): ~$151M Building Ontario Fund ask over ~2,000 homes = $75.5K/home",
 "suites":"ASSUMPTION — 80 wellness-stay suites, ADR $185, 72% occ., 30% NOI margin, funded by Sunray cash",
 "hh":"Heal House: $350/mo wellness membership (85% of Tower B, 30% of Tower A residents — sponsor assumptions); outside clients $4.0M/yr at maturity = flagship clinic revenue in HealHouse_15Year_BusinessPlan_Valuation (Jun 2026), ~$100/sf on 40,000 sf, 3-yr ramp; 60% gross margin, 10% local overhead per that plan; podium rent-free",
 "condo":"ASSUMPTION — Tower C 23 storeys, ~180,000 sf (Colliers pre-consultation, Jun 2025), not approved; $1,050/sf base; Arterial income value ~$712/sf as downside",
 "stack":"BCH as a 10-year loan, payment- and interest-free to Year 10, repaid in full from a Year-10 MLI Select refinance (capped at 1.20x coverage; 85% LTV Tower A, 75% Tower B). Building Ontario Fund on Tower B paid 4% a year and repaid at a Year-20 refinance",
}
A=dict(rate=0.0425, amort=50, soft=0.15, aff_factor=0.80, tax=0.008397, mli_share=0.50, city_share=0.05,
       grant_share=0.545, refi_dscr=1.20, bof_pref=0.04, predev=4_000_000,
       price=31_000_000, legal=500_000, months=18, loan_rate=0.065, tax_ins_yr=350_000, unguar_ltv=0.65, appraisal=30_000_000)
r=A["rate"]/12; n=A["amort"]*12; CONST=12*r/(1-(1+r)**-n)
bal=lambda P,m: P*((1+r)**n-(1+r)**m)/((1+r)**n-1)

def land_all():
    return A["price"]+ltt(A["price"])+A["legal"]+A["price"]*A["loan_rate"]*A["months"]/12+A["tax_ins_yr"]*A["months"]/12

def stack(tdc, egi, opex, sponsor, bof, aff, cap, g_rev=0.03, g_opex=0.025, refi_ltv=0.95, bof_to_yr20=False, bch_rate=0.0):
    mli=A["mli_share"]*tdc; city=A["city_share"]*tdc; bch=tdc-mli-city-bof-sponsor
    ads=mli*CONST; noi=egi-opex; to_sp=0
    for y in range(1,11):
        ny=egi*(1+g_rev)**(y-1)-opex*(1+g_opex)**(y-1); c=ny-ads; pref=min(max(c,0),A["bof_pref"]*bof); to_sp+=c-pref
    noi11=egi*(1+g_rev)**10-opex*(1+g_opex)**10; val10=noi11/cap
    refi=min(noi11/A["refi_dscr"]/CONST, refi_ltv*val10); mli10=bal(mli,120)
    bch10=bch*(1+bch_rate)**10; bch10_45=bch*1.045**10
    payoff=mli10+bch10+(0 if bof_to_yr20 else bof); surplus=refi-payoff
    out=dict(tdc=tdc,mli=mli,city=city,bch=bch,bof=bof,sponsor=sponsor,noi=noi,ads=ads,dscr=noi/ads,value=noi/cap,
        noi11=noi11,val10=val10,refi=refi,mli10=mli10,bch10=bch10,payoff=payoff,surplus=surplus,
        room45=refi-mli10-bch10_45-(0 if bof_to_yr20 else bof),to_sp=to_sp,
        mult=(to_sp+max(surplus,0))/sponsor,equity10=val10-refi,bof_to_yr20=bof_to_yr20)
    if bof_to_yr20:
        noi21=egi*(1+g_rev)**20-opex*(1+g_opex)**20; val20=noi21/cap
        refi20=min(noi21/A["refi_dscr"]/CONST, refi_ltv*val20); free20=refi20-bal(refi,120)
        out.update(cf11=noi11-refi*CONST, bof_pay=A["bof_pref"]*bof, val20=val20, free20=free20, bof_cover20=free20-bof)
    return out

def tower_a():
    gfa=GFA*SHARE_A
    k=gfa/449_768
    mix=[("1 Bed",round(222*k),560,1720,2338,55000),("2 Bed",round(261*k),760,1850,2963,70000),("3 Bed",round(72*k),960,1834,3500,75000)]
    units=sum(m[1] for m in mix); gpi=aff=dc=0
    for _,k,sf,mmr,mkt,d in mix:
        a=round(k*0.30); aff+=a; gpi+=((k-a)*mkt+a*round(mmr*A["aff_factor"]))*12; dc+=(k-a)*d
    egi=gpi*0.97; op=units*(1200+900+450+500+300)+0.04*egi
    noi=(egi-op)/(1+A["tax"]/0.0425); opex=egi-noi
    land=land_all()*SHARE_A; hard=370*gfa; tdc=land+hard+dc+A["soft"]*hard+A["predev"]*SHARE_A
    s=stack(tdc,egi,opex,land+A["predev"]*SHARE_A,0,aff,0.0425,refi_ltv=0.85)
    return dict(name="Tower A",gfa=gfa,units=units,aff=aff,mix=mix,gpi=gpi,egi=egi,land=land,hard=hard,dc=dc,**s)

def tower_b(rent=(6000,7800), opex_ratio=0.62, occ=0.92):
    gfa=GFA*SHARE_B; pod=40000; suites_sf=48000; sen_gfa=gfa-pod-suites_sf
    k=sen_gfa/320_880
    mix=[("1 Bed",round(288*k),600,55000),("2 Bed",round(123*k),820,70000)]
    units=sum(x[1] for x in mix); aff=0; gpi=0; dc=0
    for (lab,k,sf,d),rr in zip(mix,rent):
        a=round(k*0.20); aff+=a; gpi+=((k-a)*rr+a*rr*A["aff_factor"])*12; dc+=(k-a)*d
    egi=gpi*occ; opex=opex_ratio*egi
    land_b=land_all()*SHARE_B; land_res=land_b*(sen_gfa+pod)/gfa; land_suites=land_b-land_res
    hard=370*(sen_gfa+pod)+100*pod+40*sen_gfa+15000*units
    tdc=land_res+hard+dc+A["soft"]*hard+A["predev"]*SHARE_B
    sponsor=land_res+A["predev"]*SHARE_B; bof_base=75_500*units
    gap=tdc*(1-A["mli_share"]-A["city_share"])-sponsor-bof_base
    bof=bof_base+0.545*gap        # Fund takes the long-term share so BCH is fully repaid at Year 10
    s=stack(tdc,egi,opex,sponsor,bof,aff,0.06,0.03,0.03,0.75,bof_to_yr20=True)
    s["bof_base"]=bof_base
    # wellness-stay suites (Sunray) and Heal House income
    keys=80; s_rev=keys*185*365*0.72*1.10; s_noi=0.30*s_rev
    s_cost=land_suites+(370*suites_sf+keys*40000)*(1+A["soft"])+25*suites_sf
    nights=keys*365*0.72; days=nights*0.25*150
    hh_fee=0.05*egi; hh_days=days*0.5
    return dict(name="Tower B",gfa=gfa,units=units,aff=aff,gpi=gpi,egi=egi,opex_b=opex,land=land_res,hard=hard,dc=dc,
        keys=keys,s_rev=s_rev,s_noi=s_noi,s_cost=s_cost,days=days,hh_fee=hh_fee,hh_days=hh_days,**s)

def tower_c(psf=1050):
    gfa=180_000; mix=[("1 Bed",110,520,70000),("2 Bed",120,680,95000),("3 Bed",20,870,105000)]
    units=sum(m[1] for m in mix); nsa=sum(m[1]*m[2] for m in mix)
    rev=nsa*psf; hard=340*gfa; soft=A["soft"]*hard; dc=sum(m[1]*m[3] for m in mix)
    sell=0.06*rev; fin=0.05*(hard+soft); rezone=1_500_000; land=35*gfa
    cost=hard+soft+dc+sell+fin+rezone
    return dict(name="Tower C",gfa=gfa,units=units,nsa=nsa,psf=psf,rev=rev,hard=hard,soft=soft,dc=dc,sell=sell,fin=fin,
        rezone=rezone,land=land,cost=cost,profit_pre_land=rev-cost,profit=rev-cost-land,margin=(rev-cost-land)/rev,
        equity=0.20*(cost+land))

HH=dict(fee=350, uptake_b=0.85, uptake_a=0.30, outside=4_000_000, ramp=(0.45,0.70,0.90,1.0),
        gm=0.60, oh=0.10, podium_sf=40_000)
def heal_house(a,b,uptake_a=None,outside=None):
    h=HH; ua=h["uptake_a"] if uptake_a is None else uptake_a; out=h["outside"] if outside is None else outside
    mb=round(h["uptake_b"]*b["units"]); ma=round(ua*a["units"])
    lines={"Tower B resident memberships":mb*h["fee"]*12, "Tower A resident memberships":ma*h["fee"]*12,
           "Outside clients — community clinic & wellness":out, "Wellness days — suite guests":b["days"]}
    service=sum(lines.values()); margin=h["gm"]-h["oh"]
    ebitda=service*margin+b["hh_fee"]
    return dict(mb=mb,ma=ma,lines=lines,service=service,fee=b["hh_fee"],rev=service+b["hh_fee"],ebitda=ebitda,
        margin=margin,rev_psf=service/h["podium_sf"],ramp=[service*r*margin+b["hh_fee"] for r in h["ramp"]],
        outside_share=out/service)

def site():
    a=tower_a(); b=tower_b(); c=tower_c()
    la=land_all(); unguar=A["unguar_ltv"]*A["appraisal"]; guar=A["price"]-unguar
    acq_eq=la-A["price"]+A["predev"]
    hh=heal_house(a,b)
    return dict(A=a,B=b,C=c,land_all=la,guar=guar,unguar=unguar,acq_eq=acq_eq,
        homes=a["units"]+b["units"]+c["units"],aff=a["aff"]+b["aff"],
        sponsor=a["sponsor"]+b["sponsor"], bof=b["bof"], bch=a["bch"]+b["bch"], city=a["city"]+b["city"],
        mli=a["mli"]+b["mli"], tdc_rent=a["tdc"]+b["tdc"], sunray=b["s_cost"], condo_eq=c["equity"],
        hh=hh, hh_rev=hh["rev"], hh_e=hh["ebitda"])

if __name__=="__main__":
    s=site()
    for t in ("A","B"):
        x=s[t]; print(t,{k:round(v/1e6,2) if isinstance(v,float) and abs(v)>1e4 else (round(v,3) if isinstance(v,float) else v) for k,v in x.items() if k not in("mix","name")})
    print("C",{k:round(v/1e6,2) if isinstance(v,float) and abs(v)>1e4 else v for k,v in s["C"].items() if k not in("mix","name")})
    print({k:round(v/1e6,2) if isinstance(v,float) and abs(v)>1e4 else v for k,v in s.items() if k not in("A","B","C")})
    for p in (712,900,1050,1200): c=tower_c(p); print("condo",p,round(c["profit"]/1e6,1),round(c["margin"]*100,1))
    for kw in ({},dict(opex_ratio=0.65,occ=0.90)):
        b=tower_b(**kw); print("B",kw,round(b["noi"]/1e6,2),round(b["dscr"],2),round(b["surplus"]/1e6,1),round(b["mult"],1))
