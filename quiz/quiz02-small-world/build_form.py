#!/usr/bin/env python3
"""Build the Google Form for Quiz 2 (small-world networks).

The form is a drop box, not a copy of the quiz. The questions live in
`quiz02.pdf`, which the form links to; all the form does is take a photo of the
student's handwritten answers. Nothing to keep in sync with the sheet.

    python3 build_form.py --print          # dump the batchUpdate payload
    python3 build_form.py --sync           # rewrite the LIVE form from this file
    python3 build_form.py --create         # make a NEW form and fill it in

`--sync` deletes every item on the live form and recreates it, so run it only
before any responses come in.

It shells out to `gws` (the Google Workspace CLI) against the Binghamton
account. `gws` handles the OAuth; if the token has expired it opens a browser.

THE UPLOAD QUESTIONS ARE ADDED BY HAND. The Forms API answers "Creation of
file_upload question not supported", so the two questions that matter are made
in the Forms editor:

    Question 1   File upload, images, 1 file, 10 MB, required
    Question 2   File upload, images, 1 file, 10 MB, required

One per quiz question, so `gforms_download.py` can name the files `q1-` and
`q2-` and you can grade one question across the whole class at a time. The
number in the title is what it reads, so keep "Question 1" / "Question 2".

Respondents must be signed in to a Google account, which every @binghamton.edu
student is. `--sync` wipes those two questions along with everything else, so
re-add them afterwards --- it refuses unless you also pass --force.
"""

import argparse
import json
import os
import subprocess
import sys

GWS_CONFIG_DIR = os.path.expanduser("~/.config/gws-binghamton")

FORM_ID = "106JO7K2xBvgDFcr7FeO0vaX8i-VhcHAiU_VgYv8S75I"

TITLE = "Quiz 2 — Small-world networks"
DOCUMENT_TITLE = "advnetsci-quiz02-small-world"

QUIZ_PDF = "https://go.skojaku.com/quiz02"

DESCRIPTION = (
    "Advanced Network Science - Fall 2026\n\n"
    "15 minutes - 10 points - Closed notes, work on your own.\n\n"
    f"The questions: {QUIZ_PDF}\n\n"
    "Write each question's answer on its own page. Photograph each page and "
    "upload it below - one photo per question. Keep the drawings large and the "
    "labels readable."
)


def items():
    return [
        {
            "title": "Your working file",
            "description": (
                f"The two questions are in the PDF: {QUIZ_PDF}\n\n"
                "One photo per question, in the two boxes below."
            ),
            "textItem": {},
        },
    ]


def payload():
    return {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {"description": DESCRIPTION},
                    "updateMask": "description",
                }
            },
            {
                # Not a quiz in the Forms sense: nothing here is auto-scored,
                # and quiz mode would hand students a "view score" page. Email
                # is VERIFIED so each photo maps to an @binghamton.edu address.
                "updateSettings": {
                    "settings": {
                        "quizSettings": {"isQuiz": False},
                        "emailCollectionType": "VERIFIED",
                    },
                    "updateMask": "quizSettings.isQuiz,emailCollectionType",
                }
            },
            *[
                {"createItem": {"item": item, "location": {"index": i}}}
                for i, item in enumerate(items())
            ],
        ]
    }


def gws(*args):
    env = dict(os.environ, GOOGLE_WORKSPACE_CLI_CONFIG_DIR=GWS_CONFIG_DIR)
    out = subprocess.run(
        ["gws", *args], env=env, capture_output=True, text=True, check=True
    ).stdout
    # gws prints a keyring line before the JSON body.
    return json.loads(out[out.index("{"):])


def batch_update(form_id, requests):
    return gws(
        "forms", "forms", "batchUpdate",
        "--params", json.dumps({"formId": form_id}),
        "--json", json.dumps({"requests": requests}),
    )


def sync(force=False):
    form = gws("forms", "forms", "get", "--params", json.dumps({"formId": FORM_ID}))
    existing = form.get("items", [])
    uploads = [
        it["title"] for it in existing
        if "fileUploadQuestion" in ((it.get("questionItem") or {}).get("question") or {})
    ]
    if uploads and not force:
        # The API cannot put these back, so refuse to be the thing that ate them.
        print("refusing: this would delete upload questions the API cannot recreate")
        for title in uploads:
            print(f"  - {title}")
        print("pass --force if you mean it, then re-add them in the Forms editor")
        sys.exit(1)
    requests = [
        {"deleteItem": {"location": {"index": i}}}
        for i in range(len(existing) - 1, -1, -1)
    ]
    requests += payload()["requests"]
    batch_update(FORM_ID, requests)
    print(f"replaced {len(existing)} items with {len(items())} on form {FORM_ID}")
    if uploads:
        print("now re-add the file-upload questions by hand: " + ", ".join(uploads))


def create():
    form = gws(
        "forms", "forms", "create",
        "--json", json.dumps({"info": {"title": TITLE, "documentTitle": DOCUMENT_TITLE}}),
    )
    form_id = form["formId"]
    batch_update(form_id, payload()["requests"])
    print("form id:  ", form_id)
    print("responder:", form["responderUri"])
    print("editor:   ", f"https://docs.google.com/forms/d/{form_id}/edit")
    print()
    print("Now add the file-upload question by hand, then point")
    print("go.skojaku.com/ans-quiz02 at the responder URL.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print", action="store_true", dest="dump",
                        help="dump the batchUpdate payload and exit")
    parser.add_argument("--sync", action="store_true",
                        help="rewrite the live form from this file")
    parser.add_argument("--force", action="store_true",
                        help="let --sync delete the hand-made upload questions")
    parser.add_argument("--create", action="store_true",
                        help="create a NEW form and fill it in")
    opts = parser.parse_args()
    if opts.dump:
        print(json.dumps(payload(), indent=2, ensure_ascii=False))
    elif opts.sync:
        sync(force=opts.force)
    elif opts.create:
        create()
    else:
        parser.print_help()
        sys.exit(1)
