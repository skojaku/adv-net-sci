"""python3 scripts/gen_character.py [--model google/gemini-3.1-flash-image] [--only 1,3]

Candidates for the narrator of the video: a chibi person lying on their stomach, drawn in a flat, thick-outline touch, made with a Gemini image model through
OpenRouter (the key is read from $OPENROUTER_API_KEY and never written anywhere). Writes out/character/cand-N.png and cand-N.txt (the prompt).
Standard library only. Each image costs a few cents.
"""
import base64
import concurrent.futures
import json
import os
import sys
import urllib.request

MODEL = 'google/gemini-3.1-flash-image'
args = sys.argv[1:]
if '--model' in args:
    MODEL = args[args.index('--model') + 1]
only = None
if '--only' in args:
    only = {int(x) for x in args[args.index('--only') + 1].split(',')}

STYLE = (
    'A flat 2D illustration of a cute chibi character lying on their stomach, seen from the side, propping the head up on one hand, feet in the air. '
    'Style: thick, uniform, clean black outlines; flat pastel fills with no shading and no gradients; very simple, minimal shapes; big round head, '
    'straight bangs, tiny dot eyes, a small gentle smile; calm and cute, like a hand-drawn sticker or a simple animation frame. '
    'Pure white background, no text, no shadow, no props other than those named, the whole character visible and centred with generous empty margin. '
)
CANDIDATES = {
    1: 'The character has silver-white bob hair with a small side loop tied with a lavender ribbon, and wears a loose white robe with a lavender sash. Chin on one hand.',
    2: 'The character has short black hair and round glasses, wears a pale grey hoodie, and has a small open laptop on the floor in front of them; one hand rests on the keyboard.',
    3: 'The character has brown hair in a bun, wears a cream sweater, chin resting on both hands, ankles crossed, feet in the air.',
    4: 'The character has pastel blue hair, wears an oversized white t-shirt, and types on a tiny keyboard on the floor in front of them with both hands, head lifted.',
    5: 'The character wears pyjamas with the hood up (small round ears on the hood), cheek on one hand, one foot waving.',
    6: 'The character has short light grey hair and wears large headphones around the neck and a pale blue sweater, chin on one hand, lazily kicking one foot.',
}

key = os.environ.get('OPENROUTER_API_KEY')
if not key:
    sys.exit('OPENROUTER_API_KEY is not set')
os.makedirs('out/character', exist_ok=True)


def make(n):
    prompt = STYLE + CANDIDATES[n]
    body = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'modalities': ['image', 'text'],
        'image_config': {'aspect_ratio': '3:2'},
    }).encode()
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body, headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.load(r)
    msg = data['choices'][0]['message']
    images = msg.get('images') or []
    if not images:
        return n, None, (msg.get('content') or str(data)[:300])
    url = images[0]['image_url']['url']
    raw = base64.b64decode(url.split(',', 1)[1])
    with open(f'out/character/cand-{n}.png', 'wb') as f:
        f.write(raw)
    with open(f'out/character/cand-{n}.txt', 'w') as f:
        f.write(f'model: {MODEL}\n\n{prompt}\n')
    return n, len(raw), None


todo = [n for n in CANDIDATES if only is None or n in only]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(make, n) for n in todo]):
        try:
            n, size, err = fut.result()
            print(f'cand-{n}:', f'{size} bytes' if size else f'no image ({err})')
        except Exception as e:  # noqa: BLE001
            print('error:', type(e).__name__, str(e)[:200])
