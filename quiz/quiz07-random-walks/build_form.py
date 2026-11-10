#!/usr/bin/env python3
"""Build the Google Form for Quiz 7 (opinions on a network, a knight on a chessboard).

The form is a drop box, not a copy of the quiz. The questions are on the printed
sheet (`quiz07.pdf`); all the form does is take one photo of the student's
handwritten answer to each question. Nothing to keep in sync with the sheet.

    python3 build_form.py --print          # dump the batchUpdate payload
    python3 build_form.py --create         # make a NEW form and fill it in
    python3 build_form.py --info           # rewrite the LIVE form's words only

It shells out to `gws` (the Google Workspace CLI) against the Binghamton
account, and pins the file keyring backend: gws deletes credentials it cannot
decrypt, so a call on the wrong backend would wipe the auth.

THE UPLOAD QUESTIONS COME FROM QUIZ 4'S FORM. The Forms API answers "Creation
of file_upload question not supported", so `--create` does not build a form: it
copies Quiz 4's through Drive, which carries its two upload questions with it,
and rewrites the title, the description and the text item. What is kept:

    Question 1   File upload, images, 1 file, 10 MB, required
    Question 2   File upload, images, 1 file, 10 MB, required

The grader (adv-net-sci-ops/grading/quiz) maps each upload question to a quiz
question by this exact title, and `gforms_download.py` names the files `q1-` and
`q2-` from the number in it, so keep "Question 1" and "Question 2".

Respondents must be signed in to a Google account, which every @binghamton.edu
student is.
"""

import argparse
import json
import os
import subprocess
import sys

GWS_CONFIG_DIR = os.path.expanduser("~/.config/gws-binghamton")

# Quiz 4's form, the one --create copies for its upload questions.
TEMPLATE_FORM_ID = "1Znenf2k9Z8EuXIgcckcGP3xiaMiC_bIsYepmzd2Njs4"

# The live form, made by --create.
FORM_ID = "1s7IdJBaZ5Vxjt2bxrJUJ4we7F-_q3nq9DyKP18TjjFc"

TITLE = "Quiz 7 — Opinions and a knight"
DOCUMENT_TITLE = "advnetsci-quiz07-random-walks"

DESCRIPTION = (
    "Advanced Network Science - Fall 2026\n\n"
    "20 minutes - 10 points - Closed notes.\n\n"
    "The questions are on the printed sheet. Write each question's answer on its "
    "own page. Photograph each page and upload it below - one photo per question."
)


def items():
    return [
        {
            "title": "Your working files",
            "description": "One photo per question, in the two boxes below.",
            "textItem": {},
        },
    ]


def settings_request():
    # Not a quiz in the Forms sense: nothing here is auto-scored, and quiz mode
    # would hand students a "view score" page. Email is VERIFIED so each photo
    # maps to an @binghamton.edu address.
    return {
        "updateSettings": {
            "settings": {
                "quizSettings": {"isQuiz": False},
                "emailCollectionType": "VERIFIED",
            },
            "updateMask": "quizSettings.isQuiz,emailCollectionType",
        }
    }


def info_requests():
    """The words only: title, description, settings, and the text item's
    description. No item is created or deleted."""
    return [
        {
            "updateFormInfo": {
                "info": {"title": TITLE, "description": DESCRIPTION},
                "updateMask": "title,description",
            }
        },
        settings_request(),
        {
            "updateItem": {
                "item": items()[0],
                "location": {"index": 0},
                "updateMask": "title,description",
            }
        },
    ]


def gws(*args):
    env = dict(
        os.environ,
        GOOGLE_WORKSPACE_CLI_CONFIG_DIR=GWS_CONFIG_DIR,
        GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND="file",
    )
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


def is_upload(item):
    question = (item.get("questionItem") or {}).get("question") or {}
    return "fileUploadQuestion" in question


def create():
    copy = gws(
        "drive", "files", "copy",
        "--params", json.dumps({"fileId": TEMPLATE_FORM_ID}),
        "--json", json.dumps({"name": DOCUMENT_TITLE}),
    )
    form_id = copy["id"]
    form = gws("forms", "forms", "get", "--params", json.dumps({"formId": form_id}))
    upload_at = [i for i, it in enumerate(form.get("items", [])) if is_upload(it)]
    if len(upload_at) != 2:
        sys.exit(f"expected 2 upload questions in the copy, found {len(upload_at)}")
    batch_update(form_id, info_requests())
    # A Drive copy comes out unpublished: the responder URL answers 401 until
    # the form is published and accepting responses.
    gws(
        "forms", "forms", "setPublishSettings",
        "--params", json.dumps({"formId": form_id}),
        "--json", json.dumps({"publishSettings": {"publishState": {
            "isPublished": True, "isAcceptingResponses": True}}}),
    )
    form = gws("forms", "forms", "get", "--params", json.dumps({"formId": form_id}))
    print("form id:  ", form_id)
    print("responder:", form["responderUri"])
    print("editor:   ", f"https://docs.google.com/forms/d/{form_id}/edit")
    for it in form.get("items", []):
        kind = "upload" if is_upload(it) else "text"
        print(f"  item: {it.get('title')!r} ({kind})")
    print()
    print("Set FORM_ID above, then point go.skojaku.com/ans-quiz07 at the")
    print("responder URL.")


def info():
    if not FORM_ID:
        sys.exit("FORM_ID is empty: run --create and set it first")
    batch_update(FORM_ID, info_requests())
    print(f"rewrote the words on form {FORM_ID}; questions untouched")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print", action="store_true", dest="dump",
                        help="dump the words-only batchUpdate payload and exit")
    parser.add_argument("--create", action="store_true",
                        help="copy Quiz 4's form into a NEW one and fill it in")
    parser.add_argument("--info", action="store_true",
                        help="rewrite the live form's words, not its questions")
    opts = parser.parse_args()
    if opts.dump:
        print(json.dumps({"requests": info_requests()}, indent=2, ensure_ascii=False))
    elif opts.create:
        create()
    elif opts.info:
        info()
    else:
        parser.print_help()
        sys.exit(1)
