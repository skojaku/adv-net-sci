"""python3 scripts/gen_character.py [--model google/gemini-3.1-flash-image] [--only 1,3] [--ref a.png,b.png --set ref|white|boy|glasses|lines|b4|gaze|touch|both|pose|prone|pframe|expr|cup|new]

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
BOTH = (
    'The FIRST attached image is the character to KEEP, exactly in its drawing style (thick black outlines, soft off-white fills, a hint of pale lavender shading, tiny dot eyes, a small smile) and with the same '
    'body, clothes, sky-blue wristbands and tiny keyboard. The other attached image is only a style anchor. '
    'Redraw the character with ONE change: BOTH hands are on the tiny keyboard, fiddling with it (both arms stretched forward, the fingers of both hands on the keys, a sky-blue wristband on each wrist). '
    'The hand that held the chin is gone: the head is simply held up, slightly raised. Same camera, same proportions, same lying pose. Pure white background, no text, whole character visible, generous margin. '
)
CANDIDATES_BOTH = {
    1: 'The gaze stays as in the first image.',
    2: 'He looks toward the UPPER RIGHT of the picture: the face is turned slightly to the right and the tiny dot eyes sit toward the upper right; the hands keep fiddling without looking at them.',
    3: 'A relaxed, lazy fiddling: the wrists rest on the keyboard edge and the fingers are loosely spread. The gaze stays as in the first image.',
    4: 'He looks toward the UPPER RIGHT as in a daydream, and two small motion marks near the fingers show the typing.',
}
POSE = (
    'The FIRST attached image is the character to KEEP, exactly: the same boy, the same drawing style (thick black outlines, soft off-white fills, a hint of pale lavender shading), the same head, '
    'the same flat face plate with tiny dash-like eyes, the same short hair shape, white T-shirt and shorts, sky-blue wristbands, white sneakers. '
    'He is lying on his stomach, in the SAME camera and the SAME scale: the head, the torso and the legs sit at the same place on the canvas as in the first image (the pictures will be swapped as animation frames), '
    'and only what is described below changes. KEYBOARD RULE: the tiny cream keyboard lies on the floor at the lower left, at exactly the same place, size and angle as in the first image, in EVERY picture, '
    'also when his hands are not on it (then it simply lies there alone); it is never moved, never removed, never redrawn. He stays lying flat on his stomach on the floor, never floating. Pure white background, no text, whole character visible, generous margin. '
)
POSE_REF = ' The SECOND attached image (a dog character) is only a reference for the gesture and the facial expression: copy the gesture and the expression onto the boy, never the dog. '
PRONE = (
    'The FIRST attached image is the character to KEEP: the same boy, the same drawing style (thick black outlines, soft off-white fills, a hint of pale lavender shading), the same big round head, '
    'the same flat face plate with tiny dash-like eyes and a small smile, the same short hair shape, white T-shirt and shorts, sky-blue wristbands, white sneakers, and the same tiny cream keyboard. '
    'REDRAW him in a different, NATURAL pose, because the first image is twisted: the head faces the viewer while the body lies sideways. '
    'New pose: he lies FLAT ON HIS STOMACH, the body seen purely from the SIDE (like a person lying on a bed, seen from the side), the whole body in ONE relaxed, straight, horizontal line from the head to the feet '
    'with NO twisting of the shoulders or hips: chest and belly on the floor, the back on top, the legs stretched out behind him. '
    'The head faces RIGHT, toward the tiny keyboard that lies on the floor in front of him (to the right of the head); both forearms lie on the floor in front of him with the elbows bent, and both hands are on the keyboard, typing. '
    'The picture is a side view: the head is at the right, the feet at the left. Pure white background, no text, whole character visible, generous margin. '
)
CANDIDATES_PRONE = {
    1: 'The head is lifted a little and seen in side profile, facing right, with one dash eye and a small smile; the legs lie flat and straight behind him.',
    2: 'The head is lifted a little in three-quarter view (the face plate turned a little toward the viewer, but the body stays a straight side view); the knees are bent and the feet are raised in the air behind him, crossed at the ankles.',
    3: 'A relaxed pose: the chin low, the head only slightly raised and seen in side profile facing right; the legs lie flat, the feet resting on the floor.',
    4: 'The head is in a cartoon three-quarter view (the face plate fairly frontal, looking at the keyboard), set on the straight side-view body; one foot is raised a little behind him.',
}
PFRAME = (
    'The FIRST attached image is the character to KEEP, exactly: the same boy lying flat on his stomach seen from the side (head at the right, facing right, in three-quarter view), the same drawing style '
    '(thick black outlines, soft off-white fills, a hint of pale lavender shading), the same big round head and face, the same short hair shape, white T-shirt and shorts, sky-blue wristbands, white sneakers, '
    'the knees bent and the feet raised in the air behind him, crossed at the ankles. Keep the SAME camera and scale: the head, the torso and the legs sit at exactly the same place on the canvas as in the first image '
    '(the pictures will be swapped as animation frames), and only what is described below changes. '
    'KEYBOARD RULE: the tiny cream keyboard lies on the floor in front of his head at exactly the same place, size and angle as in the first image, in every picture, never moved, never removed, never redrawn. '
    'Pure white background, no text, whole character visible, generous margin. '
)
# n: (the change, an expression reference or None)
CANDIDATES_PFRAME = {
    1: ('TYPING FRAME A. Only the hands change: the hand nearest the viewer is pressed flat on the keys with the wrist low, and the other hand, partly hidden behind it, is lifted a little above the keys. The face stays exactly as in the first image.', None),
    2: ('TYPING FRAME B. Only the hands change: the hand nearest the viewer is lifted a little above the keys with the fingers curled, and the other hand, partly hidden behind it, presses down on the keys. The face stays exactly as in the first image.', None),
    3: ('TROUBLED FACE WHILE STILL TYPING. Only the face changes: the eyebrow drawn as a short slanted line tilted down toward the middle (worried), the eye a small dash, the mouth a small wavy line instead of the smile, and one small blue sweat drop near the temple. The hands stay on the keyboard exactly as in the first image.', 'worry'),
    4: ('TROUBLED FACE WHILE STILL TYPING, stronger. Only the face changes: both eyebrows as short slanted lines tilted down toward the middle, the eye looking down and sideways at the keyboard, a small wavy mouth, and one small blue sweat drop near the temple. The hands stay on the keyboard exactly as in the first image.', 'worry'),
    5: ('RELAXED SHRUG. The eye is closed as a slim calm arc, a small content smile, the shoulders raised a little, and both hands lifted off the keyboard and held open with the palms up beside it, like a gentle shrug. The feet stay up as in the first image.', 'shrug'),
    7: ('TYPING FRAME C (the opposite of frame A). Only the hands change: the hand nearest the viewer, with the wristband in front, is lifted clearly above the keys, about the height of a hand, the wrist raised, the fingers curled and spread as if about to strike; the other hand, behind it, is pressed flat on the keys. The face stays exactly as in the first image.', None),
    8: ('TYPING FRAME C2. Only the hands change: the hand nearest the viewer is lifted high above the keys with the index finger pointing down at a key, the wrist raised; the other hand, behind it, presses on the keys. The face stays exactly as in the first image.', None),
    9: ('HOVERING FRAME. Only the hands change: both hands are lifted a little off the keys with a visible gap, the fingers curled, as a typist hovers between bursts. The face stays exactly as in the first image.', None),
    10: ('TYPING FRAME C3. Only the hands change: the hand nearest the viewer is lifted high and tilted, the fingers curled, with two tiny short motion lines beside the fingers; the other hand, behind it, presses flat on the keys. The face stays exactly as in the first image.', None),
    11: ('TYPING FRAME C, the opposite of frame A. At the keyboard there are two hands: an UPPER hand (farther from the viewer, behind, higher in the picture) and a LOWER hand (nearer to the viewer, in front, lower in the picture, the one with the lower wristband). In the first image the LOWER hand is pressed flat on the keys. Now the LOWER hand is lifted clearly off the keys, with a visible gap of about the height of a hand, the wrist raised and the fingers curled as if about to strike, while the UPPER hand is pressed flat on the keys. Only the hands change; the face stays exactly as in the first image.', None),
    12: ('TYPING FRAME C2. At the keyboard there are two hands: an UPPER hand (farther from the viewer, behind, higher in the picture) and a LOWER hand (nearer to the viewer, in front, lower in the picture). Now the LOWER hand is lifted high above the keys with the fingers spread and curled like a claw, the wrist raised, while the UPPER hand is pressed flat on the keys. Only the hands change; the face stays exactly as in the first image.', None),
    13: ('TYPING FRAME C3. At the keyboard there are two hands: an UPPER hand (farther from the viewer, behind) and a LOWER hand (nearer to the viewer, in front, lower in the picture). Now the LOWER hand is raised just off the keys, one fingertip about to touch a key, while the UPPER hand is pressed flat on the keys with the wrist low. Only the hands change; the face stays exactly as in the first image.', None),
    14: ('TYPING FRAME C, with the roles of the hands swapped. The SECOND attached image shows the OPPOSITE of what I want: in it the UPPER hand (farther from the viewer) is lifted and the LOWER hand (nearer to the viewer) presses the keys. Draw the opposite of the second image: the LOWER hand, the one nearer to the viewer with the lower wristband, is lifted clearly off the keys with the wrist raised and the fingers curled, and the UPPER hand is pressed flat on the keys. Everything else stays as in the first image; copy nothing else from the second image.', None),
    15: ('TYPING FRAME C2, roles swapped. The SECOND attached image shows the OPPOSITE of what I want: its UPPER hand is lifted and its LOWER hand (nearer to the viewer) presses. Draw the opposite: the LOWER hand is raised high above the keys with spread, curled fingers, the wrist well off the keys, and the UPPER hand presses a key with its fingers. Everything else stays as in the first image; copy nothing else from the second image.', None),
    16: ('TYPING FRAME C3, roles swapped. The SECOND attached image shows the OPPOSITE of what I want: its UPPER hand is lifted and its LOWER hand (nearer to the viewer) presses. Draw the opposite: the LOWER hand hovers a little above the keys with the fingers curled, ready to strike, and the UPPER hand is pressed down on the keys. Everything else stays as in the first image; copy nothing else from the second image.', None),
    17: ('TYPING FRAME C. The attached picture is the character with a RED CIRCLE and a RED ARROW drawn on it as instructions. The red circle marks the LOWER hand (the one with the lower wristband, in front); the red arrow says that this hand must move UP. In the result the circled LOWER hand is lifted clearly off the keys, about the height of a hand above them, the wrist raised, the fingers curled as if about to strike, and the other (UPPER) hand is pressed flat on the keys. REMOVE the red circle and the red arrow completely. Everything else stays exactly as it is in the picture, including the face, the body, the feet and the keyboard.', None),
    18: ('TYPING FRAME C2. The attached picture has a RED CIRCLE and a RED ARROW drawn on it as instructions: the circle marks the LOWER hand (with the lower wristband, in front) and the arrow says it must move UP. In the result the LOWER hand is raised high above the keys with spread, curled fingers, the wrist well above the keyboard, while the UPPER hand presses down on the keys. REMOVE the red circle and the red arrow completely. Everything else stays exactly as in the picture.', None),
    19: ('TYPING FRAME C3. The attached picture has a RED CIRCLE and a RED ARROW drawn on it as instructions: the circle marks the LOWER hand (with the lower wristband, in front) and the arrow says it must move UP. In the result the LOWER hand hovers just above the keys, the fingertips about to touch a key, while the UPPER hand is pressed down on the keys. REMOVE the red circle and the red arrow completely. Everything else stays exactly as in the picture.', None),
    20: ('TYPING FRAME C, cleaned up from a rough collage. The attached picture is a ROUGH COLLAGE: the LOWER hand (in front, with the lower wristband) was cut out and rotated upward about the wrist, so that it is lifted above the keys, and a flat cream patch was painted on the keyboard where it used to be. Redraw the picture cleanly in the same drawing style: KEEP the lower hand lifted exactly where it is now (the fingers curled, about to strike), join its wrist smoothly to the forearm and the wristband, remove the rough edges, redraw the keys of the keyboard under the lifted hand where the cream patch is, and keep the UPPER hand pressing the keys. Everything else (the head, the face, the body, the feet, the position of the keyboard) must stay exactly as it is.', None),
    21: ('TYPING FRAME C2, cleaned up from a rough collage. The attached picture is a ROUGH COLLAGE: the LOWER hand (in front, with the lower wristband) was cut out and rotated upward about the wrist so that it is lifted above the keys, and a flat cream patch was painted on the keyboard where it used to be. Redraw it cleanly in the same drawing style, keeping the lower hand lifted where it is, with a clearly readable hand shape: four fingers curled down and the thumb, the wrist joined smoothly to the forearm; redraw the keyboard keys under it; keep the UPPER hand pressing the keys, and keep the two hands clearly separate. Everything else stays exactly as it is.', None),
    22: ('TYPING FRAME C3, cleaned up from a rough collage. The attached picture is a ROUGH COLLAGE: the LOWER hand (in front, with the lower wristband) was cut out and rotated upward about the wrist so that it is lifted above the keys. Clean it up in the same drawing style: keep the lower hand lifted where it is, hovering above the keys with relaxed curled fingers; make the wrist and forearm join smoothly; redraw the keyboard keys where the cream patch is; keep the UPPER hand pressing the keys. Everything else stays exactly as it is.', None),
    6: ('SHRUG, elbows out. The eye closed as a slim arc, a small content smile, the head tilted a little to one side, both forearms lifted off the floor with the elbows out and the open hands palms up near the keyboard. The feet stay up as in the first image.', 'shrug'),
}
CUP = (
    'The FIRST attached image is the character to KEEP, exactly, in the same drawing style (thick black outlines, soft off-white fills, a hint of pale lavender shading). '
    'Redraw the same picture with ONE new object added: a cup of hot tea standing on the floor. EVERYTHING else stays exactly the same: the boy, his face, his hands, the keyboard, '
    'the camera, the scale, the position of every line, and the plain white background. '
)
CANDIDATES_CUP = {
    1: 'The cup is a small round ceramic tea cup with a little handle, pale blue glaze like the wristbands, tea inside, and one tiny curl of steam above it. Place it standing on the floor to the right of the boy\'s face, a little behind the keyboard, completely inside the picture with free white space around it. It is about one third as tall as the boy\'s head.',
    2: 'The cup is a small Japanese tea cup (a yunomi, no handle), cream coloured with a thin pale blue band, tea inside, and one tiny curl of steam above it. Place it standing on the floor to the right of the boy\'s face, a little behind the keyboard, completely inside the picture with free white space around it. It is about one third as tall as the boy\'s head.',
    3: 'The cup is a small off-white mug with a handle and a blue stripe, tea inside, and one tiny curl of steam above it. Place it standing on the floor just to the right of the keyboard, at the right edge of the picture, completely inside the picture. It is about one third as tall as the boy\'s head.',
}
NEWPOSE = (
    'The FIRST attached image is the character to KEEP, exactly: the same boy (the same big round head and face, short hair, white T-shirt and shorts, sky-blue wristbands, white sneakers), '
    'the same drawing style (thick black outlines, soft off-white fills, a hint of pale lavender shading), the same small cream keyboard and the same cup of tea with its steam, drawn at the same size. '
    'Draw the boy in the NEW pose described below, on a plain white background, the whole figure fully inside the picture. Unless the pose says otherwise, the keyboard and the cup of tea '
    'stay on the floor at the same place and the same size as in the first image. '
)
CANDIDATES_NEW = {
    1: 'DRAMATIC KEY PUSH. He is lying on his stomach and slams one key of the keyboard: the arm nearest the viewer is raised high above the keyboard and the fist comes down hard on a key, three short motion lines beside the arm, the eyebrows level and the mouth set in a determined look.',
    2: 'PUSH-UP. He pushes his chest up off the floor with both straight arms like a push-up, the head up, a cheerful determined face, the legs still bent up in the air behind him; the keyboard and the cup stay on the floor.',
    3: 'PUSHING AWAY. He lies on his stomach and pushes the keyboard away from himself with both flat palms, the arms straight, a tired "enough" face with one eyebrow raised, two small motion lines.',
    4: 'ON HIS BACK. He lies flat on his back, face up, the head at the right as before, both hands tucked behind his head, the knees up and the legs crossed, the sneakers up, the eyes closed in a relaxed smile. The keyboard and the cup stay on the floor beside him.',
    5: 'ON HIS BACK, STRETCHING. He lies on his back, the arms stretched up over his head, the toes pointed, a big open-mouthed yawn with the eyes closed. The keyboard and the cup stay on the floor.',
    6: 'ON HIS BACK, THINKING. He lies on his back looking up, both hands resting on his stomach, one knee up with the other leg crossed over it, a calm blank look. The keyboard and the cup stay on the floor.',
    7: 'DRINKING TEA. He is on his stomach propped on one elbow, holding the cup of tea with both hands close to his mouth, taking a sip with the eyes closed in a content look, steam rising from the cup. The keyboard lies on the floor in front of him; the floor spot where the cup stood is now empty.',
    8: 'DRINKING TEA, ONE HAND. He lies on his stomach with the head up, one hand holds the cup of tea near his mouth while the other hand still rests on the keyboard, a content look. The floor spot where the cup stood is now empty.',
    9: 'TEA BREAK. He lies on his stomach on both elbows, holding the cup of tea in both hands in front of his chest and looking down into it with a gentle smile, steam rising. The keyboard lies on the floor in front of him; the floor spot where the cup stood is now empty.',
}
CANDIDATES_EXPR = {
    # more faces for the video (lecturer, 2026-10-06: the narrator is monotone). Face only: same camera, same head, the hands stay on the keys.
    1: ('HAPPY FACE WHILE STILL TYPING. Only the face changes: the eye is closed as a happy upward arc, the mouth is a wide open smile, the cheek has a faint pink blush. The hands stay on the keyboard exactly as in the first image.', 'happy'),
    2: ('GRINNING FACE WHILE STILL TYPING. Only the face changes: the eye is a bright round dot with a small white highlight, the eyebrow raised a little, the mouth a big open grin, with two tiny sparkle marks near the head. The hands stay on the keyboard exactly as in the first image.', None),
    3: ('SURPRISED FACE WHILE STILL TYPING. Only the face changes: the eyebrow raised high, the eye wide open as a round circle with a tiny pupil, the mouth a small round open O, and one small exclamation mark floating above the head. The hands stay on the keyboard exactly as in the first image.', None),
    4: ('SURPRISED, OH I SEE. Only the face changes: the eyebrow raised, the eye wide open and round, looking toward the text on the right, the mouth a small open oval. No other marks. The hands stay on the keyboard exactly as in the first image.', None),
    5: ('THINKING FACE WHILE STILL TYPING. Only the face changes: the eye looks up and to the right, one eyebrow raised a little, the mouth a small flat line pushed to one side, and a small thought cloud with three dots floating beside the head. The hands stay on the keyboard exactly as in the first image.', None),
    6: ('PUZZLED THINKING. Only the face changes: the eye looks up and sideways, the eyebrow raised, the mouth a small pursed circle, and one small question mark floating beside the head. The hands stay on the keyboard exactly as in the first image.', None),
    7: ('SMUG FACE WHILE STILL TYPING. Only the face changes: the eye half closed and relaxed, one eyebrow slightly raised, a confident little smirk on one side of the mouth. The hands stay on the keyboard exactly as in the first image.', None),
    8: ('DETERMINED FACE WHILE STILL TYPING. Only the face changes: both eyebrows drawn level and slightly lowered, the eye focused on the text to the right, the mouth a small firm line, and one tiny sweat-free highlight on the cheek. The hands stay on the keyboard exactly as in the first image.', None),
}
CANDIDATES_POSE = {
    1: ('TYPING FRAME A. Only the hands change: the hand at the left end of the keyboard is pressed flat on the keys, the other hand is lifted a little above the keys with the fingers curled, ready to press. The face stays exactly as in the first image.', None),
    2: ('TYPING FRAME B. Only the hands change: the hand at the right side of the keyboard is pressed flat on the keys, the other hand (at the left end) is lifted a little above the keys with the fingers curled. The face stays exactly as in the first image.', None),
    3: ('TROUBLED. He is worried and stuck: the eyebrows are drawn as two short slanted lines tilted down toward the middle, the mouth a small wavy line, and one small blue sweat drop near the temple. He has taken his hands off the keyboard (it lies untouched on the floor) and folds both ARMS crossed in front of him, and his two LEGS are crossed at the ankles in the air.', 'worry'),
    4: ('TROUBLED, thinking hard. He is on his elbows with the arms folded together on the floor in front of the chin; a puzzled, uneasy look, NOT angry: the eyebrows only slightly slanted, the mouth a small wavy line, the eyes tiny dashes looking sideways; the legs crossed at the ankles in the air.', 'worry'),
    5: ('HAPPY. He is delighted: the eyes are closed as two happy arcs, the mouth wide open in a big smile with a small pink tongue, both small fists raised beside the shoulders in a cheering gesture, the feet kicking up in the air; the keyboard lies untouched on the floor.', 'happy'),
    6: ('HAPPY, laughing. The eyes are closed as happy arcs, a wide open smiling mouth, both arms thrown up in the air in a V, the legs kicking high with the feet apart.', 'happy'),
    7: ('RELAXED SHRUG. The eyes are closed as two slim calm arcs, a small content smile, both hands open with the palms up at the sides of the body like a gentle shrug, the legs crossed lazily at the ankles in the air.', 'shrug'),
}
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
    if SET == 'prone':
        prompt = PRONE + CANDIDATES_PRONE[n]
        parts = [{'type': 'text', 'text': prompt}]
        for path in REFS:
            with open(path, 'rb') as f:
                parts.append({'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(f.read()).decode()}})
        content = parts
        name = f'prone-{n}'
    elif SET in ('cup', 'new'):
        prompt = (CUP + CANDIDATES_CUP[n]) if SET == 'cup' else (NEWPOSE + CANDIDATES_NEW[n])
        parts = [{'type': 'text', 'text': prompt}]
        for path in REFS:
            with open(path, 'rb') as f:
                parts.append({'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(f.read()).decode()}})
        content = parts
        name = f'{SET}-{n}'
    elif SET in ('pose', 'pframe', 'expr'):
        change, expr = (CANDIDATES_POSE if SET == 'pose' else CANDIDATES_EXPR if SET == 'expr' else CANDIDATES_PFRAME)[n]
        prompt = (POSE if SET == 'pose' else PFRAME) + change + (POSE_REF if expr else '')
        paths = REFS + ([f'out/character/expr/{expr}.png'] if expr else [])
        parts = [{'type': 'text', 'text': prompt}]
        for path in paths:
            with open(path, 'rb') as f:
                parts.append({'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(f.read()).decode()}})
        content = parts
        name = f'{SET}-{n}'
    elif SET in ('ref', 'white', 'boy', 'glasses', 'lines', 'b4', 'gaze', 'touch', 'both'):
        prompt = (BOTH + CANDIDATES_BOTH[n] if SET == 'both' else TOUCH if SET == 'touch' else GAZE + CANDIDATES_GAZE[n] if SET == 'gaze' else REFINE + CANDIDATES_B4[n] if SET == 'b4' else REF_STYLE) + ('' if SET in ('b4', 'gaze', 'touch', 'both') else BOY_NOTE + GLASSES_NOTE + MORE_COLOUR + HAIR_LINES + CANDIDATES_LINES[n] if SET == 'lines' else WHITE_RULE + CANDIDATES_WHITE[n] if SET == 'white' else BOY_NOTE + WHITE_RULE + CANDIDATES_BOY[n] if SET == 'boy' else BOY_NOTE + GLASSES_NOTE + MORE_COLOUR + CANDIDATES_GLASSES[n] if SET == 'glasses' else CANDIDATES_REF[n])
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


todo = [n for n in {'ref': CANDIDATES_REF, 'white': CANDIDATES_WHITE, 'boy': CANDIDATES_BOY, 'glasses': CANDIDATES_GLASSES, 'lines': CANDIDATES_LINES, 'b4': CANDIDATES_B4, 'gaze': CANDIDATES_GAZE, 'touch': CANDIDATES_TOUCH, 'both': CANDIDATES_BOTH, 'pose': CANDIDATES_POSE, 'prone': CANDIDATES_PRONE, 'pframe': CANDIDATES_PFRAME, 'expr': CANDIDATES_EXPR, 'cup': CANDIDATES_CUP, 'new': CANDIDATES_NEW}.get(SET, CANDIDATES) if only is None or n in only]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(make, n) for n in todo]):
        try:
            n, size, err = fut.result()
            print(f'{SET} {n}:', f'{size} bytes' if size else f'no image ({err})')
        except Exception as e:  # noqa: BLE001
            print('error:', type(e).__name__, str(e)[:200])
