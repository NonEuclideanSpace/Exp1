from pathlib import Path
from itertools import combinations
from PIL import Image
from diffusers import Flux2KleinKVPipeline
from diffusers.models.transformers import transformer_flux2 as tr
from safetensors.torch import load_file,save_file
import torch,json,math,gc,sys
from bowl_measure import traits
B=Path('/root/flux2-bowl-interventions-20261119')
D=B/'routing-values-fp32';D.mkdir(exist_ok=True)
MODEL='/root/autodl-tmp/models/black-forest-labs/FLUX.2-klein-9b-kv'
SELECT={24,25,26,28,29,30,31}
T=512
baseline='/root/flux2-binding-round2-20261119/results/N04/text_condition.safetensors'
dispatch=tr.dispatch_attention_fn
class Study:
 def __init__(self):
  self.pipe=Flux2KleinKVPipeline.from_pretrained(MODEL,torch_dtype=torch.bfloat16,local_files_only=True)
  self.pipe.set_progress_bar_config(disable=True)
  source=json.loads((B/'guide-prompts.json').read_text())['g1']
  donor_path=B/'routing-values'/'donor.safetensors'
  if donor_path.exists():self.donor=load_file(str(donor_path))['prompt_embeds'].to('cuda')
  else:
   self.pipe.text_encoder.to('cuda')
   self.donor=self.pipe.encode_prompt(prompt=source,device='cuda',max_sequence_length=512)[0].detach()
   save_file({'prompt_embeds':self.donor.cpu()},str(donor_path))
  self.pipe.register_modules(text_encoder=None)
  gc.collect();torch.cuda.empty_cache()
  self.pipe.transformer.to('cuda');self.pipe.vae.to('cuda')
  self.base=load_file(baseline)['prompt_embeds'].to('cuda')
  self.cache={};self.pipe.transformer.register_forward_pre_hook(self.begin)
  tr.dispatch_attention_fn=self.attention
 def begin(self,*args):self.step+=1;self.block=-1
 def factor(self,q,k,v,output):
  q=q[0,T:].transpose(0,1); k=k[0].transpose(0,1); v=v[0,T:].transpose(0,1)
  routing=[];text=[]
  for pos in range(0,len(q),4):
   region=slice(pos,pos+4)
   weights=(q[region].float()@k[region].float().transpose(1,2)/math.sqrt(q.shape[-1])).softmax(-1)[...,T:]
   image=weights@v[region].float()
   text.append(output[0,T:,region].transpose(0,1).float()-image)
   routing.append(weights)
  return torch.cat(routing),v.contiguous(),torch.cat(text)
 def attention(self,q,k,v,*args,**kw):
  self.block+=1
  out=dispatch(q,k,v,*args,**kw); key=self.step,self.block
  if self.step not in self.steps or self.block not in SELECT or self.variant=='base':return out
  if self.variant=='capture':
   r,vv,t=self.factor(q,k,v,out)
   self.cache[key]=(r.cpu(),vv.contiguous().cpu(),t.cpu(),out[0,T:].clone().cpu())
   return out
  a=out.clone();rd,vd,td,od=self.cache[key]
  if self.variant=='whole':
   a[0,T:]=od.to(a.device);return a
  rr,vr,tt=self.factor(q,k,v,out)
  route=rd.to(a.device) if 'R' in self.variant else rr
  values=vd.to(a.device) if 'V' in self.variant else vr
  text=td.to(a.device) if 'T' in self.variant else tt
  for h in range(0,32,4):
   hs=slice(h,h+4)
   mix=route[hs].float() @ values[hs].float()+text[hs]
   a[0,T:,hs]=mix.transpose(0,1).to(a.dtype)
  return a
 def run(self,name,seed,steps):
  self.step=-1;self.block=-1;self.variant=name;self.steps=steps
  args=dict(prompt_embeds=self.donor if name=='capture' else self.base,height=512,width=512,num_inference_steps=4,generator=torch.Generator('cuda').manual_seed(seed))
  im=self.pipe(**args).images[0]
  path=D/('step'+''.join(str(i+1) for i in sorted(steps))+f'_{name}__s{seed}.png')
  im.save(path);print('FACTOR',path.name,traits(path)['score'],flush=True)
@torch.inference_mode()
def main():
 torch.backends.cuda.matmul.allow_tf32=False
 study=Study()
 for seed in (2,1,0):
  study.cache.clear();study.run('capture',seed,{0,1})
  for step in ({0,1},{0}):
   for tag in ('base','whole','copy','R','V','T','RV','RT','VT','RVT'):
    filename='step'+''.join(str(i+1) for i in sorted(step))+f'_{tag}__s{seed}.png'
    if not (D/filename).exists():study.run(tag,seed,step)
 records={p.name:traits(p) for p in D.glob('*.png')}
 (D/'results.json').write_text(json.dumps(records,indent=2))
 print('FACTORIAL COMPLETE',flush=True)
if __name__=='__main__':main()
