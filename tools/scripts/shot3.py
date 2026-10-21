import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for name,vp in [('desk',{'width':1300,'height':820}),('mob',{'width':390,'height':844})]:
      pg=await b.new_page(viewport=vp)
      errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
      await pg.goto('file:///mnt/user-data/outputs/mapa-mudo-espana.html');await pg.wait_for_timeout(600)
      await pg.click('[data-s=rios]');await pg.wait_for_timeout(300);await pg.screenshot(path=f'{name}_rios.png')
      await pg.click('[data-m=trib]');await pg.wait_for_timeout(300);await pg.screenshot(path=f'{name}_trib.png')
      await pg.click('.opts button');await pg.wait_for_timeout(300)
      await pg.click('[data-m=find]');await pg.wait_for_timeout(200)
      bx=await pg.locator('#map').bounding_box();await pg.mouse.click(bx['x']+bx['width']*.45,bx['y']+bx['height']*.4);await pg.wait_for_timeout(300)
      await pg.screenshot(path=f'{name}_rfind.png')
      await pg.click('[data-m=study]');
      await pg.click('[data-s=rel]');await pg.wait_for_timeout(300);await pg.screenshot(path=f'{name}_rel.png')
      await pg.click('[data-m=what]');await pg.wait_for_timeout(300)
      await pg.click('[data-m=exam]');await pg.click('#st');await pg.mouse.click(bx['x']+bx['width']*.5,bx['y']+bx['height']*.3)
      await pg.click('[data-s=costa]');await pg.wait_for_timeout(200)
      # self-hit test for all objects
      r=await pg.evaluate('''()=>{const bad=[];for(const o of O){const p=o.kind==='line'?o.lines[0][Math.floor(o.lines[0].length/2)]:o.xy[0];const[n]=nearest(p[0],p[1],O.filter(q=>CSEC[q.cat]===CSEC[o.cat]));if(n!==o)bad.push(o.id+'->'+n.id)}return bad}''')
      print(name,errs,r)
    await b.close()
asyncio.run(main())
