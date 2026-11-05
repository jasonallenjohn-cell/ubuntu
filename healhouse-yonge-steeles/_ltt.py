def ltt(p):
    """Ontario land transfer tax, non-single-family property."""
    b=[(55000,.005),(250000,.01),(400000,.015),(float('inf'),.02)]; t=0; lo=0
    for hi,r in b:
        if p>lo: t+=(min(p,hi)-lo)*r
        lo=hi
    return round(t)
