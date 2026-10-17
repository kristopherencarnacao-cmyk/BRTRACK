# Real-timer test of score batching. Usage: python3 tests/batching_test.py index.html  (needs Playwright + Chromium)
import sys, os
from playwright.sync_api import sync_playwright
src=sys.argv[1]; d=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.tmp'); os.makedirs(d,exist_ok=True)
name=os.path.basename(src).replace('.html','')
open(f'{d}/{name}_b.html','w').write('<!doctype html><html><head><meta charset="utf-8"></head><body>'+open(src).read()+'</body></html>')
fails=[]
def check(label, cond, extra=''):
    print(('PASS ' if cond else 'FAIL ')+label+(f'  [{extra}]' if extra else ''))
    if not cond: fails.append(label)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(f'file://{d}/{name}_b.html'); pg.evaluate("localStorage.clear()"); pg.reload()
    a=lambda s: pg.locator('#app '+s).first.click()
    vp=lambda: int(pg.locator('#app .board .vp').inner_text().replace('--','0'))
    tot=lambda: pg.locator('#app .stats').inner_text().replace('\n',' ').replace('--','0')
    pend=lambda: [x.inner_text() for x in pg.locator('#app .pend').all()]
    panel=lambda i: pg.locator('#app .scr-h .v').nth(i).inner_text().replace('--','0')
    undo_lbl=lambda: pg.locator('#app [data-act=undo]').get_attribute('aria-label')
    hist=lambda: pg.evaluate("G.players[G.solo].history.length")
    a('[data-act=solo]')

    # 1 tally + commit after 3 s from LAST tap
    a('[data-arg="prim:3:"]'); a('[data-arg="prim:2:"]')
    check('1a tally shows +5 on Primary', pend()==['+5'], pend())
    check('1b scoreboard not yet updated', vp()==0 and panel(0)=='0', f'vp {vp()} panel {panel(0)}')
    check('1c faint +5 beside score label', '+5' in pg.locator('#app .board .lbl').first.inner_text())
    check('1d countdown bar showing', pg.locator('#app .pbar.on i').count()==1)
    pg.wait_for_timeout(2000); a('[data-arg="sec:1:"]')
    check('1e both panels pending, shared batch', pend()==['+5','+1'], pend())
    pg.wait_for_timeout(2000)
    check('1f 2 s after last tap: still pending (timer restarted)', vp()==0 and pend()==['+5','+1'], f'vp {vp()}')
    pg.wait_for_timeout(1300)
    check('1g ~3 s after last tap: committed', vp()==6 and pend()==[] and tot()=='PRIMARY 5 SECONDARY 1'.title().upper() or tot().upper()=='PRIMARY 5 SECONDARY 1', f'vp {vp()} {tot()}')
    check('1h one batch = one undo step', hist()==1, hist())
    check('1i undo label names the batch', undo_lbl()=='Undo Primary +5, Secondary +1', undo_lbl())

    # 2 undo during pending cancels ONLY pending
    a('[data-arg="prim:4:"]')
    check('2a undo label says pending', undo_lbl()=='Undo pending Primary +4', undo_lbl())
    a('[data-act=undo]')
    check('2b pending cancelled, committed batch untouched', vp()==6 and pend()==[] and hist()==1, f'vp {vp()} hist {hist()}')
    pg.wait_for_timeout(3300)
    check('2c cancelled points never land', vp()==6, vp())

    # 3 undo after commit removes the whole batch
    a('[data-act=undo]')
    check('3a whole last batch undone', vp()==0 and hist()==0, f'vp {vp()}')

    # 4 mixed +1 then -1 nets zero -> nothing pending, no empty batch
    a('[data-arg="prim:1:"]'); a('[data-arg="prim:-1:"]')
    check('4a net zero clears pending', pend()==[] and pg.evaluate("G.players[G.solo].pend")==None)
    pg.wait_for_timeout(3300)
    check('4b no empty batch in undo history', hist()==0, hist())
    check('4c undo disabled', pg.locator('#app [data-act=undo]').is_disabled())

    # 5 floor at zero
    a('[data-arg="sec:-1:"]')
    check('5a -1 at 0 does nothing', pend()==[], pend())
    a('[data-arg="sec:2:"]'); a('[data-arg="sec:-1:"]'); a('[data-arg="sec:-1:"]'); a('[data-arg="sec:-1:"]')
    check('5b pending never drops committed+pending below 0', pend()==[], pend())

    # 6 Next round within 3 s commits to the ORIGINAL round
    a('[data-arg="prim:4:"]'); a('[data-act=endRound]')
    check('6a moved to BR2', pg.locator('#app .trk .cur').inner_text()=='BR2')
    check('6b points committed instantly to BR1', vp()==4 and pg.evaluate("G.players[G.solo].prim[0]")==4 and pg.evaluate("G.players[G.solo].prim[1]")==0)

    # 7 jumping to a past round commits first
    a('[data-arg="sec:3:"]'); a('[data-act=goRound][data-arg="1"]')
    check('7a BR2 secondary committed to BR2 before jump', pg.evaluate("G.players[G.solo].sec[1]")==3 and pg.locator('#app .trk .cur').inner_text()=='BR1')

    # 8 tap the tally to commit now
    a('[data-arg="prim:2:"]'); a('#app .pend') if False else pg.locator('#app .pend').first.click()
    check('8a tapping +2 commits now', pend()==[] and pg.evaluate("G.players[G.solo].prim[0]")==6, pg.evaluate("G.players[G.solo].prim[0]"))

    # 9 CP is instant and its own undo step
    h0=hist(); a('.foot [data-arg="cp:2:"]')
    check('9a CP instant', pg.locator('#app .cpmid .v').inner_text()=='2' and pend()==[])
    check('9b CP is its own undo step', hist()==h0+1 and undo_lbl()=='Undo Command points +2', undo_lbl())
    a('[data-arg="prim:1:"]'); a('[data-act=undo]')
    check('9c undo with pending cancels pending, not the CP', pg.locator('#app .cpmid .v').inner_text()=='2' and pend()==[])
    a('[data-act=undo]'); check('9d next undo reverts CP', pg.locator('#app .cpmid .v').inner_text()=='0')

    # 10 app backgrounded mid-countdown: commit + save immediately
    a('[data-arg="prim:5:"]'); before=pg.evaluate("G.players[G.solo].prim[0]")
    pg.evaluate("Object.defineProperty(document,'visibilityState',{configurable:true,get:()=> 'hidden'}); document.dispatchEvent(new Event('visibilitychange'))")
    saved=pg.evaluate("JSON.parse(localStorage.getItem('scorehammer:game')).G.players[JSON.parse(localStorage.getItem('scorehammer:game')).G.solo].prim[0]")
    check('10a hidden -> committed', pg.evaluate("G.players[G.solo].prim[0]")==before+5 and pend()==[], f'{before}->{pg.evaluate("G.players[G.solo].prim[0]")}')
    check('10b hidden -> saved with the points', saved==before+5, saved)
    pg.evaluate("Object.defineProperty(document,'visibilityState',{configurable:true,get:()=> 'visible'})")

    # 11 closed with pending (save written mid-batch) -> restored with points kept
    a('[data-arg="sec:4:"]'); pg.evaluate("save()")   # the save every render makes, while pending
    secb=pg.evaluate("G.players[G.solo].sec[0]")
    pg.evaluate("window.removeEventListener('pagehide', ()=>{})"); 
    pg.goto('about:blank'); pg.goto(f'file://{d}/{name}_b.html')
    check('11a reopen restores and commits pending', pg.evaluate("G.players[G.solo].sec[0]")==secb+4 and pend()==[], pg.evaluate("G.players[G.solo].sec[0]"))

    # 12 phone asleep past the deadline: commits on wake (timestamp, not just a timer)
    a('[data-arg="prim:1:"]'); pg.evaluate("G.players[G.solo].pend.due = Date.now()-1")
    pg.wait_for_timeout(300)
    check('12a overdue batch commits on next tick', pend()==[])

    # 13 final scoring batches too, and Finish commits first
    for _ in range(5): a('[data-act=endRound]') if pg.locator('#app [data-act=endRound]').count() else None
    if pg.locator('#app h2').first.inner_text().upper()!='FINAL SCORING': a('[data-act=goRound][data-arg="6"]')
    a('[data-arg="postP:3:"]'); check('13a end-of-game tally', pend()==['+3'], pend())
    a('[data-act=finish]'); check('13b Finish commits pending', pg.evaluate("G.players[G.solo].postP")==3)

    print('JS ERRORS', errs); print('FAILED:', fails or 'none')
