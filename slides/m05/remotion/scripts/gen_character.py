"""python3 scripts/gen_character.py [--model google/gemini-3.1-flash-image] [--only 1,3] [--ref a.png,b.png --set ref]

Candidates for the narrator of the video: a chibi person lying on their stomach, drawn in a flat, thick-outline touch, made with a Gemini image model through
OpenRouter (the key is read from $OPENROUTER_API_KEY and never written anywhere). Writes out/character/cand-N.png and cand-N.txt (the prompt).
With `--set ref --ref a.png,b.png` the images are sent to the model as a STYLE reference (the touch of the lines and fills), with an instruction to draw a new, original character;
without `--ref` nothing is uploaded and the touch is described in words. Standard library only. Each image costs a few cents.
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
SET = args[args.index('--set') + 1] if '--set' in args else 'words'
REFS = args[args.index('--ref') + 1].split(',') if '--ref' in args else []
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

REF_STYLE = (
    'The attached image(s) show a drawing STYLE I like: a chibi character lying propped on one elbow, chin on hand; very thick, even, black outlines; flat off-white and cream fills '
    'with a few pale lavender accents; a huge round head with the hair as one big smooth shape; a flat, slightly tilted face plate with tiny dash-like eyes and a small smile; a tiny body in a loose white robe with a sash. '
    'Draw a NEW, ORIGINAL character in exactly that drawing style and the same relaxed lying pose, but do NOT copy the character in the attached image: give them a different hairstyle, hair colour and outfit as described. '
    'Keep the outline thickness, the flat fills and the simplicity of the attached style. Pure white background, no text, no shadow, whole character visible, generous margin. '
)
CANDIDATES_REF = {
    1: 'Pale pink hair with two small buns and a heart-shaped hairpin, white robe with a pink sash.',
    2: 'Black bob hair with a single lavender hairclip, white robe with a dark navy sash.',
    3: 'Light brown short hair with one small leaf-shaped ahoge on top, cream robe with a green-grey sash.',
    4: 'Long straight silver hair without any loop or ribbon, white robe with a navy sash, one foot waving.',
    5: 'Pale blue hair with a side ponytail, white robe, typing on a tiny keyboard on the floor with one hand while the other hand props the chin.',
}

key = os.environ.get('OPENROUTER_API_KEY')
if not key:
    sys.exit('OPENROUTER_API_KEY is not set')
os.makedirs('out/character', exist_ok=True)


def make(n):
    if SET == 'ref':
        prompt = REF_STYLE + CANDIDATES_REF[n]
        parts = [{'type': 'text', 'text': prompt}]
        for path in REFS:
            with open(path, 'rb') as f:
                parts.append({'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(f.read()).decode()}})
        content = parts
        name = f'ref-{n}'
    else:
        prompt = STYLE + CANDIDATES[n]
        content = prompt
        name = f'cand-{n}'
    body = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': content}],
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
    with open(f'out/character/{name}.png', 'wb') as f:
        f.write(raw)
    with open(f'out/character/{name}.txt', 'w') as f:
        f.write(f'model: {MODEL}\n\n{prompt}\n')
    return n, len(raw), None


todo = [n for n in (CANDIDATES_REF if SET == 'ref' else CANDIDATES) if only is None or n in only]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(make, n) for n in todo]):
        try:
            n, size, err = fut.result()
            print(f'{SET} {n}:', f'{size} bytes' if size else f'no image ({err})')
        except Exception as e:  # noqa: BLE001
            print('error:', type(e).__name__, str(e)[:200])
