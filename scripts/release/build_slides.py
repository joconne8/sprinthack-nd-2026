"""Build an offline HTML deck; optional PowerPoint export from verified renderings."""
import argparse
import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--pptx', action='store_true'); args = parser.parse_args()
    slides = json.loads((ROOT / 'planning/pitch/slides.json').read_text())
    output = ROOT / 'presentation'; output.mkdir(exist_ok=True)
    if args.pptx:
        from pptx import Presentation
        from pptx.util import Inches
        presentation = Presentation(); presentation.slide_width = Inches(13.333333); presentation.slide_height = Inches(7.5)
        for i, content in enumerate(slides):
            slide = presentation.slides.add_slide(presentation.slide_layouts[6])
            slide.shapes.add_picture(str(output / 'slides' / f'{i+1:02d}.png'), 0, 0, width=presentation.slide_width, height=presentation.slide_height)
            slide.notes_slide.notes_text_frame.text = content['notes'] + '\n\n' + content['title'] + '\n' + content.get('body', '')
        presentation.core_properties.title = 'Goodwill Michiana — Reporting You Can Trace'
        presentation.core_properties.subject = 'Synthetic P0 prototype progress and live-pilot roadmap'
        presentation.save(output / 'goodwill-progress.pptx')
        print('Exported 10-slide PowerPoint with speaker notes.'); return
    sections = []
    for i, content in enumerate(slides):
        kind = content.get('kind', 'card-slide'); parts = []
        parts.append('<div class="eyebrow">' + html.escape(content['eyebrow']) + '</div>')
        parts.append('<h1>' + html.escape(content['title']).replace('\n', '<br>') + '</h1>')
        parts.append('<p class="lead">' + html.escape(content.get('body', '')).replace('\n', '<br>') + '</p>')
        if 'cards' in content:
            cards = []
            for n, card in enumerate(content['cards']):
                cards.append(f'<div class="card"><span class="card-number">0{n+1}</span><h2>{html.escape(card["title"])}</h2><p>{html.escape(card["text"]).replace(chr(10), "<br>")}</p></div>')
            parts.append('<div class="cards">' + ''.join(cards) + '</div>')
        if 'image' in content:
            image_path = output / content['image']
            encoded = base64.b64encode(image_path.read_bytes()).decode()
            parts.append('<div class="product-frame"><div class="window-bar"><i></i><i></i><i></i><span>Actual synthetic application</span></div><img alt="Recorded '+html.escape(content['title'])+'" src="data:image/png;base64,'+encoded+'"></div>')
        if kind == 'video':
            parts.append('<video controls preload="metadata" aria-label="Narrated synthetic application demo" src="demo.mp4"></video>')
        if kind in ('title', 'closing'):
            parts.append('<div class="signature"><span>ACQUIRE</span><b>→</b><span>VERIFY</span><b>→</b><span>UNDERSTAND</span></div>')
        parts.append('<footer><span>' + html.escape(content.get('source', 'Working synthetic prototype · no live vendor connection')) + f'</span><span>GOODWILL / {i+1:02d}</span></footer>')
        sections.append(f'<article class="slide {kind}" id="slide-{i+1}" aria-label="Slide {i+1}" data-notes="{html.escape(content["notes"], quote=True)}">'+''.join(parts)+'</article>')
    css = '''
    *{box-sizing:border-box}body{margin:0;background:#0b1e2e;color:#142e45;font-family:Arial,Helvetica,sans-serif}#frame{position:relative;margin:24px auto}#deck{position:relative;width:1600px;height:900px;transform-origin:top left}.slide{position:absolute;inset:0;display:none;overflow:hidden;background:#f5f3ec;padding:76px 96px}.slide.active{display:block}.eyebrow{font-size:18px;letter-spacing:3px;color:#397263;font-weight:700;margin-bottom:32px}h1{font-size:78px;line-height:1.06;letter-spacing:-3.5px;margin:0 0 30px;max-width:1330px}.lead{font-size:27px;line-height:1.45;color:#506274;max-width:1150px;margin:0}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:44px}.card{background:white;border:1px solid #d7dfdc;border-radius:16px;padding:27px 30px;min-height:236px}.card-number{font-family:monospace;color:#397263;font-size:18px}h2{font-size:31px;letter-spacing:-.8px;margin:18px 0 13px}.card p{font-size:22px;line-height:1.5;color:#506274;margin:0}footer{position:absolute;bottom:34px;left:96px;right:96px;display:flex;justify-content:space-between;gap:25px;font-size:15px;color:#617483;border-top:1px solid #d3dad6;padding-top:16px}.title,.closing{background:radial-gradient(ellipse at 110% 15%,#316958 0%,#142e45 47%);color:#fff}.title h1{font-size:104px;margin-top:78px}.title .lead,.closing .lead{color:#cbdad5;font-size:30px;max-width:1030px}.title .eyebrow,.closing .eyebrow{color:#a3ccb5}.signature{display:flex;gap:22px;align-items:center;margin-top:72px;font-size:24px;letter-spacing:3px;font-weight:700}.signature b{color:#cbdcb5}.title footer,.closing footer{color:#c9d6d9;border-color:#547075}.closing h1{font-size:96px;margin-top:60px}.closing .signature{margin-top:34px}.flow .card{background:#142e45;color:white;border:none}.flow h2{font-size:42px}.flow .card p{color:#d0ded8}.flow .card-number{color:#a5c9af}.image h1,.video h1{font-size:72px;max-width:620px}.image .lead{width:550px;margin-top:30px;font-size:25px}.product-frame{position:absolute;top:95px;right:80px;width:755px;height:656px;border:1px solid #c9d6d1;background:#fff;overflow:hidden;border-radius:18px;box-shadow:0 24px 60px #142e4522}.window-bar{height:40px;background:#e4eae8;display:flex;align-items:center;gap:7px;padding:0 15px}.window-bar i{height:9px;width:9px;background:#9db0a9;border-radius:50%}.window-bar span{margin-left:13px;font-size:12px;color:#506274}.product-frame img{width:100%;height:616px;object-fit:cover;object-position:top}.image:nth-of-type(6) img{object-position:bottom}.video .lead{width:575px;font-size:24px}.video video{position:absolute;right:80px;top:240px;width:770px;height:432px;border-radius:14px;background:#142e45;box-shadow:0 24px 50px #142e4522}.controls{display:flex;justify-content:center;align-items:center;gap:16px;color:#d4e1da;font-size:15px}button{background:#234658;color:white;border:1px solid #547075;border-radius:6px;padding:10px 18px;cursor:pointer}.controls a{color:#d4e1da}.notes{position:fixed;bottom:0;left:0;right:0;z-index:100;background:#fff;color:#142e45;padding:20px 10%;font-size:18px;line-height:1.5;display:none}.notes.open{display:block}.notes strong{display:block;margin-bottom:8px}
    @media print{@page{size:1600px 900px;margin:0}body{background:white}#frame{margin:0;width:1600px!important;height:auto!important}#deck{height:auto;transform:none!important}.slide{position:relative;display:block!important;width:1600px;height:900px;break-after:page;-webkit-print-color-adjust:exact;print-color-adjust:exact}.controls,.notes{display:none!important}.slide:last-child{break-after:auto}video:after{content:'Play demo.mp4 from the presentation folder'}}
    '''
    js = '''
    const slides=[...document.querySelectorAll('.slide')];let current=0;
    function fit(){const scale=Math.min((innerWidth-30)/1600,(innerHeight-100)/900);document.querySelector('#deck').style.transform='scale('+scale+')';document.querySelector('#frame').style.width=1600*scale+'px';document.querySelector('#frame').style.height=900*scale+'px';}
    function show(index){slides[current].querySelector('video')?.pause();current=Math.max(0,Math.min(slides.length-1,index));slides.forEach((s,i)=>s.classList.toggle('active',i===current));document.querySelector('#counter').textContent=(current+1)+' / '+slides.length;document.querySelector('#note-text').textContent=slides[current].dataset.notes;history.replaceState(null,'','#'+(current+1));}
    document.querySelector('#next').onclick=()=>show(current+1);document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#notes-toggle').onclick=()=>document.querySelector('.notes').classList.toggle('open');document.querySelector('#fullscreen').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();
    document.addEventListener('keydown',e=>{if(e.target.tagName==='VIDEO')return;if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='n')document.querySelector('.notes').classList.toggle('open')});addEventListener('resize',fit);fit();show(Math.max(0,(Number(location.hash.slice(1))||1)-1));
    '''
    text = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Goodwill · Reporting you can trace</title><style>'+css+'</style></head><body><main id="frame"><div id="deck">'+''.join(sections)+'</div></main><nav class="controls" aria-label="Presentation"><button id="prev">← Previous</button><span id="counter"></span><button id="next">Next →</button><button id="notes-toggle">Speaker notes (N)</button><button id="fullscreen">Fullscreen</button><a href="goodwill-progress.pdf">PDF</a><a href="goodwill-progress.pptx">PowerPoint</a><a href="demo.mp4">Demo video</a></nav><aside class="notes"><strong>Presenter notes</strong><span id="note-text"></span></aside><script>'+js+'</script></body></html>'
    (output / 'index.html').write_text(text)
    print('Built offline HTML slides with embedded verified screenshots.')


if __name__ == '__main__': main()
