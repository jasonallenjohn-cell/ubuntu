"""Zonix Tower B — Heal House Seniors Living Program (no Common Ground). Single source of truth."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import ltt
SRC = {
 "gfa": "Tower B = 40-storey tower; GFA allocated 40/84 of the 858,648 sf approved scheme (Colliers, Jun 2026) — unverified vs stamped set",
 "constr": "Arterial hard cost, Markham 40–60 storeys, $330–410/sf midpoint (Nov 4 2026)",
 "rents": "Arterial scenario comps, Yonge/Steeles leasing: 1BR $2,338 (5), 2BR $2,963 (4) (Nov 4 2026)",
 "cmhc": "Arterial / CMHC Markham zone avg rents 1BR $1,720, 2BR $1,850 (Nov 4 2026)",
 "tax": "Arterial Markham multi-res rate 0.8397% (2025)",
 "dc": "ESTIMATE — no Arterial Markham/York DC data; affordable units assumed DC-exempt (Ontario DCA); needs municipal quote",
 "bof": "Heal House GR brief (Nov 3 2026): ~$151M Building Ontario Fund ask across ~2,000 homes = $75.5K/home",
 "aff": "Program: ~400 of 2,000 homes (20%) affordable for 40 years, here at 80% of CMHC average rent",
 "mli": "ASSUMPTION — CMHC MLI Select, 100 points, 4.25%, 50-yr amortization, sized to 1.20x coverage (min 1.10x), ≤95% of value",
 "hh": "Heal House $350/mo, 85% seniors uptake (sponsor assumption); 60% gross margin per HealHouse_15Year_BusinessPlan_Valuation (Jun 2026)",
 "suites": "ASSUMPTION — 80 family & recovery suites funded outside the housing stack (e.g. Sunray cash); ADR $185, 72% occ., 30% NOI margin",
}
A=dict(gfa_total=858648, share=40/84, psf=370, soft=0.15, cap=0.0425, rate=0.0425, amort=50,
       vac=0.03, aff=0.20, aff_factor=0.80, tax=0.008397, dscr_target=1.20, max_ltv=0.95,
       bof_per_home=75_500, price=31_000_000, legal=500_000, months=18, loan_rate=0.065,
       tax_ins_yr=350_000, predev=4_000_000)
PODIUM=dict(sf=40000, ti=100, opex_psf=5)
SUITES=dict(keys=80, sf=48000, adr=185, occ=0.72, other=0.10, margin=0.30, ffe=40000, dc_psf=25, cap=0.075)
MIX=[("1 Bed",288,600,1720,2338,55000),("2 Bed",123,820,1850,2963,70000)]
HH=dict(fee=350, uptake=0.85, cogs=0.40, oh=0.10, day_capture=0.25, day_price=150)

def run():
    a=A; gfa=round(a["gfa_total"]*a["share"]); sen_gfa=gfa-PODIUM["sf"]-SUITES["sf"]
    units=sum(m[1] for m in MIX); nra=sum(m[1]*m[2] for m in MIX)
    gpi=0; aff=0; dc=0
    for _,n,sf,mmr,mkt,d in MIX:
        k=round(n*a["aff"]); aff+=k; gpi+=((n-k)*mkt+k*round(mmr*a["aff_factor"]))*12; dc+=(n-k)*d
    egi=gpi*(1-a["vac"])
    op=units*(1200+900+450+500+300+1200)+0.04*egi+PODIUM["sf"]*PODIUM["opex_psf"]
    noi=(egi-op)/(1+a["tax"]/a["cap"]); tax=egi-op-noi; value=noi/a["cap"]
    # land: whole-site cost allocated to Tower B by GFA share
    land_all=a["price"]+ltt(a["price"])+a["legal"]+a["price"]*a["loan_rate"]*a["months"]/12+a["tax_ins_yr"]*a["months"]/12
    land_B=land_all*a["share"]
    res_share=(sen_gfa+PODIUM["sf"])/gfa; land_res=land_B*res_share; land_suites=land_B-land_res
    hard=a["psf"]*(sen_gfa+PODIUM["sf"])+PODIUM["sf"]*PODIUM["ti"]
    soft=a["soft"]*hard; tdc=land_res+hard+dc+soft+a["predev"]
    r=a["rate"]/12; n=a["amort"]*12; const=12*r/(1-(1+r)**-n)
    mli=min(noi/a["dscr_target"]/const, a["max_ltv"]*value); ads=mli*const
    bof=a["bof_per_home"]*units
    gap=tdc-mli-bof
    # suites (outside stack)
    s=SUITES; s_hard=a["psf"]*s["sf"]+s["keys"]*s["ffe"]; s_cost=land_suites+s_hard*(1+a["soft"])+s["sf"]*s["dc_psf"]
    s_rev=s["keys"]*s["adr"]*365*s["occ"]*(1+s["other"]); s_noi=s_rev*s["margin"]
    # Heal House
    mem=round(HH["uptake"]*units); m_rev=mem*HH["fee"]*12
    nights=s["keys"]*365*s["occ"]; d_rev=nights*HH["day_capture"]*HH["day_price"]
    hh_rev=m_rev+d_rev; hh_e=hh_rev*(1-HH["cogs"]-HH["oh"])
    return dict(SRC=SRC,A=a,gfa=gfa,sen_gfa=sen_gfa,units=units,nra=nra,aff=aff,gpi=gpi,egi=egi,opex=op+tax,tax=tax,
        noi=noi,value=value,land_all=land_all,land_B=land_B,land_res=land_res,land_suites=land_suites,hard=hard,dc=dc,
        soft=soft,tdc=tdc,mli=mli,ads=ads,dscr=noi/ads,ltv=mli/value,ltc=mli/tdc,bof=bof,gap=gap,
        s_cost=s_cost,s_rev=s_rev,s_noi=s_noi,mem=mem,m_rev=m_rev,d_rev=d_rev,hh_rev=hh_rev,hh_e=hh_e,
        cost_per=tdc/units, value_gap=value-tdc)
if __name__=="__main__":
    d=run()
    for k,v in d.items():
        if isinstance(v,(int,float)): print(f"{k:12s} {v:,.2f}")
