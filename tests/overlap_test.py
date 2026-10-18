import sys, json
from playwright.sync_api import sync_playwright
src=sys.argv[1]
import os; os.makedirs('t/srv',exist_ok=True); open('t/srv/ov_b.html','w').write('<!doctype html><html><head><meta charset="utf-8"></head><body>'+open(src).read()+'</body></html>')
SIZES=[(390,740),(540,730),(600,760),(768,740),(800,800),(1280,760),(1280,800),(320,568),(360,640),(375,667),(390,844),(414,896),(430,932),(568,320),(667,375),(844,390),(932,430),(600,960),(768,1024),(820,1180),(1024,768),(1180,820),(1366,1024),(1440,900)]
CHECK="""(()=>{const bad=[];const R=e=>e.getBoundingClientRect();
 const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
 const ov=(a,b)=>a.left<b.right-0.5&&b.left<a.right-0.5&&a.top<b.bottom-0.5&&b.top<a.bottom-0.5;
 const inside=(a,b)=>a.left>=b.left-0.5&&a.right<=b.right+0.5&&a.top>=b.top-0.5&&a.bottom<=b.bottom+0.5;
 const sb=q('.board.solo .sb'), strip=q('.board.solo .bstrip'), board=q('.board.solo');
 if(sb){ const S=R(sb), T=R(strip);
   const parts={lbl:q('.board.solo .sb-main .lbl'),vp:q('.board.solo .vp'),aside:q('.board.solo .sb-aside')};
   for(const [k,e] of Object.entries(parts)){ if(!e) continue; const r=R(e); if(!inside(r,S)) bad.push(k+' outside score area '+JSON.stringify([Math.round(r.top),Math.round(r.bottom),Math.round(S.top),Math.round(S.bottom)])); }
   if(ov(R(parts.vp),R(parts.aside))) bad.push('score overlaps totals');
   if(ov(R(parts.lbl),R(parts.vp))) bad.push('label overlaps score');
   if(!inside(T,R(board))) bad.push('strip outside board');
   if(S.bottom>T.top+0.5) bad.push('score area runs into strip');
   qa('.board.solo .stat').forEach((s,i)=>{const l=R(s.querySelector('.lbl')),b=R(s.querySelector('.big')); if(ov(l,b)) bad.push('stat '+i+' label/number overlap')});
 }
 qa('.scr').forEach((s,i)=>{const t=s.querySelector('.scr-t'),v=s.querySelector('.scr-h .v'),p=s.querySelector('.pend');
   if(t&&v&&ov(R(t),R(v))) bad.push('scorer '+i+' title/value overlap'); if(t&&p&&ov(R(t),R(p))) bad.push('scorer '+i+' title/pending overlap');
   const mt=s.querySelector('.maxtag'); if(mt&&!inside(R(mt),R(s))) bad.push('scorer '+i+' MAX tag clipped');});
 qa('.trk button,.cpbar button,.scr-b button').forEach(b=>{if(b.scrollWidth>b.clientWidth+1) bad.push('button text clipped: '+b.textContent.trim())});
 const cp=q('.cpmid'); if(cp&&cp.scrollWidth>cp.clientWidth+1) bad.push('CP number clipped');
 return bad})()"""
STATES={
 'empty': "",
 'big': "const P=G.players[G.solo]; P.prim=[15,15,15,15,15]; P.sec=[15,15,15,15,15]; P.postP=20; P.postS=8; P.cp=12; render()",
 'pending_max': "const P=G.players[G.solo]; P.prim=[18,0,0,0,0]; P.sec=[15,0,0,0,0]; BATCH_MS=10000; render()",
}
with sync_playwright() as p:
    b=p.chromium.launch(); total=0
    for w,h in SIZES:
        for st,js in STATES.items():
            pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('file:///tmp/claude-0/-home-claude/cd37b6fb-30f6-511d-901d-9e5d80dda4c4/scratchpad/t/srv/ov_b.html'); pg.evaluate("localStorage.clear()"); pg.reload()
            pg.evaluate("SEEN=[true,true]; newGame(); render()"); pg.locator('#app [data-act=solo]').click()
            if js: pg.evaluate(js)
            if st=='pending_max': pg.evaluate("act('bump','sec:1:'); render()")
            pg.wait_for_timeout(120)
            bad=pg.evaluate(CHECK)
            # also the end-of-game screen
            pg.evaluate("commitAll(); const P=G.players[G.solo]; P.screen='post'; P.reachedFS=true; render()"); pg.wait_for_timeout(80)
            bad2=[ 'END: '+x for x in pg.evaluate(CHECK)]
            if bad or bad2 or errs: total+=1; print(f'{w}x{h} {st}:', bad+bad2, errs)
            if st=='big' and (w,h) in [(320,568),(844,390),(768,1024),(1024,768)]:
                pg.evaluate("G.players[G.solo].screen='round'; render()"); pg.wait_for_timeout(80); pg.screenshot(path=f't/ov_{sys.argv[2]}_{w}x{h}.png')
            pg.close()
    print('PROBLEM CASES:', total)
