"""python3 scripts/gen_character.py [--model google/gemini-3.1-flash-image] [--only 1,3] [--ref a.png,b.png --set ref|white|boy|glasses|lines|b4|gaze|touch]

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
WHITE_RULE = (
    ' COLOUR RULE: keep the colours minimal. The hair, the robe and the face plate are all white or the faintest off-white (the face plate only a hint of warm cream); '
    'use exactly ONE small accent colour on the whole character (named below) and nothing else; the outlines stay thick and black. '
)
CANDIDATES_WHITE = {
    1: 'White hair as one big smooth shape with a small side loop, white robe; the one accent colour is lavender, on a small hairclip and the sash only.',
    2: 'White short hair with one small ahoge on top, white robe; the one accent colour is sky blue, on the sash only.',
    3: 'White hair in two short low twin tails, white robe; the one accent colour is soft pink, on a small ribbon on one twin tail only.',
    4: 'White long straight hair, white robe, one foot waving; the one accent colour is pale yellow, on a small star hairclip only.',
    5: 'White hair with a side ponytail, white robe, typing on a tiny white keyboard on the floor with one hand while the other hand props the chin; the one accent colour is lavender, on the hair tie only.',
}
BOY_NOTE = (
    ' The character is a BOY with short hair cut close in a Japanese "sports cut" (a short, flat-topped crop: no long strands, no bangs, no ponytail, no ahoge, no loop). A sporty, cheerful kid. '
    'His outfit is given below and OVERRIDES the robe mentioned above. Keep the same thick black outlines and the same lying pose. '
)
CANDIDATES_BOY = {
    1: 'White hair (just a clean outline with a very light grey crop texture), white short-sleeve T-shirt and white shorts, bare feet in the air; the one accent colour is sky blue, on a sweatband on one wrist only.',
    2: 'White hair, white gym shirt and white shorts, white sneakers on the raised feet; the one accent colour is lavender, on a small towel around the neck only.',
    3: 'White hair, white loose robe like the attached style but for a boy, bare feet; the one accent colour is pale yellow, on the sash only.',
    4: 'White hair, white T-shirt and white shorts, typing on a tiny white keyboard on the floor with one hand while the other hand props the chin; the one accent colour is sky blue, on a wristband only.',
    5: 'White hair, white hooded sweatshirt (hood down) and white shorts, one foot waving, white socks; the one accent colour is soft pink, on the sock cuffs only.',
}
MORE_COLOUR = (
    ' COLOUR RULE: still light and minimal, but a little more colour than pure white is welcome: mostly white and off-white, plus two to four SOFT pastel colours in all (named below); '
    'no red, no green, no strong or dark colours except the thick black outlines. '
)
GLASSES_NOTE = ' The boy WEARS GLASSES (drawn simply: two round or square lenses with a frame and a small bridge, the eyes as tiny dash-like dots seen through them). '
CANDIDATES_GLASSES = {
    1: 'Round glasses with thin dark frames; light grey hair; white T-shirt with sky-blue sleeves; pale yellow wristband.',
    2: 'Square glasses with sky-blue frames; soft light-brown hair; white hoodie; pale blue shorts; pale yellow socks.',
    3: 'Round glasses with lavender frames; soft grey hair; white gym shirt with a lavender collar; a sky-blue towel around the neck.',
    4: 'Typing on a tiny pale-pink keyboard on the floor with one hand while the other hand props the chin; square glasses with lavender frames; light-brown hair; white T-shirt; sky-blue wristband.',
    5: 'Round glasses sliding a little down the nose; soft light-brown hair; pale yellow T-shirt; sky-blue shorts; white socks with pink cuffs; one foot waving.',
}
HAIR_LINES = (
    ' HAIR: the hair is drawn as ONLY a few short black line strokes (four to seven short strokes, like a close-cropped sports cut) on the top of the head; the head itself is just the skin colour. '
    'NO filled hair shape, NO hair colour, no bangs, no outline of a hair mass. '
)
CANDIDATES_LINES = {
    1: 'Round glasses with thin dark frames; white T-shirt with sky-blue sleeves; pale yellow wristband; bare feet.',
    2: 'Square glasses with sky-blue frames; white hoodie; pale blue shorts; pale yellow socks.',
    3: 'Round glasses with lavender frames; white gym shirt with a lavender collar; a sky-blue towel around the neck.',
    4: 'Typing on a tiny pale-pink keyboard on the floor with one hand while the other hand props the chin; square glasses with lavender frames; white T-shirt; sky-blue wristband.',
    5: 'Round glasses sliding a little down the nose; pale yellow T-shirt; sky-blue shorts; white socks with pink cuffs; one foot waving.',
}
REFINE = (
    'The FIRST attached image is a character to KEEP: a short-haired boy lying on his stomach, typing on a tiny keyboard. The OTHER attached images show the target drawing STYLE. '
    'Redraw the SAME boy (same pose, same outfit, same keyboard, same sky-blue wristband, short sports-cut hair, white clothes) but match the target style much more faithfully: '
    'noticeably thicker, even black outlines; a very large round head on a tiny body; a flat, slightly tilted face plate with tiny dash-like eyes and a small smile; '
    'soft off-white and cream fills with a hint of pale lavender-grey in the shadows of the clothes and hair, like the target; simple, rounded, slightly wobbly hand-drawn shapes. '
    'Do NOT copy the character of the target images; only their style. Pure white background, no text, whole character visible, generous margin. '
)
CANDIDATES_B4 = {
    1: 'Keep it as close to the first image as possible, only restyled.',
    2: 'Restyled, and the boy has a tiny pale-lavender hairclip on the short hair (a small accent like in the target).',
    3: 'Restyled, and the boy wears round glasses with thin dark frames.',
    4: 'Restyled, with a slightly bigger head, a more tilted face plate, and white sneakers on his raised feet.',
}
GAZE = (
    'The FIRST attached image is the character to KEEP: a short-haired boy lying on his stomach at a tiny keyboard. The SECOND attached image is another boy whose face is turned and whose eyes look up and to the right: '
    'it shows the gaze I want. The remaining attached images show the target drawing STYLE. '
    'Redraw the boy from the first image, in the same drawing style, same outfit, same keyboard, same sky-blue wristband and short hair, but make him LOOK TOWARD THE UPPER RIGHT of the picture: '
    'the face is turned slightly toward the right and the eyes look up and to the right, as if he is reading something above and to the right. '
    'One hand just idly rests on and fiddles with the tiny keyboard, without looking at it. Do NOT copy the other characters; only the gaze and the style. '
    'Pure white background, no text, whole character visible, generous margin. '
)
CANDIDATES_GAZE = {
    1: 'No glasses; exactly as in the first image otherwise.',
    2: 'Keep the bigger head, the more tilted face plate and the white sneakers of the first image.',
    3: 'Keep the round glasses with thin dark frames of the first image; the eyes seen through the lenses look up and to the right.',
    4: 'Keep the small pale-lavender hairclip of the first image.',
}
TOUCH = (
    'The FIRST attached image is a picture whose COMPOSITION must NOT change: keep exactly the same character, pose, camera, proportions, placement of every element, expression, gaze, clothes and colours. '
    'The SECOND attached image (a dog character in a chat-bubble video) shows the TOUCH I want: soft rounded shapes; slightly rough, wobbly, hand-drawn marker-like outlines in a dark brown-black with uneven line width; '
    'flat cream-white fills with a little texture at the edges; round soft-pink blush spots on the cheeks; and a thin pale sticker-like edge around the whole character. '
    'Redraw the first picture in that touch only (line quality, softness, blush, sticker edge). Do not copy the dog. Pure white background, no text, whole character visible, generous margin. '
)
CANDIDATES_TOUCH = {1: '', 2: '', 3: '', 4: ''}
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
    if SET in ('ref', 'white', 'boy', 'glasses', 'lines', 'b4', 'gaze', 'touch'):
        prompt = (TOUCH if SET == 'touch' else GAZE + CANDIDATES_GAZE[n] if SET == 'gaze' else REFINE + CANDIDATES_B4[n] if SET == 'b4' else REF_STYLE) + ('' if SET in ('b4', 'gaze', 'touch') else BOY_NOTE + GLASSES_NOTE + MORE_COLOUR + HAIR_LINES + CANDIDATES_LINES[n] if SET == 'lines' else WHITE_RULE + CANDIDATES_WHITE[n] if SET == 'white' else BOY_NOTE + WHITE_RULE + CANDIDATES_BOY[n] if SET == 'boy' else BOY_NOTE + GLASSES_NOTE + MORE_COLOUR + CANDIDATES_GLASSES[n] if SET == 'glasses' else CANDIDATES_REF[n])
        parts = [{'type': 'text', 'text': prompt}]
        for path in REFS:
            with open(path, 'rb') as f:
                parts.append({'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(f.read()).decode()}})
        content = parts
        name = f'{SET}-{n}'
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


todo = [n for n in {'ref': CANDIDATES_REF, 'white': CANDIDATES_WHITE, 'boy': CANDIDATES_BOY, 'glasses': CANDIDATES_GLASSES, 'lines': CANDIDATES_LINES, 'b4': CANDIDATES_B4, 'gaze': CANDIDATES_GAZE, 'touch': CANDIDATES_TOUCH}.get(SET, CANDIDATES) if only is None or n in only]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(make, n) for n in todo]):
        try:
            n, size, err = fut.result()
            print(f'{SET} {n}:', f'{size} bytes' if size else f'no image ({err})')
        except Exception as e:  # noqa: BLE001
            print('error:', type(e).__name__, str(e)[:200])
