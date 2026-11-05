"""Zonix x Heal House — integrated Common Ground model (single source of truth).
All figures on the one-pager are imported from run(). Sources and dates in SRC."""
import json

SRC = {
 "gfa": "Approved two-tower scheme, 858,648 sf marketed GFA (Colliers brochure, Jun 2026) — unverified vs stamped set",
 "constr": "Arterial construction cost, Markham condos 40–60 storeys, $330–410/sf midpoint (Nov 4 2026)",
 "rents": "Arterial scenario comps, Yonge/Steeles leasing: 1BR $2,338 (5), 2BR $2,963 (4); 3BR $3,500 adj. from 1 comp (Nov 4 2026)",
 "cmhc": "Arterial / CMHC Markham zone avg rents 1BR $1,720 · 2BR $1,850 · 3BR $1,834 (Nov 4 2026)",
 "tax": "Arterial Markham multi-res rate 0.8397% (2025)",
 "dc": "ESTIMATE — Arterial has no Markham/York DC data; needs municipal quote",
 "land": "Working value $30M (desktop opinion, Nov 4 2026); bid $31M",
 "hotel": "ASSUMPTION — 80 short-stay keys, ADR $185, 72% occ., 30% NOI margin",
 "podium": "ASSUMPTION — 40,000 sf Heal House clinic/wellness at $32/sf net",
 "stack": "Common Ground July 2026: MLI Select 50% / BCH 40% (54.5% contribution, 45.5% mezz) / City 5% / land equity 5%. Per instruction, assumes MLI Select + BCH fund commercial space",
}

A = dict(constr=370, soft=0.15, cap_res=0.0425, cap_com=0.06, cap_hot=0.075,
         rate=0.0425, amort=50, vac=0.03, aff_share=0.30, aff_factor=0.80,
         tax_rate=0.008397, growth=0.03, opex_g=0.025, com_g=0.02,
         grant_share=0.545, mezz_rate=0.045, gfa=858648)

TOWER_A = [  # label, beds, count, sqft, cmhc, market, dc
 ("1 Bed",1,284,560,1720,2338,55000),("2 Bed",2,334,760,1850,2963,70000),("3 Bed",3,92,960,1834,3500,75000)]
SENIORS = [("55+ 1 Bed",1,175,600,1720,2338,55000),("55+ 2 Bed",2,75,820,1850,2963,70000)]
PODIUM = dict(sf=40000, rent=32, vac=0.05, nonrec=0.03, ti=100, dc_psf=25)
HOTEL  = dict(keys=80, sf=48000, adr=185, occ=0.72, other=0.10, margin=0.30, ffe=40000, dc_psf=25)
SENIORS_GFA = 195000
ACQ = dict(price=31_000_000, appraisal=30_000_000, legal=500_000, months=18, loan_rate=0.065,
           tax_ins_yr=350_000, predev=4_000_000, unguar_ltv=0.65)

def ltt(p):  # Ontario LTT, non-single-family
    b=[(55000,.005),(250000,.01),(400000,.015),(float('inf'),.02)]; t=0; lo=0
    for hi,r in b:
        if p>lo: t+=(min(p,hi)-lo)*r
        lo=hi
    return round(t)

def res_block(mix, extra_opex=0):
    units=sum(u[2] for u in mix); nra=sum(u[2]*u[3] for u in mix)
    gpi=0; aff=0
    for _,_,n,_,mmr,mkt,_ in mix:
        a=round(n*A["aff_share"]); aff+=a
        gpi+=((n-a)*mkt + a*round(mmr*A["aff_factor"]))*12
    egi=gpi*(1-A["vac"])
    op_ex_tax=units*(1200+900+450+500+300+extra_opex)+0.04*egi
    # solve tax = rate * (NOI/cap)
    noi=(egi-op_ex_tax)/(1+A["tax_rate"]/A["cap_res"]); tax=egi-op_ex_tax-noi
    dc=sum(u[2]*u[6] for u in mix)
    return dict(units=units,nra=nra,aff=aff,gpi=gpi,egi=egi,opex=op_ex_tax+tax,tax=tax,noi=noi,dc=dc)

