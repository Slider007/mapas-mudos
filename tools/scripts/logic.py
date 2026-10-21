import asyncio,json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844})
    await pg.goto('file:///mnt/user-data/outputs/mapa-mudo-espana.html');await pg.wait_for_timeout(600)
    r=await pg.evaluate('''()=>{const bad=[],close=[];
     for(const o of O){for(const [x,y] of o.xy){const [n]=nearest(x,y);if(n!==o)bad.push(o.name+' -> '+n.name)}}
     for(let i=0;i<O.length;i++)for(let j=i+1;j<O.length;j++){const a=O[i],b=O[j];if(a.kind==='isl'&&b.kind==='isl')continue;
       let d=1e9;for(const p of a.xy)for(const q of b.xy)d=Math.min(d,Math.hypot(p[0]-q[0],p[1]-q[1]));if(d<20)close.push(a.name+' / '+b.name+' '+d.toFixed(1)+'u = '+(d*pxPerUnit()).toFixed(0)+'px')}
     // island inside test
     const isl=O.filter(o=>o.kind==='isl').map(o=>o.name+':'+inIsland(o.id,...o.xy[0]));
     return {bad,close,isl,ppu:pxPerUnit()}}''')
    print(json.dumps(r,ensure_ascii=False,indent=1));await b.close()
asyncio.run(main())
