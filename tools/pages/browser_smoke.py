#!/usr/bin/env python3
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import json
from pathlib import Path
import argparse,shutil,tempfile,threading
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser(description='Optional real-Chromium Pages UI smoke test; requires Playwright and Chromium.')
parser.add_argument('--site-dir',type=Path,default=Path('/tmp/geometric-labs-pages'))
parser.add_argument('--output-dir',type=Path,default=Path('/tmp/geometric-pages-browser-review'))
args=parser.parse_args()
artifact=args.site_dir.resolve()
args.output_dir.mkdir(parents=True,exist_ok=True)
expected=json.loads((artifact/'data/status.json').read_text())
area_count=len(expected['sections'])
experimental_count=sum(s['status']=='experimental' for s in expected['sections'])
with tempfile.TemporaryDirectory(prefix='pages-preview-') as directory:
    shutil.copytree(artifact,Path(directory)/'Geometric-Labs')
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=directory))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}/Geometric-Labs/'
    results=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
            context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
            errors=[];requests=[]
            page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('request',lambda request:requests.append(request.url))
            page.goto(base);page.wait_for_selector('.project-card')
            assert page.locator('.project-card').count()==area_count
            assert 'Geometry' in page.locator('h1').inner_text()
            assert 'earlier audited revision' in page.locator('#evidence-description').inner_text()
            page.screenshot(path=str(args.output_dir/'desktop.png'),full_page=False)
            page.get_by_role('button',name='Experimental',exact=True).click()
            assert page.locator('.project-card').count()==experimental_count
            page.get_by_role('button',name='All areas',exact=True).click()
            page.locator('#search').fill('hurwitz')
            assert page.locator('.project-card').count()>0
            for text in page.locator('#file-list li').all_text_contents():assert 'hurwitz' in text.lower()
            page.locator('#search').fill('no-such-section-abcdef')
            assert page.locator('#no-results').is_visible()
            page.locator('#search').fill('')
            page.get_by_role('button',name='Experiments',exact=True).click()
            assert page.locator('.project-card').count()==1
            assert 'AlexNet' in page.locator('.project-card h3').inner_text()
            page.get_by_role('button',name='All areas',exact=True).click()
            assert page.locator('.project-card').count()==area_count
            results.append('desktop: sections, filters, search, empty state, development-loop reset, evidence label')
            page.set_viewport_size({'width':390,'height':844});page.goto(base);page.wait_for_selector('.project-card')
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
            page.screenshot(path=str(args.output_dir/'mobile.png'),full_page=False)
            page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(n)=>n===document.activeElement')
            page.get_by_role('link',name='Project map',exact=True).click()
            page.get_by_role('button',name='Experimental',exact=True).click()
            assert page.locator('.project-card').count()==experimental_count
            results.append('mobile 390px: no horizontal page overflow, keyboard skip link and filtering')
            assert not errors,errors
            assert all(url.startswith(base) for url in requests),requests
            results.append('homepage: no runtime errors or third-party network requests')
            assert context.request.get(base+'research-ide/index.html').status==200
            assert context.request.get(base+'checkpoint/index.html').status==200
            assert context.request.get(base+'UPDATE_PROCEDURE.md').status==200
            results.append('project subpath: local CSS/JS/data, checkpoint, IDE and update guide resolve')
            alias=context.new_page()
            alias.route('**/*',lambda route:route.continue_() if route.request.url.startswith(base) else route.abort())
            assert context.request.get(base+'Research_IDE/index.html').status==200
            alias.goto(base+'Research_IDE/index.html',wait_until='domcontentloaded')
            alias.wait_for_url(base+'research-ide/index.html')
            alias.close()
            results.append('Research_IDE/index.html: reported case-sensitive URL redirects to the canonical Research IDE')
            payload=json.loads((artifact/'data/status.json').read_text())
            payload['recent_commits'][0]['subject']='<img src=x onerror="window.injected=true">'
            test=context.new_page()
            test.route('**/data/status.json',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(payload)))
            test.goto(base);test.wait_for_selector('#activity li')
            assert test.locator('#activity img').count()==0
            assert test.evaluate('window.injected') is None
            assert '<img' in test.locator('#activity').inner_text()
            results.append('untrusted commit text: rendered inert with textContent')
            fail=context.new_page();fail.route('**/data/status.json',lambda route:route.abort())
            fail.goto(base);fail.locator('#load-error').wait_for(state='visible')
            assert 'Snapshot unavailable' in fail.locator('#source-line').inner_text()
            results.append('data failure: accessible error state and source/checkpoint fallbacks')
            browser.close()
        (args.output_dir/'browser-review.json').write_text(json.dumps({'status':'PASS','browser':'system Chromium via Playwright','checks':results,'screenshots':['desktop.png','mobile.png']},indent=2)+'\n')
        print('\n'.join(results))
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
