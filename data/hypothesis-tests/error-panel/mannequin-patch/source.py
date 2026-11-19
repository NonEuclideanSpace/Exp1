from pathlib import Path
import json,gc
import torch
from PIL import Image
from diffusers import Flux2KleinKVPipeline
from diffusers.models.transformers import transformer_flux2 as tr
root=Path('/root/autodl-tmp/flux-experiments/2026-11-19/07-hypothesis-tests/error-panel/mannequin-grid')
p=root/'patch';p.mkdir(exist_ok=True)
all_jobs=json.loads((root/'full-contact/design.json').read_text())['jobs']
jobs=[r for r in all_jobs if r['feed_layout'] and r['role']=='right-bottom' and r['distance']=='near' and r['seed'] in (31,32)]
selected={25,26,27,29,30,31,32};other=set(range(12,19));N=1024;T=512
settings={'selected_blocks':sorted(selected),'same_size_control_blocks':sorted(other),'samples':[j['id'] for j in jobs],'selection':'All four near right-bottom cells in the two text-control seeds; examined matched images for clear original failures with reference and clear correct text-only contacts in all four. This is a paired diagnostic sample, not a frequency estimate.','intervention':'Keep recipient Q and K unchanged, substitute current image-token V from same-seed other branch at same grid indices. Text, reference-token V and non-image query outputs unchanged. refdrop separately zeros reference-token V without renormalizing weights. Donor and recipient differ in reference, resulting pose and framing. Judge target and composition separately.'}
(p/'design.json').write_text(json.dumps(settings,indent=2))
class Experiment:
 def __init__(self):
  self.pipe=Flux2KleinKVPipeline.from_pretrained('/root/autodl-tmp/models/black-forest-labs/FLUX.2-klein-9b-kv',torch_dtype=torch.bfloat16,local_files_only=True)
  self.pipe.set_progress_bar_config(disable=True);self.pipe.text_encoder.to('cuda')
  self.emb={j['id']:self.pipe.encode_prompt(j['prompt'],device='cuda',max_sequence_length=512,text_encoder_out_layers=(9,18,27))[0] for j in jobs}
  self.pipe.register_modules(text_encoder=None);gc.collect();torch.cuda.empty_cache()
  self.pipe.transformer.to('cuda');self.pipe.vae.to('cuda')
  self.orig=tr.dispatch_attention_fn;tr.dispatch_attention_fn=self.att
  self.pipe.transformer.register_forward_pre_hook(self.begin)
  blocks=list(self.pipe.transformer.transformer_blocks)+list(self.pipe.transformer.single_transformer_blocks)
  self.handles=[]
  for i,b in enumerate(blocks):
   self.handles.append(b.register_forward_pre_hook(self.enter(i+1)))
 def begin(self,*_):self.step+=1
 def enter(self,i):
  def hook(*_):self.b=i
  return hook
 def att(self,q,k,v,*args,**kw):
  out=self.orig(q,k,v,*args,**kw)
  if q.shape[1]==N and k.shape[1]==N:return out
  if q.shape[1]!=T+N or k.shape[1] not in (T+N,T+2*N):raise ValueError((q.shape,k.shape))
  key=self.step,self.b
  if self.b not in selected | other:return out
  if self.variant in ('capture-good','capture-bad'):
   self.bank[self.variant,key]=v[:,-N:].detach().cpu();return out
  blocks=other if self.variant=='earlier-blocks' else selected
  steps=(3,4) if self.variant=='late-steps' else (1,2)
  if self.b not in blocks or self.step not in steps:return out
  vv=v.clone()
  if self.variant=='refdrop':
   if k.shape[1]==T+2*N:vv[:,T:T+N]=0
  else:
   bank='capture-bad' if self.variant in ('reverse','sham') else 'capture-good'
   vv[:,-N:]=self.bank[bank,key].to(v.device)
  modified=self.orig(q,k,vv,*args,**kw)
  a=out.clone();a[:,-N:]=modified[:,-N:];return a
 def run(self,j,mode):
  self.step=0;self.variant=mode
  args={}
  if mode not in ('capture-good','reverse'):
   with Image.open(root/j['layout']) as src:args['image']=[src.convert('RGB')]
  image=self.pipe(prompt_embeds=self.emb[j['id']],height=512,width=512,num_inference_steps=4,generator=torch.Generator('cuda').manual_seed(j['seed']),**args).images[0]
  image.save(p/f"{j['id']}--{mode}.png")
with torch.inference_mode():
 torch.backends.cuda.matmul.allow_tf32=False
 xp=Experiment()
 modes=['capture-good','capture-bad','sham','V','earlier-blocks','late-steps','refdrop','reverse']
 for j in jobs:
  xp.bank={}
  for mode in modes:xp.run(j,mode)
  print('PATCH',j['id'],flush=True)
 for name,subset in [('forward',modes[:4]),('controls',modes[4:])]:
  out=Image.new('RGB',(4*265,len(subset)*265))
  for row,mode in enumerate(subset):
   for c,j in enumerate(jobs):
    with Image.open(p/f"{j['id']}--{mode}.png") as im:out.paste(im.resize((265,265),Image.Resampling.LANCZOS),(265*c,265*row))
  out.save(p/(name+'.jpg'),quality=96)
(p/'finished.json').write_text(json.dumps(dict(n=len(jobs)*len(modes),modes=modes)))
