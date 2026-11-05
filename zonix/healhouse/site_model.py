"""Zonix — full site: Tower A rental, Tower B Heal House retirement + wellness stays, Tower C boutique condo.
One model drives every figure in the package. Stack per tower: CMHC MLI Select + BCH split tranche (Year-10 payout)
+ Building Ontario Fund (seniors) + City + sponsor equity."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import ltt

GFA=858_648; SHARE_A=44/84; SHARE_B=40/84
SRC={
 "gfa":"Approved 40/44-storey scheme, 858,648 sf (Colliers brochure, Jun 2026); split between towers by storeys — unverified vs stamped set",
 "cost":"Arterial hard cost: $370/sf (40–60 storeys), $340/sf (20–40 storeys), Markham (Nov 4–5 2026)",
 "rents":"Arterial comps, Yonge/Steeles leasing: 1BR $2,338 (5), 2BR $2,963 (4); 3BR $3,500 adj. from 1 comp",
 "cmhc":"CMHC Markham zone avg rents 1BR $1,720 · 2BR $1,850 · 3BR $1,834 via Arterial",
 "tax":"Markham multi-res tax 0.8397% (Arterial, 2025)",
 "dc":"ESTIMATE — no Arterial Markham/York DC data; affordable homes assumed DC-exempt",
 "ret":"ASSUMPTION — licensed retirement home with two services: 1-bed $6,000, 2-bed $7,800/mo all-in; 92% occ.; 62% expenses incl. 5% Heal House management fee; 6.0% cap",
 "bof":"Heal House GR brief (Nov 3 2026): ~$151M Building Ontario Fund ask over ~2,000 homes = $75.5K/home",
 "suites":"ASSUMPTION — 80 wellness-stay suites, ADR $185, 72% occ., 30% NOI margin, funded by Sunray cash",
 "condo":"ASSUMPTION — Tower C 23 storeys, ~180,000 sf (Colliers pre-consultation, Jun 2025), not approved; $1,050/sf base; Arterial income value ~$712/sf as downside",
 "stack":"Year-10 refinance capped at 85% LTV (Tower A) and 75% (Tower B). BCH split tranche modelled on Common Ground: 54.5% contribution vesting Yrs 1–10 vs affordable homes, 45.5% mezz payment-free to Yr 10; BCH mezz and Fund repaid by Year-10 refinance",
}
A=dict(rate=0.0425, amort=50, soft=0.15, aff_factor=0.80, tax=0.008397, mli_share=0.50, city_share=0.05,
       grant_share=0.545, refi_dscr=1.20, bof_pref=0.04, predev=4_000_000,
       price=31_000_000, legal=500_000, months=18, loan_rate=0.065, tax_ins_yr=350_000, unguar_ltv=0.65, appraisal=30_000_000)
r=A["rate"]/12; n=A["amort"]*12; CONST=12*r/(1-(1+r)**-n)
bal=lambda P,m: P*((1+r)**n-(1+r)**m)/((1+r)**n-1)

def land_all():
    return A["price"]+ltt(A["price"])+A["legal"]+A["price"]*A["loan_rate"]*A["months"]/12+A["tax_ins_yr"]*A["months"]/12

def stack(tdc, egi, opex, sponsor, bof, aff, cap, g_rev=0.03, g_opex=0.025, refi_ltv=0.95):
    mli=A["mli_share"]*tdc; city=A["city_share"]*tdc; bch=tdc-mli-city-bof-sponsor
    grant=A["grant_share"]*bch; mezz=bch-grant; ads=mli*CONST; noi=egi-opex
    cf=[]; to_sp=0
    for y in range(1,11):
        ny=egi*(1+g_rev)**(y-1)-opex*(1+g_opex)**(y-1); c=ny-ads; pref=min(max(c,0),A["bof_pref"]*bof)
        cf.append(c); to_sp+=c-pref
    noi11=egi*(1+g_rev)**10-opex*(1+g_opex)**10; val10=noi11/cap
    refi=min(noi11/A["refi_dscr"]/CONST, refi_ltv*val10); payoff=bal(mli,120)+mezz+bof; surplus=refi-payoff
    return dict(tdc=tdc,mli=mli,city=city,bch=bch,grant=grant,mezz=mezz,bof=bof,sponsor=sponsor,noi=noi,ads=ads,
        dscr=noi/ads,value=noi/cap,noi11=noi11,val10=val10,refi=refi,mli10=bal(mli,120),payoff=payoff,surplus=surplus,
        to_sp=to_sp,mult=(to_sp+max(surplus,0))/sponsor,grant_per_aff=grant/aff if aff else 0,equity10=val10-refi)

def tower_a():
    gfa=GFA*SHARE_A
    mix=[("1 Bed",222,560,1720,2338,55000),("2 Bed",261,760,1850,2963,70000),("3 Bed",72,960,1834,3500,75000)]
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
    mix=[("1 Bed",288,600,55000),("2 Bed",123,820,70000)]
    units=411; aff=0; gpi=0; dc=0
    for (lab,k,sf,d),rr in zip(mix,rent):
        a=round(k*0.20); aff+=a; gpi+=((k-a)*rr+a*rr*A["aff_factor"])*12; dc+=(k-a)*d
    egi=gpi*occ; opex=opex_ratio*egi
    land_b=land_all()*SHARE_B; land_res=land_b*(sen_gfa+pod)/gfa; land_suites=land_b-land_res
    hard=370*(sen_gfa+pod)+100*pod+40*sen_gfa+15000*units
    tdc=land_res+hard+dc+A["soft"]*hard+A["predev"]*SHARE_B
    bof=75_500*units
    s=stack(tdc,egi,opex,land_res+A["predev"]*SHARE_B,bof,aff,0.06,0.03,0.03,0.75)
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

def site():
    a=tower_a(); b=tower_b(); c=tower_c()
    la=land_all(); unguar=A["unguar_ltv"]*A["appraisal"]; guar=A["price"]-unguar
    acq_eq=la-A["price"]+A["predev"]
    hh_members_a=round(0.20*a["units"]); hh_mem_rev=hh_members_a*350*12
    hh_rev=b["hh_fee"]+b["days"]+hh_mem_rev; hh_e=b["hh_fee"]+b["hh_days"]+0.5*hh_mem_rev
    return dict(A=a,B=b,C=c,land_all=la,guar=guar,unguar=unguar,acq_eq=acq_eq,
        homes=a["units"]+b["units"]+c["units"],aff=a["aff"]+b["aff"],
        sponsor=a["sponsor"]+b["sponsor"], bof=b["bof"], bch=a["bch"]+b["bch"], city=a["city"]+b["city"],
        mli=a["mli"]+b["mli"], tdc_rent=a["tdc"]+b["tdc"], sunray=b["s_cost"], condo_eq=c["equity"],
        hh_members_a=hh_members_a, hh_rev=hh_rev, hh_e=hh_e)

if __name__=="__main__":
    s=site()
    for t in ("A","B"):
        x=s[t]; print(t,{k:round(v/1e6,2) if isinstance(v,float) and abs(v)>1e4 else (round(v,3) if isinstance(v,float) else v) for k,v in x.items() if k not in("mix","name")})
    print("C",{k:round(v/1e6,2) if isinstance(v,float) and abs(v)>1e4 else v for k,v in s["C"].items() if k not in("mix","name")})
    print({k:round(v/1e6,2) if isinstance(v,float) and abs(v)>1e4 else v for k,v in s.items() if k not in("A","B","C")})
    for p in (712,900,1050,1200): c=tower_c(p); print("condo",p,round(c["profit"]/1e6,1),round(c["margin"]*100,1))
    for kw in ({},dict(opex_ratio=0.65,occ=0.90)):
        b=tower_b(**kw); print("B",kw,round(b["noi"]/1e6,2),round(b["dscr"],2),round(b["surplus"]/1e6,1),round(b["mult"],1))
