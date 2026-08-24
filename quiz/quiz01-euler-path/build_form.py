#!/usr/bin/env python3
"""Build the Google Form for Quiz 1 (Euler paths).

The live form already exists --- see README.md for its id and URLs.

    python3 build_form.py --print          # dump the batchUpdate payload
    python3 build_form.py --sync           # rewrite the LIVE form's questions
    python3 build_form.py --create         # make a NEW form and fill it in

`--sync` deletes every item on the live form and recreates it from this file,
so run it only before any responses come in.

It shells out to `gws` (the Google Workspace CLI) against the Binghamton
account. `gws` handles the OAuth; if the token has expired it opens a browser.

One question cannot be made this way. The Forms API answers "Creation of
file_upload question not supported", so the photo-upload question at the end is
added by hand in the Forms editor: File upload, images and PDF, 2 files,
10 MB, required. Respondents must be signed in to a Google account, which every
@binghamton.edu student is. `--sync` never touches it, because the API cannot
see a way to recreate it --- so re-add it if a sync wipes it.
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

DESCRIPTION = (
    "Advanced Network Science - Fall 2026\n\n"
    "15 minutes - 10 points - Closed notes, work on your own.\n\n"
    "Type each graph as a list of edges, and upload a photo of your working at "
    "the end."
)


def hdr(title, desc):
    return {"title": title, "description": desc, "textItem": {}}


def para(title, desc, points, required=True):
    question = {"required": required, "textQuestion": {"paragraph": True}}
    if points is not None:
        question["grading"] = {"pointValue": points}
    item = {"title": title, "questionItem": {"question": question}}
    if desc:
        item["description"] = desc
    return item


def line(title, required=True):
    return {
        "title": title,
        "questionItem": {
            "question": {"required": required, "textQuestion": {"paragraph": False}}
        },
    }


def items():
    return [
        line("Your name"),
        hdr(
            "Question 1 - Even degrees are not enough (4 points)",
            "The graph here is undirected. The degree of a node is the number of "
            "edges touching it. An Euler path is a walk that uses every edge "
            "exactly once.\n\n"
            "Here is a tempting rule: if every node has even degree, an Euler "
            "path exists. It is false.",
        ),
        para(
            "1(a) Give a counterexample: at most 6 nodes, an even degree at every "
            "node, at least one edge at every node, and no Euler path. Name every "
            "node and give its degree.",
            "Write one edge per line, no arrows. For example:\n"
            "A - B\nB - C\nC - A\n"
            "then a line such as: degrees: A=2, B=2, C=2",
            3,
        ),
        para(
            "1(b) The tempting rule is missing one requirement. Name it, and say "
            "in one sentence why your graph violates it.",
            None,
            1,
        ),
        hdr(
            "Question 2 - Now the edges have directions (6 points)",
            "Every edge now carries an arrow, and a walk may only follow the "
            "arrow. An Euler path in a directed graph is a walk that uses every "
            "directed edge exactly once.",
        ),
        para(
            "2(a) Write the condition under which a directed graph has an Euler "
            "path.",
            "Use the words in-degree and out-degree, and do not forget the "
            "condition that has nothing to do with degrees.",
            3,
        ),
        para(
            "2(b) Give a directed graph with 4 or 5 nodes that HAS an Euler path. "
            "Say where the walk starts and where it ends.",
            "Write one edge per line, with an arrow. For example:\n"
            "A -> B\nB -> C\nC -> A\nA -> D\nstart: A\nend: D",
            2,
        ),
        para(
            "2(c) Give a directed graph with 4 or 5 nodes that has NO Euler path. "
            "Name the node or nodes that break your condition, and give their "
            "in-degree and out-degree.",
            "Same edge-list format as 2(b), then your explanation underneath.",
            1,
        ),
        hdr(
            "Your working",
            "Photograph what you wrote and upload it. Keep the drawings large and "
            "the labels readable.",
        ),
        para(
            "Bonus (ungraded). What is the smallest number of edges you can add to "
            "your Question 1 graph so that an Euler path appears?",
            None,
            None,
            required=False,
        ),
    ]


def create_requests(start_index=0):
    return [
        {"createItem": {"item": item, "location": {"index": start_index + i}}}
        for i, item in enumerate(items())
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
                "updateSettings": {
                    "settings": {
                        "quizSettings": {"isQuiz": True},
                        "emailCollectionType": "VERIFIED",
                    },
                    "updateMask": "quizSettings.isQuiz,emailCollectionType",
                }
            },
            *create_requests(),
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
    print("re-add the file-upload question by hand if the sync removed it")


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
                        help="rewrite the live form's questions from this file")
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