def run():
    ta=res_block(TOWER_A); sn=res_block(SENIORS, extra_opex=1200)
    ta_gfa=A["gfa"]-PODIUM["sf"]-HOTEL["sf"]-SENIORS_GFA
    p=PODIUM; p_noi=p["sf"]*p["rent"]*(1-p["vac"]-p["nonrec"])
    h=HOTEL; h_rev=h["keys"]*h["adr"]*365*h["occ"]*(1+h["other"]); h_noi=h_rev*h["margin"]
    noi=ta["noi"]+sn["noi"]+p_noi+h_noi
    value=(ta["noi"]+sn["noi"])/A["cap_res"]+p_noi/A["cap_com"]+h_noi/A["cap_hot"]
    hard=A["constr"]*A["gfa"]+p["sf"]*p["ti"]+h["keys"]*h["ffe"]
    dc=ta["dc"]+sn["dc"]+(p["sf"]+h["sf"])*p["dc_psf"]
    soft=A["soft"]*hard
    land=ACQ["appraisal"]; draw=0.60*land
    base=hard+dc+soft
    tdc=(base+draw)/0.95; land_eq=min(0.05*tdc, land-draw); tdc=base+draw+land_eq
    mli=0.50*tdc; bch=0.40*tdc; grant=A["grant_share"]*bch; mezz=bch-grant; city=tdc-mli-bch-land_eq
    r=A["rate"]/12; n=A["amort"]*12; pmt=mli*r/(1-(1+r)**-n); ads=pmt*12
    bal=lambda P,m: P*((1+r)**n-(1+r)**m)/((1+r)**n-1)
    buyout=land_eq+(mli-bal(mli,120)); sup=buyout*1.01; sup_ads=sup*r/(1-(1+r)**-n)*12
    # 20-yr
    res_egi=ta["egi"]+sn["egi"]; res_opex=ta["opex"]+sn["opex"]; com=p_noi+h_noi
    rows=[]; bal_m=mezz; lo=[]; cum_np=0
    for y in range(1,21):
        ny=res_egi*(1+A["growth"])**(y-1)-res_opex*(1+A["opex_g"])**(y-1)+com*(1+A["com_g"])**(y-1)
        if y<=10:
            cf=ny-ads; lo_share=0.6*cf; np_share=0.4*cf; sweep=0
        else:
            cf=ny-ads-sup_ads; due=bal_m*(1+A["mezz_rate"]); sweep=min(max(0.6*cf,0),due)
            bal_m=due-sweep; lo_share=0; np_share=cf-sweep
        cum_np+=np_share
        rows.append(dict(y=y,noi=ny,cf=cf,lo=lo_share,np=np_share,bch=sweep,mezz_bal=bal_m))
    dscr10=rows[10]["noi"]/(ads+sup_ads)
    lo_cf=sum(x["lo"] for x in rows)
    # acquisition & raise
    a=ACQ; l=ltt(a["price"]); carry=a["price"]*a["loan_rate"]*a["months"]/12+a["tax_ins_yr"]*a["months"]/12
    unguar=a["unguar_ltv"]*a["appraisal"]; guar_top=a["price"]-unguar
    eq_at_acq=l+a["legal"]+carry+a["predev"]
    land_gap=a["price"]-draw                         # land loan left after Day-1 draw
    peak=eq_at_acq+land_gap
    perm=peak-a["predev"]                            # pre-dev recovered from soft budget at close
    unrecognized=perm-land_eq
    cmhc_nw=0.25*mli; cmhc_liq=0.10*mli
    # investor IRR (t=0 acq, t=1.5 close, 3.5yr build, ops years end t=6..15, buyout t=15)
    flows={0:-eq_at_acq,1.5:-(land_gap)+a["predev"]}
    for i,x in enumerate(rows[:10]): flows[6+i]=flows.get(6+i,0)+x["lo"]
    flows[15]+=buyout
    def npv(rt): return sum(v/(1+rt)**t for t,v in flows.items())
    lo_,hi_=0.0,1.0
    for _ in range(100):
        mid=(lo_+hi_)/2; (lo_:=mid) if npv(mid)>0 else (hi_:=mid)
    irr=mid; back=lo_cf+buyout
    res_units=ta["units"]+sn["units"]; aff=ta["aff"]+sn["aff"]
    return dict(SRC=SRC,A=A,ta=ta,sn=sn,ta_gfa=ta_gfa,p_noi=p_noi,h_rev=h_rev,h_noi=h_noi,noi=noi,value=value,
      hard=hard,dc=dc,soft=soft,draw=draw,land_eq=land_eq,tdc=tdc,mli=mli,bch=bch,grant=grant,mezz=mezz,city=city,
      ads=ads,dscr=noi/ads,ltv=mli/value,buyout=buyout,dscr10=dscr10,lo_cf=lo_cf,rows=rows,mezz_resid=bal_m,
      ltt=l,carry=carry,unguar=unguar,guar_top=guar_top,eq_at_acq=eq_at_acq,land_gap=land_gap,peak=peak,perm=perm,
      unrecognized=unrecognized,cmhc_nw=cmhc_nw,cmhc_liq=cmhc_liq,irr=irr,back=back,mult=back/perm,
      res_units=res_units,aff=aff,grant_per_aff=grant/aff,np_cf=cum_np,cf1=rows[0]["cf"])

if __name__=="__main__":
    d=run()
    for k,v in d.items():
        if isinstance(v,(int,float)): print(f"{k:16s} {v:,.3f}")
    print("ta",{k:round(v) for k,v in d['ta'].items()}); print("sn",{k:round(v) for k,v in d['sn'].items()})
    for x in d["rows"]: print(x["y"], round(x["noi"]/1e6,2), round(x["cf"]/1e6,2), round(x["lo"]/1e6,2), round(x["bch"]/1e6,2), round(x["mezz_bal"]/1e6,2))
