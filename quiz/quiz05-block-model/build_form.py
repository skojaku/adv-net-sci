#!/usr/bin/env python3
"""Build the Google Form for Quiz 5 (the k-core, and the degree-corrected block model).

The form is a drop box, not a copy of the quiz. The questions live in
`quiz05.pdf`, which the form links to; all the form does is take a photo of the
student's handwritten answers. Nothing to keep in sync with the sheet.

    python3 build_form.py --print          # dump the batchUpdate payload
    python3 build_form.py --sync           # rewrite the LIVE form from this file
    python3 build_form.py --create         # make a NEW form and fill it in

`--sync` deletes every item on the live form and recreates it, so run it only
before any responses come in.

It shells out to `gws` (the Google Workspace CLI) against the Binghamton
account. `gws` handles the OAuth; if the token has expired it opens a browser.

THE UPLOAD QUESTIONS COME FROM QUIZ 4'S FORM. The Forms API answers "Creation
of file_upload question not supported", so `--create` does not build a form: it
copies Quiz 4's through Drive, which carries the two upload questions with it,
and then rewrites the title, the description and the text item. The questions
it carries are:

    Question 1   File upload, images, 1 file, 10 MB, required
    Question 2   File upload, images, 1 file, 10 MB, required

One per quiz question. The grader (adv-net-sci-ops/grading/quiz) maps each
upload question to one quiz question by this exact title, and
`gforms_download.py` names the files `q1-` and `q2-` from the number in it,
so keep "Question 1" / "Question 2".

Respondents must be signed in to a Google account, which every @binghamton.edu
student is. `--sync` wipes those two questions along with everything else, so
re-add them afterwards --- it refuses unless you also pass --force. `--info`
rewrites only the words and leaves every question alone.
"""

import argparse
import json
import os
import subprocess
import sys

GWS_CONFIG_DIR = os.path.expanduser("~/.config/gws-binghamton")

# Quiz 4's form, the one --create copies for its upload questions.
TEMPLATE_FORM_ID = "1Znenf2k9Z8EuXIgcckcGP3xiaMiC_bIsYepmzd2Njs4"

FORM_ID = "1O_sID_M5DdjbxegnPpCnQ0dZZ_FAw38SiLhpsYcZh84"

TITLE = "Quiz 5 — Cores and blocks"
DOCUMENT_TITLE = "advnetsci-quiz05-block-model"

QUIZ_PDF = "https://go.skojaku.com/quiz05"

DESCRIPTION = (
    "Advanced Network Science - Fall 2026\n\n"
    "20 minutes - 10 points - Closed notes, course assistant allowed.\n\n"
    f"The questions: {QUIZ_PDF}\n\n"
    "Write each question's answer on its own page. Photograph each page and "
    "upload it below - one photo per question. Question 2 is a derivation, so "
    "photograph the whole page and keep the algebra readable."
)


def items():
    return [
        {
            "title": "Your working file",
            "description": (
                f"The questions are in the PDF: {QUIZ_PDF}\n\n"
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


def info_requests():
    """The words only: title, description, settings, and the text item's
    description. No item is created or deleted, so the upload questions stay."""
    text = items()[0]
    return [
        {
            "updateFormInfo": {
                "info": {"title": TITLE, "description": DESCRIPTION},
                "updateMask": "title,description",
            }
        },
        payload()["requests"][1],
        {
            "updateItem": {
                "item": text,
                "location": {"index": 0},
                "updateMask": "title,description",
            }
        },
    ]


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
    copy = gws(
        "drive", "files", "copy",
        "--params", json.dumps({"fileId": TEMPLATE_FORM_ID}),
        "--json", json.dumps({"name": DOCUMENT_TITLE}),
    )
    form_id = copy["id"]
    batch_update(form_id, info_requests())
    form = gws("forms", "forms", "get", "--params", json.dumps({"formId": form_id}))
    print("form id:  ", form_id)
    print("responder:", form["responderUri"])
    print("editor:   ", f"https://docs.google.com/forms/d/{form_id}/edit")
    for it in form.get("items", []):
        print("  item:", it.get("title"))
    print()
    print("Set FORM_ID above, then point go.skojaku.com/ans-quiz05 at the")
    print("responder URL.")


def info():
    batch_update(FORM_ID, info_requests())
    print(f"rewrote the words on form {FORM_ID}; questions untouched")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print", action="store_true", dest="dump",
                        help="dump the batchUpdate payload and exit")
    parser.add_argument("--sync", action="store_true",
                        help="rewrite the live form from this file")
    parser.add_argument("--force", action="store_true",
                        help="let --sync delete the hand-made upload questions")
    parser.add_argument("--create", action="store_true",
                        help="copy Quiz 4's form into a NEW one and fill it in")
    parser.add_argument("--info", action="store_true",
                        help="rewrite the live form's words, not its questions")
    opts = parser.parse_args()
    if opts.dump:
        print(json.dumps(payload(), indent=2, ensure_ascii=False))
    elif opts.sync:
        sync(force=opts.force)
    elif opts.create:
        create()
    elif opts.info:
        info()
    else:
        parser.print_help()
        sys.exit(1)
