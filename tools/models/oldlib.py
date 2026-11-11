import json, uuid, base64, io, math
from PIL import Image
FACES=['north','south','east','west','up','down']
def hsh(*a):
    h=2166136261
    for v in a:
        h^=int(v)&0xffffffff; h=(h*16777619)&0xffffffff
    return h
def sh(c,d): return tuple(max(0,min(255,v+d)) for v in c)
P=dict(
 wood=[(134,98,56),(116,84,48),(98,70,40),(76,54,31)],
 grey=[(156,156,150),(132,132,127),(108,108,105),(80,80,80)],
 copper=[(238,152,116),(222,130,98),(196,106,78),(158,80,60)],
 sail=[(242,242,238),(230,230,225),(208,208,203),(172,172,170)],
 tan=[(200,164,106),(174,138,84),(140,108,64)],
 dark=[(66,66,70),(46,46,50),(32,32,36)],
 chest=[(176,128,46),(154,108,35),(126,86,27),(52,36,12)],
 iron=[(96,104,118),(66,72,84),(52,57,68),(36,40,48)],
 brass=[(250,214,120),(228,184,92),(192,146,62),(140,100,40)],
 vault=[(104,114,132),(74,82,98),(56,62,76),(38,42,54)],
)
def plank(a,b,seed):
    p=P['wood']; row=b//4; r=b%4
    L=11+hsh(row,seed)%7; off=hsh(row,seed,3)%L; seg=(a+off)//L
    tone=(hsh(row,seg,seed)%5-2)*5           # per-board tone
    c=sh(p[1],tone)
    if r==0: c=sh(p[0],tone)
    if r==3: c=sh(p[3],tone//2)              # seam between rows
    elif (a+off)%L==0: c=sh(p[3],tone//2)    # board end joint
    elif hsh(a//3,b,seed)%9==0: c=sh(p[2],tone)   # grain streak
    elif hsh(a,b,seed,7)%23==0: c=sh(p[0],tone+6)
    kx=hsh(row,seg,seed,9)%L; 
    if hsh(row,seg,seed,11)%4==0 and r in(1,2) and abs(((a+off)%L)-kx)<=1 and kx>2: c=p[3] if r==1 else sh(p[2],-6)  # knot
    return c
def andes(x,y,seed):
    g=P['grey']; k=hsh(x,y,seed)%10
    return g[1] if k<6 else g[0] if k<8 else g[2]
def prop_mask(w,h,nb,w0,w1,curve,phase=0.0):
    cx,cy=(w-1)/2,(h-1)/2; R=min(cx,cy); M=[[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            dx,dy=x-cx,y-cy
            for i in range(nb):
                th=2*math.pi*i/nb+phase; u=dx*math.cos(th)+dy*math.sin(th); v=-dx*math.sin(th)+dy*math.cos(th)
                if u<0.08*R or u>R: continue
                t=u/R; vc=curve*R*t*t; hw=R*(w0+(w1-w0)*t**0.8); ht=R*w1
                d=v-vc
                if abs(d)>hw: continue
                if u>R-ht and (u-(R-ht))**2+d*d>ht*ht: continue
                M[y][x]=1 if d<-hw*0.25 else 3 if d>hw*0.45 else 2
    return M,cx,cy,R
PROPS=dict(prop2=(2,.035,.085,0.0),prop2b=(2,.035,.085,0.0,math.pi/2),prop3=(3,.07,.17,.12),prop4=(4,.09,.2,.16),pinwheel=(4,.05,.19,.3),pinwheelb=(4,.05,.19,.3,math.pi/4),fan4=(4,.09,.27,.42),fan4b=(4,.09,.27,.42,math.pi/4),blade2=(2,.07,.13,.05),blade2b=(2,.07,.13,.05,math.pi/2))
def paint(mat,w,h,face):
    im=Image.new('RGBA',(w,h)); px=im.load(); horiz=w>=h; seed=hsh(w,h,len(mat),ord(mat[0]))
    if mat in PROPS:
        M,cx,cy,R=prop_mask(w,h,*PROPS[mat]); s=P['sail']
        for y in range(h):
            for x in range(w):
                c=(0,0,0,0); m=M[y][x]
                if m:
                    c=s[0] if m==1 else s[1] if m==2 else s[2]
                    if any(not(0<=x+i<w and 0<=y+j<h) or not M[y+j][x+i] for i,j in((1,0),(-1,0),(0,1),(0,-1))): c=(74,74,80) if mat.startswith(('fan','blade')) else P['grey'][2]
                r=math.hypot(x-cx,y-cy); hr=max(1.6,0.085*R)
                if r<=hr: c=P['dark'][1]
                if r<=hr*0.5: c=P['grey'][0]
                px[x,y]=c if len(c)==4 else c+(255,)
        return im
    for y in range(h):
        for x in range(w):
            a,b=(x,y) if horiz else (y,x); L,W_=(w,h) if horiz else (h,w)
            e=min(x,y,w-1-x,h-1-y)
            if mat=='wood':
                c=plank(a,b,seed)
                if L>=10 and (a<2 or a>=L-2):
                    c=andes(x,y,seed)
                    if a in(1,L-2): c=P['grey'][3] if b==W_-1 else sh(c,10)
            elif mat=='casing':
                c=plank(x,y,seed)
                if e<2 or min(w,h)<=3:
                    c=andes(x,y,seed)
                    if e==0 and (y==h-1 or x==w-1): c=P['grey'][3]
                    if e==1 and (x in(1,w-2)) and (y in(1,h-2)): c=P['dark'][0]     # corner bolts
                elif e==2 and min(w,h)>7: c=P['wood'][3]
            elif mat=='engine':
                p=P['copper']
                if face=='south':
                    c=P['dark'][1]
                    if e>=2 and ((x+y)%3==0 or (x-y)%3==0): c=P['grey'][2]
                    if e<2: c=andes(x,y,seed)
                    if e==0 and (y==h-1 or x==w-1): c=P['grey'][3]
                else:
                    c=p[1] if hsh(x,y,seed)%7 else p[0]
                    if e==0: c=p[3]
                    elif e==2 and min(w,h)>=7: c=p[2] if (x==2 or y==2) else p[0]
            elif mat=='sail':
                s=P['sail']; c=s[0]
                k=hsh(x//2,y//2,seed)%9
                if k==0: c=s[1]
                if min(w,h)<=1: c=P['tan'][1]
                else:
                    n=max(1,round(L/16)); pl=L/n; pa=a-int(a//pl*pl+1e-6); pn=int(round(pl))
                    pe=min(pa,pn-1-pa,b,W_-1-b)
                    if pe==0: c=P['tan'][1] if hsh(a,b,seed)%5 else P['tan'][2]
                    elif pe==1: c=s[2] if (pa==1 or b==1) else s[1]
                    elif pe==2 and W_>=7 and pa in(3,4,pn-5,pn-4) and b in(2,W_-3): c=s[3]
                    if min(w,h)==2: c=P['tan'][1] if b==0 else P['tan'][2]
            elif mat=='rod':
                g=P['grey']; c=g[1]
                if b==0: c=g[0]
                if b==W_-1 and W_>1: c=g[3]
                if a%8==7: c=g[2]
            elif mat=='seat':
                c=(98,62,46)
                if y==0 or x==0: c=(118,78,58)
                if y==h-1 or x==w-1: c=(72,46,36)
            elif mat=='wheel':
                r=math.hypot(x-(w-1)/2,y-(h-1)/2); c=P['dark'][1]
                if face in('east','west'):
                    c=P['dark'][1] if r>1.2 else P['grey'][1]
                    if e==0 and (x in(0,w-1)) and (y in(0,h-1)): c=(0,0,0,0)
                elif a%2==0: c=P['dark'][2]
            elif mat=='cog':
                c=(0,0,0,0); cx,cy=(w-1)/2,(h-1)/2; dx,dy=x-cx,y-cy; r=math.hypot(dx,dy); ang=math.atan2(dy,dx)
                R=cx-1.2+(1.2 if math.cos(ang*8)>0.1 else 0)
                if r<=R:
                    c=P['wood'][1] if r>R-1.5 or r<cx*0.62 else (0,0,0,0)
                    if abs(dx)<0.8 or abs(dy)<0.8: c=P['wood'][2]
                    if r>cx-2.4 and c!=(0,0,0,0): c=P['wood'][0] if (x+y)%2 else P['wood'][2]
                    if r<=2.2: c=P['grey'][1]
            elif mat.startswith('chest'):
                p=P['chest']; c=p[1] if hsh(x//2,y,seed)%6 else p[0]
                if face in('up','down'):
                    if e==0: c=p[3]
                    elif e==1: c=p[0]
                    elif y%4==1: c=p[2]
                else:
                    if y in(0,4,5,h-1) or x in(0,w-1): c=p[3]
                    elif y in(1,6): c=p[0]
                    elif y in(3,h-2,9): c=p[2]
            elif mat in('iron','truss'):
                p=P['iron']; n=max(1,round(L/16)); pl=L/n; pa=a-int(a//pl*pl+1e-6); pn=int(round(pl)); pe=min(pa,pn-1-pa,b,W_-1-b)
                c=p[1] if hsh(x//2,y//2,seed)%7 else p[2]
                if min(w,h)<=2: c=p[1] if b==0 else p[3]
                else:
                    if pe==0: c=p[3]
                    elif pe==1 and (pa==1 or b==1): c=p[0]
                    elif pe==2 and W_>=8 and pa in(2,pn-3) and b in(2,W_-3): c=(150,160,172)
                    if mat=='truss' and W_>=4 and pe>=1:
                        k=pa%(2*(W_-2)) if W_>2 else 0; d1=abs(k-(b-1)); d2=abs((2*(W_-2)-k)-(b-1))
                        c=p[0] if min(d1,d2)==0 else p[3] if min(d1,d2)==1 else p[2]
            elif mat in('brass','engine_b'):
                p=P['brass']
                if mat=='engine_b' and face=='south':
                    c=P['dark'][1]
                    if e>=2 and (y%3==0): c=P['dark'][0]
                    r=math.hypot(x-(w-1)/2,y-(h-1)/2)
                    if e>=2 and abs(r-min(w,h)*0.28)<0.8: c=p[2]
                    if r<1.5: c=p[1]
                    if e<2: c=p[1] if e==1 else p[3]
                else:
                    c=p[1] if hsh(x,y,seed)%6 else p[0]
                    if min(w,h)<=2: c=p[1] if b==0 else p[3]
                    else:
                        if e==0: c=p[3]
                        elif e==1: c=p[0] if (x==1 or y==1) else p[2]
                        elif min(w,h)>=8 and e==3: c=p[2]
                        elif min(w,h)>=8 and e==4 and (x==4 or y==4): c=p[0]
                        if min(w,h)>=6 and (x in(1,w-2)) and (y in(1,h-2)): c=p[3]
                        if mat=='engine_b' and face in('east','west') and min(w,h)>=8 and e>=3 and y%2==0: c=P['dark'][0]
            elif mat=='vault':
                p=P['vault']
                if face in('north','south'):
                    c=p[1]
                    if e==0: c=p[3]
                    elif e in(1,4): c=p[0]
                    elif e==2: c=p[2]
                    r=math.hypot(x-(w-1)/2,y-(h-1)/2)
                    if r<3.2: c=P['brass'][2]
                    if r<2.0: c=P['brass'][0]
                else:
                    c=p[1]
                    if b==0: c=p[0]
                    if b==W_-1: c=p[3]
                    k=a%12
                    if k in(0,1): c=p[0] if k==0 else p[3]
                    if k==6 and b in(2,W_-3): c=(150,160,176)
                    if W_>=10 and b in(W_//2,): c=p[2]
            elif mat=='gun':
                d=P['dark']; c=d[1]
                if b==0: c=d[0]
                if b==W_-1 and W_>1: c=d[2]
                if a%5==4: c=P['grey'][2]
                if a>=L-2: c=d[2]
            elif mat=='sailw':
                s2=P['sail']; c=s2[0]
                if hsh(x//2,y//2,seed)%9==0: c=s2[1]
                if min(w,h)<=2: c=P['iron'][1] if b==0 else P['iron'][3]
                else:
                    n=max(1,round(L/16)); pl=L/n; pa=a-int(a//pl*pl+1e-6); pn=int(round(pl)); pe=min(pa,pn-1-pa,b,W_-1-b)
                    if pe==0: c=P['iron'][1] if hsh(a,b,seed)%4 else P['iron'][0]
                    elif pe==1: c=s2[2]
                    elif pe==2 and W_>=7 and pa in(3,4,pn-5,pn-4) and b in(2,W_-3): c=P['brass'][2]
                    eb=min(b,W_-1-b)
                    if W_>=12 and eb==4 and pe>1: c=(168,60,52)       # red tier stripe
            elif mat=='hullw':      # andesite-framed dark spruce boards (warship pack hull)
                n=max(1,round(L/16)); pl=L/n; pa=a-int(a//pl*pl+1e-6); pn=int(round(pl)); pe=min(pa,pn-1-pa,b,W_-1-b)
                dw=[(104,74,44),(90,63,37),(76,53,31),(60,42,25)]
                if min(w,h)<=3:
                    c=(126,126,122) if b==0 else (104,104,101) if b<W_-1 else (80,80,78)
                elif pe<2:
                    c=(132,132,128) if pe==1 else (98,98,96)
                    if pe==1 and (pa in(1,pn-2)) and (b in(1,W_-2)): c=(70,70,70)
                    if pe==0 and (b==W_-1 or pa==pn-1): c=(78,78,77)
                else:
                    col=(pa if horiz else pa)//3; r=pa%3      # vertical boards across the panel length
                    c=dw[1] if r==1 else dw[0] if r==0 else dw[3]
                    if r!=2 and hsh(col,b//5,seed)%4==0: c=dw[2]
                    if pe==2: c=dw[3]
            elif mat=='panel':      # brass-framed dark glossy tiles
                n=max(1,round(L/12)); pl=L/n; pa=a-int(a//pl*pl+1e-6); pn=int(round(pl)); pe=min(pa,pn-1-pa,b,W_-1-b); eo=min(a,L-1-a,b,W_-1-b)
                br=P['brass']
                if min(w,h)<=2: c=br[1] if b==0 else br[3]
                elif eo==0: c=br[1] if (b==0 or a==0) else br[3]
                elif eo==1 and min(w,h)>=6: c=br[0] if (b==1 or a==1) else br[2]
                else:
                    t=b/max(1,W_-1); g=int(22-18*t)
                    c=(34+g,38+g,46+g)
                    if pe<=(1 if min(w,h)<6 else 2) and eo>1: c=(24,26,32)
                    if pe==(2 if min(w,h)<6 else 3) and b<W_/2: c=(74,80,92)
                    if min(w,h)>=8 and pa==pn//2 and b==W_//2: c=(120,128,140)
            elif mat=='tank':       # copper fluid-tank cylinder, axis along z
                cp=[(250,176,132),(232,142,104),(206,112,80),(170,86,62),(128,62,48)]
                if face=='south':
                    c=(34,34,38); cx,cy=(w-1)/2,(h-1)/2; dx,dy=x-cx,y-cy; r=math.hypot(dx,dy); ang=math.atan2(dy,dx)
                    if e>=2 and math.cos(ang*8)>0.35 and r>1.5: c=(96,96,100)
                    if r<=1.6: c=(150,150,152)
                    if e<2: c=cp[1] if e==1 else cp[4]
                    if e==1 and (x in(1,w-2)) and (y in(1,h-2)): c=cp[0]
                elif face=='north':
                    c=cp[1]
                    if e==0: c=cp[4]
                    elif e==1: c=cp[0] if (x==1 or y==1) else cp[3]
                    elif min(w,h)>=8 and e==3: c=cp[3] if (x==3 or y==3) else cp[0]
                else:
                    al,ac,AL,AC=(x,y,w,h) if face in('east','west') else (y,x,h,w)
                    t=ac/max(1,AC-1); k=abs(t-0.32)
                    c=cp[0] if k<0.1 else cp[1] if k<0.28 else cp[2] if k<0.5 else cp[3]
                    if ac in(0,AC-1): c=cp[4]
                    m8=al%8
                    if m8==0: c=cp[4] if ac in(0,AC-1) else cp[3]
                    if m8==1 and 0<ac<AC-1: c=cp[0] if k<0.28 else cp[1]
                    if al in(0,AL-1): c=cp[4]
            elif mat=='sailc':      # clean warship sail
                n=max(1,round(L/20)); pl=L/n; pa=a-int(a//pl*pl+1e-6); pn=int(round(pl))
                m2=max(1,round(W_/20)); ql=W_/m2; qb=b-int(b//ql*ql+1e-6); qn=int(round(ql))
                pe=min(pa,pn-1-pa,qb,qn-1-qb); c=(224,224,218)
                if min(w,h)<=2: c=(190,190,186) if b==0 else (150,150,148)
                else:
                    if pe==0: c=(196,196,192)
                    elif pe==1: c=(238,238,234)
                    elif pe==2: c=(214,214,208)
                    if pe==0 and min(qb,qn-1-qb)>=4 and (qb in(5,6,qn-7,qn-6)) and W_>=14: c=(132,128,120)
                    if min(a,L-1-a,b,W_-1-b)==0: c=(168,168,164)
            elif mat=='girder':
                c=(78,80,88)
                if b==0: c=(112,114,122)
                elif b==W_-1: c=(48,50,56)
                elif W_>=4:
                    k=(a+b)%6
                    if k==0: c=(100,102,110)
                    elif k==1: c=(58,60,66)
                if a%16==0: c=(48,50,56)
            elif mat=='brassrod':
                br=P['brass']; c=br[1]
                if b==0: c=br[0]
                if b==W_-1 and W_>1: c=br[3]
                if a%6==5: c=br[2]
            elif mat=='window':
                c=(186,216,232)
                if (x-y)%7==0 or (x-y)%7==1 and e>1: c=(222,238,246)
                if e==0 or min(w,h)<=2: c=andes(x,y,seed)
                elif e==1: c=(150,186,206)
            elif mat=='latch':
                c=(198,198,198)
                if x==0 or y==0: c=(232,232,232)
                if y==h-1 or x==w-1: c=(110,110,112)
            else: c=(255,0,255)
            px[x,y]=c if len(c)==4 else c+(255,)
    return im

class Model:
    def __init__(s,name,TW=128): s.name=name; s.C=[]; s.TW=TW; s.gorig={}
    def cube(s,name,f,t,mat,group='body',rot=None,origin=None):
        s.C.append(dict(name=name,f=list(map(float,f)),t=list(map(float,t)),mat=mat,group=group,rot=rot,origin=origin))
    def mir(s,name,f,t,mat,group='body',g2=None):
        s.cube(name,f,t,mat,group); s.cube(name,[-t[0],f[1],f[2]],[-f[0],t[1],t[2]],mat,g2 or group)
    def rcube(s,name,f,t,mat,rot,origin,group='body'): s.cube(name,f,t,mat,group,rot=list(rot),origin=list(origin))
    def rmir(s,name,f,t,mat,rot,origin,group='body'):
        s.rcube(name,f,t,mat,rot,origin,group)
        s.rcube(name,[-t[0],f[1],f[2]],[-f[0],t[1],t[2]],mat,[rot[0],-rot[1],-rot[2]],[-origin[0],origin[1],origin[2]],group)
    def chest(s,x0,y0,z0,front):   # 14^3 vanilla size, front in 'e','w'
        s.cube('chest',[x0,y0,z0],[x0+14,y0+14,z0+14],'chest','cargo')
        if front=='e': s.cube('latch',[x0+14,y0+7,z0+6],[x0+15,y0+11,z0+8],'latch','cargo')
        if front=='w': s.cube('latch',[x0-1,y0+7,z0+6],[x0,y0+11,z0+8],'latch','cargo')
        if front=='n': s.cube('latch',[x0+6,y0+7,z0-1],[x0+8,y0+11,z0],'latch','cargo')
        if front=='s': s.cube('latch',[x0+6,y0+7,z0+14],[x0+8,y0+11,z0+15],'latch','cargo')
    def build(s):
        C=s.C; TW=s.TW
        def fsize(c,f):
            dx,dy,dz=[c['t'][i]-c['f'][i] for i in range(3)]
            return {'north':(dx,dy),'south':(dx,dy),'east':(dz,dy),'west':(dz,dy),'up':(dx,dz),'down':(dx,dz)}[f]
        rects=[]; uniq={}
        for ci,c in enumerate(C):
            c['uv']={}
            for f in FACES:
                w,h=fsize(c,f)
                if w<=0 or h<=0: continue
                W,H=max(1,math.ceil(w)),max(1,math.ceil(h))
                fk=f if c['mat'] in('engine','wheel','engine_b','vault','tank') else ('ud' if f in('up','down') else 's')
                key=(c['mat'],W,H,fk); rects.append((key,ci,f)); uniq[key]=(W,H)
        def pack(TH):
            pos={}; x=y=rowh=0
            for key,(W,H) in sorted(uniq.items(),key=lambda kv:(-kv[1][1],-kv[1][0])):
                if x+W>TW: x=0; y+=rowh+1; rowh=0
                if y+H>TH: return None
                pos[key]=(x,y); x+=W+1; rowh=max(rowh,H)
            return pos
        TH=64
        while not (pos:=pack(TH)): TH*=2
        tex=Image.new('RGBA',(TW,TH),(0,0,0,0))
        for key,(x,y) in pos.items():
            W,H=uniq[key]; fk=key[3]; tex.paste(paint(key[0],W,H,'up' if fk=='ud' else 'north' if fk=='s' else fk),(x,y))
        for key,ci,f in rects:
            x,y=pos[key]; W,H=uniq[key]; C[ci]['uv'][f]=[x,y,x+W,y+H]
            c=C[ci]; d=[c['t'][i]-c['f'][i] for i in range(3)]
            if d[1]==0 and f=='down': c['uv'][f]=[x,y+H,x+W,y]
            if d[2]==0 and f=='north': c['uv'][f]=[x+W,y,x,y+H]
            if d[0]==0 and f=='west': c['uv'][f]=[x+W,y,x,y+H]
        tex.save(s.name+'.png')
        buf=io.BytesIO(); tex.save(buf,'PNG'); src='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
        gdef=getattr(s,'gdef',{})
        def grot(g):
            while g:
                d=gdef.get(g,{})
                if d.get('rotation'): return d['rotation'], (d.get('origin') or s.gorig.get(g,[0,0,0]))
                g=d.get('parent')
            return None
        els=[]; groups={}; nodes={}; roots=[]
        def node(g):
            if g in nodes: return nodes[g]
            d=gdef.get(g,{})
            n=dict(name=g,origin=d.get('origin') or s.gorig.get(g,[0,0,0]),color=0,uuid=str(uuid.uuid4()),export=True,mirror_uv=False,isOpen=False,locked=False,visibility=True,autouv=0,children=[])
            if d.get('rotation'): n['rotation']=d['rotation']
            nodes[g]=n
            p=d.get('parent')
            if p: node(p)['children'].append(n)
            else: roots.append(n)
            return n
        scene=[]
        for c in C:
            u=str(uuid.uuid4())
            faces={f:({'uv':c['uv'][f],'texture':0} if f in c['uv'] else {'uv':[0,0,0,0],'texture':None}) for f in FACES}
            org=c['origin'] or [(c['f'][i]+c['t'][i])/2 for i in range(3)]
            e=dict(name=c['name'],box_uv=False,rescale=False,locked=False,render_order='default',allow_mirror_modeling=True,**{'from':c['f'],'to':c['t']},autouv=0,color=0,origin=org,faces=faces,type='cube',uuid=u)
            if c['rot']: e['rotation']=c['rot']
            els.append(e); groups.setdefault(c['group'],[]).append(u); node(c['group'])['children'].append(u)
            sc=dict(c); gr=grot(c['group'])
            if not c['rot'] and gr: sc['rot'],sc['origin']=gr
            scene.append(sc)
        anims={}; pi=0
        for g in sorted(groups):
            if not g.startswith('propell'): continue
            c0=[c for c in C if c['group']==g and any(c['t'][i]==c['f'][i] for i in range(3)) and c['mat']!='cog']
            if not c0: continue
            ax='y' if c0[0]['t'][1]==c0[0]['f'][1] else 'z' if c0[0]['t'][2]==c0[0]['f'][2] else 'x'
            sp=(100 if ax=='y' else 150)*(1 if pi%2==0 else -1); pi+=1
            dp={k:'0' for k in 'xyz'}; dp[ax]='variable.engine_rotation * %d'%sp
            anims[nodes[g]['uuid']]=dict(name=g,type='bone',keyframes=[dict(channel='rotation',data_points=[dp],uuid=str(uuid.uuid4()),time=0,color=-1,interpolation='linear',bezier_linked=True,bezier_left_time=[-0.1]*3,bezier_left_value=[0]*3,bezier_right_time=[0.1]*3,bezier_right_value=[0]*3)])
        animations=[dict(uuid=str(uuid.uuid4()),name='animation',loop='loop',override=False,length=0,snapping=24,selected=False,anim_time_update='',blend_weight='',start_delay='',loop_delay='',animators=anims)] if anims else []
        bb=dict(meta=dict(format_version='4.9',model_format='free',box_uv=False),name=s.name,model_identifier='',visible_box=[1,1,0],variable_placeholders='',variable_placeholder_buttons=[],timeline_setups=[],unhandled_root_fields={},
                resolution=dict(width=TW,height=TH),elements=els,outliner=roots,
                textures=[dict(path='',name=s.name+'.png',folder='',namespace='',id='0',width=TW,height=TH,uv_width=TW,uv_height=TH,particle=False,layers_enabled=False,sync_to_project='',render_mode='default',render_sides='auto',frame_time=1,frame_order_type='loop',frame_order='',frame_interpolate=False,visible=True,internal=True,saved=True,uuid=str(uuid.uuid4()),source=src)],animations=animations)
        json.dump(bb,open(s.name+'.bbmodel','w'))
        json.dump(dict(cubes=scene,tw=TW,th=TH,tex=src),open(s.name+'.scene.json','w'))
        print(s.name,'cubes',len(C),'tex',TW,TH,'anim',len(anims))
