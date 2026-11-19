from pathlib import Path
import numpy as np
from PIL import Image
import json,sys,csv,gzip
root=Path('/root/flux2-bowl-interventions-20261119')
def traits(path):
 im=np.asarray(Image.open(path).convert('RGB')).astype('float32')
 R,G,B=im[...,0],im[...,1],im[...,2]
 blue=(B>1.17*G)&(B>1.26*R)&(B-R>15)
 pink=(R>1.2*G)&(R>1.2*B)&(R-G>27)
 green=(G>1.06*R)&(G>B*1.01)&(G-R>6)
 ys,xs=np.where(blue)
 if len(xs)<300: return dict(pink=0, green=0, side=0, score=0)
 top,bottom=np.percentile(ys,[1,99]);left,right=np.percentile(xs,[1,99])
 inside=np.zeros_like(blue)
 for y in range(int(top+.30*(bottom-top)),int(top+.68*(bottom-top))+1):
    x=np.flatnonzero(blue[y])
    if x.size<6: continue
    low,high=np.percentile(x,[2,98])
    inside[y,int(low+.11*(high-low)):int(high-.11*(high-low))+1]=True
 p=int((pink&inside).sum());g=int((green&inside).sum())
 # Side marker is positive when the pink object lies to the right of the green object.
 side=float(np.where(pink)[1].mean()-np.where(green)[1].mean()) if pink.any() and green.any() else 0
 return dict(pink=p,green=g,side=round(side,1),score=round((p-g)/max(1,inside.sum()),4))
def write_scores():
 scores={f.stem:traits(f) for f in root.glob('*__s*.png')}
 (root/'measurements.json').write_text(json.dumps(scores,indent=2))
 return scores
if __name__=='__main__':
 scores=write_scores()
 if len(sys.argv)>1 and sys.argv[1]=='donor':
    ranks=[]
    readout=Path('/root/flux-cross-20261119/blind-visual-readout.jsonl')
    decisions={}
    if readout.exists():
        for line in readout.read_text().splitlines():
            try:
                record=json.loads(line)
                decisions[record['key']]=record['codes']
            except ValueError:pass
    for k in ('g1','g2','g4'):
        samples=[scores.get(f'{k}__s{s}',{}) for s in (2,0,1)]
        if all(x for x in samples): ranks.append((int(samples[0]['side']>0 and samples[0]['pink']>70 and samples[0]['score']>0), int(decisions.get(f'bowl/{k}__s2')==['B','A']),sum(x['side']>0 and x['score']>0 and x['pink']>70 for x in samples),samples[0]['score'],k))
 print(max(ranks)[-1] if len(sys.argv)>1 and sys.argv[1]=='donor' and ranks else json.dumps(scores))
