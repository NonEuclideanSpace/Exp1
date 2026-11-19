"""Targeted first-step experiments for the FLUX.2 bowl task, head indices are zero-based."""
from pathlib import Path
import argparse, json, math, time, shutil
import numpy as np
from PIL import Image
import torch
from safetensors.torch import load_file
from diffusers import Flux2KleinKVPipeline
from diffusers.models.transformers import transformer_flux2 as tr

root=Path('/root/flux2-binding-round2-20261119/results')
model=Path('/root/autodl-tmp/models/black-forest-labs/FLUX.2-klein-9b-kv')
dest=Path('/root/flux2-bowl-interventions-20261119')
dest.mkdir(exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--donor',type=str,default=None)
parser.add_argument('--refine',action='store_true')
args=parser.parse_args()
pipe=Flux2KleinKVPipeline.from_pretrained(str(model),torch_dtype=torch.bfloat16,local_files_only=True).to('cuda')
pipe.set_progress_bar_config(disable=True)
torch.backends.cuda.matmul.allow_tf32=False
blocks=list(pipe.transformer.transformer_blocks)+list(pipe.transformer.single_transformer_blocks)
dispatch=tr.dispatch_attention_fn
settings=dict(seed=2,case='N04',op='none',layers=set(),steps={0},plan={},capture=False)
step=-1
layer=-1
donor_att={}
donor_ff={}
rows=[]
started=time.monotonic()
description={
'g1':'Close studio photograph of two matte ceramic figurines and one shallow cobalt-blue bowl. On the LEFT a jade-green cat sits upright behind its side of the bowl, both paws resting on the upper rim. On the RIGHT a coral-pink rabbit reaches a long pink foreleg down INTO the bowl; its pink paw is pressed flat on the bottom at the center of the bowl. The blue interior is open to view around the pink paw. Slight overhead angle. Warm ivory studio background.',
'g2':'Viewed slightly from above, a single coral-pink rabbit paw lies flat in the middle of the inside bottom of a shallow cobalt-blue bowl. The pink foreleg extends all the way into the bowl from the coral-pink ceramic rabbit seated at its right. A jade-green ceramic cat sits on the left with both short front paws touching only the upper edge of the bowl. Full view of both figures and the bowl. Matte ceramic glaze and soft warm ivory studio lighting.',
'g3':'One shallow cobalt-blue bowl sits between a coral-pink ceramic rabbit and a jade-green ceramic cat. The rabbit presses one front paw flat against the inside bottom of the bowl. The cat touches the top rim of the same bowl with one front paw. Seen slightly from above so both contact points are visible. Matte ceramic glaze, warm ivory backdrop, soft studio light.',
'g4':'The coral-pink ceramic rabbit has its front paw planted in the center of a shallow cobalt-blue bowl, its paw covers the base inside the dish. The jade-green ceramic cat grips the left lip of the dish. The rabbit is on the right. Photograph from above, showing a single long pink foreleg inside the blue dish and green toes on its rim. Matte ceramic glaze, warm ivory backdrop, soft studio light.'}
emb={i:load_file(str(root/i/'text_condition.safetensors'))['prompt_embeds'].to('cuda') for i in ('N03','N04')}
meta={i:json.loads((root/i/'tokens.json').read_text()) for i in ('N03','N04')}
ids=load_file(str(root/'N04/seed-2/input.safetensors'))['img_ids'][0].to('cuda')
left=ids[:,2] < 16
ntext=512
focus={2:[17],3:[10],4:[22],5:[27]}
other={2:[18],3:[11],4:[23],5:[28]}
def begin(*args,**kw):
    global step,layer
    step+=1
    layer=-1
def probabilities(q,k,hh):
    h=torch.as_tensor(hh,device=q.device)
    qi=q[0,ntext:].index_select(1,h).permute(1,0,2).float()
    ki=k[0].index_select(1,h).permute(1,2,0).float()
    return torch.matmul(qi,ki).mul_(1/math.sqrt(q.shape[-1])).softmax(dim=-1)
def routed(q,k,v,*a,**kw):
    global layer
    layer+=1
    out=dispatch(q,k,v,*a,**kw)
    op=settings['op']
    if step not in settings['steps'] or layer not in settings['layers']: return out
    if op=='observe':
        ix=[g['indices'] for g in meta[settings['case']]['groups']]
        for start in range(0,32,8):
            hh=list(range(start,start+8)); p=probabilities(q,k,hh)
            for ti,tokens in enumerate(ix):
                w=p[...,tokens].sum(-1)
                left_mass=w[:,left].sum(1).cpu().tolist()
                right_mass=w[:,~left].sum(1).cpu().tolist()
                for h,l,r in zip(hh,left_mass,right_mass):
                    rows.append((settings['case'],settings['seed'],step,layer,h,ti,l,r))
        return out
    if op=='cache':
        donor_att[step,layer]=out[0,ntext:].detach().clone()
        return out
    heads=settings['plan'].get(layer,list(range(32)))
    if op=='image_ff' or (op=='mix' and layer not in settings.get('use_att',())): return out
    out=out.clone()
    if op in ('replace_att','replace_both','mix'):
        h=torch.as_tensor(heads,device=out.device)
        out[0,ntext:].index_copy_(1,h,donor_att[step,layer].index_select(1,h))
    elif op=='zero':
        out[0,ntext:].index_fill_(1,torch.as_tensor(heads,device=out.device),0)
    elif op=='route':
        # Exchange the probabilities of the introductory and action mentions
        # of rabbit (22/25) and cat (15/40) for image queries only.
        for start in range(0,len(heads),8):
            hh=heads[start:start+8]
            p=probabilities(q,k,hh)
            change=0
            for i,j in [(22,25),(15,40)]:
                mass=p[...,i]-p[...,j]
                delta=v[0,j,hh].float()-v[0,i,hh].float()
                change=change+mass.unsqueeze(-1)*delta[:,None,:]
            h=torch.as_tensor(hh,device=out.device)
            selected=out[0,ntext:].index_select(1,h)
            out[0,ntext:].index_copy_(1,h,(selected.float()+change.transpose(0,1)).to(out.dtype))
    return out
def ff_hook(i):
    def hook(module,args,out):
        if step not in settings['steps'] or i not in settings['layers']: return
        if settings['op']=='cache': donor_ff[step,i]=out.detach().clone()
        if settings['op'] in ('image_ff','replace_both') or (settings['op']=='mix' and i in settings.get('use_ff',())): return donor_ff[step,i]
    return hook
def single_ff_pre(i):
    def hook(module,args):
        if step not in settings['steps'] or i not in settings['layers']: return
        h=args[0]
        width=pipe.transformer.config.num_attention_heads*pipe.transformer.config.attention_head_dim
        if settings['op']=='cache':
            donor_ff[step,i]=h[:,ntext:,width:].detach().clone()
        elif settings['op'] in ('image_ff','replace_both') or (settings['op']=='mix' and i in settings.get('use_ff',())):
            h=h.clone()
            h[:,ntext:,width:]=donor_ff[step,i]
            return (h,)
    return hook
pipe.transformer.register_forward_pre_hook(begin,with_kwargs=True)
for i,b in enumerate(blocks[:8]): b.ff.register_forward_hook(ff_hook(i))
for i,b in enumerate(blocks[8:],8): b.attn.to_out.register_forward_pre_hook(single_ff_pre(i))
tr.dispatch_attention_fn=routed
def run(name,id='N04',seed=2,op='none',indices=(),plan=None,steps=(0,)):
    global step,layer
    settings.update(seed=seed,case=id,op=op,layers=set(indices),steps=set(steps),plan=plan or {})
    step=-1
    layer=-1
    if id not in emb:
        emb[id]=pipe.encode_prompt(prompt=description[id],device='cuda',max_sequence_length=512)[0]
    im=pipe(prompt_embeds=emb[id],height=512,width=512,num_inference_steps=4,generator=torch.Generator(device='cuda').manual_seed(seed)).images[0]
    im.save(dest/f'{name}__s{seed}.png')
    print('DONE',name,seed,round(time.monotonic()-started,1),flush=True)
def sheet(names, filename, size=154):
    files=sorted([p for p in dest.glob('*__s*.png') if p.name.split('__')[0] in names],key=lambda p:(names.index(p.name.split('__')[0]),p.name))
    cols=min(6,len(files))
    canvas=Image.new('RGB',(cols*size,((len(files)+cols-1)//cols)*size),'white')
    for j,p in enumerate(files):
        x=j%cols*size; y=j//cols*size
        canvas.paste(Image.open(p).resize((size,size)),(x,y))
    canvas.save(dest/filename,quality=90)
    (dest/(filename+'.json')).write_text(json.dumps([p.name for p in files]))
@torch.inference_mode()
def main():
    if args.refine:
        from bowl_measure import traits
        scores=json.loads((dest/'measurements.json').read_text())
        def measure(tag,seed=2):
            return traits(dest/f'{tag}__s{seed}.png')
        def qualifies(m):
            return m['side']>0 and m['pink']>=70 and m['score']>.009 and m['pink']>2*m['green']
        def setup(seed):
            donor_att.clear();donor_ff.clear()
            run('ref_cache',args.donor,seed,op='cache',indices=range(32))
        trials=[]
        def try_mix(tag,selected,seed):
            aa={i for t,i in selected if t=='att'};ff={i for t,i in selected if t=='ff'}
            settings['use_att']=aa;settings['use_ff']=ff
            run(tag,seed=seed,op='mix',indices=aa|ff)
            m=measure(tag,seed)
            trials.append(dict(name=tag,seed=seed,components=sorted(selected),metrics=m))
            return qualifies(m)
        groups=[('att',i) for i in range(32)]+[('ff',i) for i in range(32)]
        setup(2)
        byone=sorted(groups,key=lambda c:scores.get(f'{c[0]}_L{c[1]+1:02}__s2',{}).get('score',-1),reverse=True)
        winners=[c for c in byone if qualifies(scores.get(f'{c[0]}_L{c[1]+1:02}__s2',dict(side=0,pink=0,green=0,score=0)))]
        if winners: selected={winners[0]}
        else:
            selected=set(groups)
            if not try_mix('mix_anchor',selected,2):selected=set()
            else:
                seq=0
                for width in (16,8,4,2,1):
                    for kind in ('att','ff'):
                        for first in range(0,32,width):
                            removed={(kind,i) for i in range(first,first+width)}&selected
                            if not removed or not selected-removed:continue
                            seq+=1
                            if try_mix(f'mix_{seq:03}',selected-removed,2):selected-=removed
        if selected:
            for seed in [0,1,2]:
                setup(seed)
                try_mix('replicate',selected,seed)
                control={(kind,(i+9)%32) for kind,i in selected}
                try_mix('replicate_control',control,seed)
                # Reciprocal, put original-failure components in the successful donor.
                donor_att.clear();donor_ff.clear()
                run('baseline_cache','N04',seed,op='cache',indices=range(32))
                aa={i for t,i in selected if t=='att'};ff={i for t,i in selected if t=='ff'}
                settings['use_att']=aa;settings['use_ff']=ff
                run('reciprocal',args.donor,seed,op='mix',indices=aa|ff)
        head_trials=[]
        if selected:
            setup(2)
            aa={i for t,i in selected if t=='att'};ff={i for t,i in selected if t=='ff'}
            settings['use_att']=aa;settings['use_ff']=ff
            for i in sorted(aa):
                for head in range(32):
                    tag=f'headsolo_L{i+1:02}H{head:02}'
                    run(tag,seed=2,op='mix',indices=aa|ff,plan={i:[head]})
                    m=measure(tag)
                    head_trials.append(dict(layer=i,head=head,mode='one_of_32',metrics=m))
                if len(aa)>3: break
            best=sorted([t for t in head_trials if qualifies(t['metrics'])], key=lambda t:t['metrics']['score'], reverse=True)[:2]
            for t in best:
                i=t['layer'];head=t['head']
                for seed in (0,1,2):
                    setup(seed)
                    settings['use_att']=aa;settings['use_ff']=ff
                    for key,hs in [('retain',[head]),('omit',[h for h in range(32) if h!=head]),('other',[(head+1)%32])]:
                        tag=f'{key}_L{i+1:02}H{head:02}'
                        run(tag,seed=seed,op='mix',indices=aa|ff,plan={i:hs})
                        head_trials.append(dict(layer=i,head=head,seed=seed,mode=key,metrics=measure(tag,seed)))
        (dest/'refinement.json').write_text(json.dumps(dict(selected=sorted(selected),single_candidates=winners,trials=trials,head_trials=head_trials),indent=2))
        print('REFINED COMPONENT SET',sorted(selected),flush=True)
    elif args.donor is None:
        names=['orig','pair','g1','g2','g3','g4']
        for s in [2,0,1]:
            run('orig',seed=s,op='observe',indices=range(8))
            run('pair','N03',seed=s,op='observe',indices=range(8))
        import gzip,csv
        with gzip.open(dest/'head_mass.csv.gz','wt') as f:
            w=csv.writer(f); w.writerow(['case','seed','step_index','block_index','head_index','word_group','mass_left','mass_right']);w.writerows(rows)
        for key in description:
            for s in [2,0,1]: run(key,key,s)
        (dest/'guide-prompts.json').write_text(json.dumps(description,indent=2))
        sheet(names,'guide-grid.jpg')
        for s in [2,0,1]:
            run('route_L5H22',seed=s,op='route',indices=[4],plan={4:[22]})
            run('zero_L5H22',seed=s,op='zero',indices=[4],plan={4:[22]})
            run('route_L3to6heads',seed=s,op='route',indices=focus,plan=focus)
            run('route_controls',seed=s,op='route',indices=other,plan=other)
            run('zero_L3to6heads',seed=s,op='zero',indices=focus,plan=focus)
            run('zero_controls',seed=s,op='zero',indices=other,plan=other)
            run('route_all_L3to6',seed=s,op='route',indices=range(2,6))
            run('route_all_double',seed=s,op='route',indices=range(8))
        sheet(['orig','route_L5H22','zero_L5H22','route_L3to6heads','route_controls','zero_L3to6heads','zero_controls','route_all_L3to6','route_all_double'],'target-grid.jpg')
    else:
        names=['orig','cache_'+args.donor]
        # Fixed text, noise, and generation settings on each recipient run.
        for s in [2,0,1]:
            donor_att.clear();donor_ff.clear()
            run('cache_'+args.donor,args.donor,s,op='cache',indices=range(32),steps=[0])
            trials=[('patch_H22','replace_att',[4],{4:[22]}),('patch_heads','replace_att',list(focus),focus),
                  ('patch_L5att','replace_att',[4],None),('patch_L3to6att','replace_att',list(range(2,6)),None),
                  ('patch_L5ff','image_ff',[4],None),('patch_L3to6ff','image_ff',list(range(2,6)),None),
                  ('patch_doubleAtt','replace_att',list(range(8)),None),('patch_doubleFF','image_ff',list(range(8)),None),
                  ('patch_singleAtt','replace_att',list(range(8,32)),None),('patch_allAtt','replace_att',list(range(32)),None),('patch_singleFF','image_ff',list(range(8,32)),None),('patch_allFF','image_ff',list(range(32)),None),('patch_allBoth','replace_both',list(range(32)),None)]
            for name,op,layers,plan in trials:
                run(name,seed=s,op=op,indices=layers,plan=plan)
                if name not in names: names.append(name)
        sheet(names,'patch-grid.jpg')
        # One-component scan on the preselected target seed. Follow-up seeds are
        # needed for any component whose first-step intervention changes the relation.
        donor_att.clear();donor_ff.clear()
        run('cache_'+args.donor,args.donor,2,op='cache',indices=range(32))
        scan=[]
        for i in range(32):
            for label,op in [('att','replace_att'),('ff','image_ff')]:
                tag=f'{label}_L{i+1:02}'
                run(tag,seed=2,op=op,indices=[i])
                scan.append(tag)
        sheet(scan,'scan-grid.jpg',size=145)
    print('FINISHED',flush=True)
main()
