#!/usr/bin/env python3
"""Build the Google Form for Quiz 1 (Euler paths).

The form is a drop box, not a copy of the quiz. The questions live in
`quiz01.pdf`, which the form links to; all the form does is take a photo of the
student's handwritten answers. Nothing to keep in sync with the sheet.

    python3 build_form.py --print          # dump the batchUpdate payload
    python3 build_form.py --sync           # rewrite the LIVE form from this file
    python3 build_form.py --create         # make a NEW form and fill it in

`--sync` deletes every item on the live form and recreates it, so run it only
before any responses come in.

It shells out to `gws` (the Google Workspace CLI) against the Binghamton
account. `gws` handles the OAuth; if the token has expired it opens a browser.

THE UPLOAD QUESTION IS ADDED BY HAND. The Forms API answers "Creation of
file_upload question not supported", so the one question that matters is made
in the Forms editor: File upload, images and PDF, 2 files, 10 MB, required.
Respondents must be signed in to a Google account, which every
@binghamton.edu student is. `--sync` wipes it along with everything else, so
re-add it afterwards.
"""

import argparse
import json
import os
import subprocess
import sys

GWS_CONFIG_DIR = os.path.expanduser("~/.config/gws-binghamton")

FORM_ID = "1zEVrm1Qt29IhAIcp4LieXNx854WGXPoj7vPzpSizS6Q"

TITLE = "Quiz 1 — Euler paths"
DOCUMENT_TITLE = "advnetsci-quiz01-euler-paths"

QUIZ_PDF = "https://go.skojaku.com/quiz01"

DESCRIPTION = (
    "Advanced Network Science - Fall 2026\n\n"
    "15 minutes - 10 points - Closed notes, work on your own.\n\n"
    f"The questions: {QUIZ_PDF}\n\n"
    "Write your answers by hand, photograph the page, and upload it below. "
    "Keep the drawings large and the labels readable."
)


def items():
    return [
        {
            "title": "Your working",
            "description": (
                f"The two questions are in the PDF: {QUIZ_PDF}\n\n"
                "Upload one clear photo of your handwritten answers. Two photos "
                "if one page is not enough."
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


def sync():
    form = gws("forms", "forms", "get", "--params", json.dumps({"formId": FORM_ID}))
    count = len(form.get("items", []))
    requests = [{"deleteItem": {"location": {"index": i}}} for i in range(count - 1, -1, -1)]
    requests += payload()["requests"]
    batch_update(FORM_ID, requests)
    print(f"replaced {count} items with {len(items())} on form {FORM_ID}")
    print("now re-add the file-upload question by hand")


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
    print("go.skojaku.com/ans-quiz01 at the responder URL.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print", action="store_true", dest="dump",
                        help="dump the batchUpdate payload and exit")
    parser.add_argument("--sync", action="store_true",
                        help="rewrite the live form from this file")
    parser.add_argument("--create", action="store_true",
                        help="create a NEW form and fill it in")
    opts = parser.parse_args()
    if opts.dump:
        print(json.dumps(payload(), indent=2, ensure_ascii=False))
    elif opts.sync:
        sync()
    elif opts.create:
        create()
    else:
        parser.print_help()
        sys.exit(1)
