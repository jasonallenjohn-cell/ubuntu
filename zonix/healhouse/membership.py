"""Heal House membership economics at Zonix — imports building figures from model.run()."""
import sys; sys.path.insert(0,'.')
from model import run, PODIUM
d=run(); ta,sn=d['ta'],d['sn']
FEE=350; COGS=0.40; LOCAL_OH=0.10; CAM_PSF=5      # COGS = 60% gross margin per HealHouse_15Year model (mature)
def pnl(members, rent):
    rev=members*FEE*12; cogs=COGS*rev; oh=LOCAL_OH*rev
    occ= PODIUM['sf']*PODIUM['rent'] if rent else PODIUM['sf']*CAM_PSF
    e=rev-cogs-oh-occ; return dict(members=members,rev=rev,cogs=cogs,oh=oh,occ=occ,ebitda=e,margin=e/rev)
cases={
 "85% of whole building": round(0.85*(ta['units']+sn['units'])),
 "85% seniors + 20% Tower A": round(0.85*sn['units'])+round(0.20*ta['units']),
 "85% seniors only": round(0.85*sn['units']),
}
for name,m in cases.items():
    for rent in (True,False):
        p=pnl(m,rent)
        print(f"{name:28s} rent={'mkt' if rent else 'amen'} members {m:4d} rev {p['rev']/1e6:5.2f} ebitda {p['ebitda']/1e6:5.2f} ({p['margin']*100:4.0f}%)  8x {8*p['ebitda']/1e6:5.1f} 12x {12*p['ebitda']/1e6:5.1f}  2.5xRev {2.5*p['rev']/1e6:5.1f} 5.5xRev {5.5*p['rev']/1e6:5.1f}")
# building impact if podium is amenity (no rent)
import model
ads=d['ads']; print("DSCR base",round(d['noi']/ads,2),"podium as amenity",round((d['noi']-d['p_noi'])/ads,2))
print("TI funded in stack",PODIUM['sf']*PODIUM['ti'])
# 2,000-unit seniors portfolio
m=round(0.85*2000); p=pnl(m,False)
print("2000 units: members",m,"rev",p['rev']/1e6,"ebitda (amenity, 1 podium per 250)", None)
sites=2000/250; rev=m*FEE*12; ebitda=rev*(1-COGS-LOCAL_OH)-sites*PODIUM['sf']*CAM_PSF
print("sites",sites,"rev",rev/1e6,"ebitda",ebitda/1e6,"8-12x",8*ebitda/1e6,12*ebitda/1e6,"5.5-6.5x rev",5.5*rev/1e6,6.5*rev/1e6)
noi_suite=sn['noi']/sn['units']; print("seniors NOI/suite",noi_suite,"2000-suite NOI",2000*noi_suite/1e6,"value @4.25%",2000*noi_suite/0.0425/1e6)
print("affordable 1BR rent",round(1720*.8),"2BR",round(1850*.8), "fee share", 350/round(1720*.8))
