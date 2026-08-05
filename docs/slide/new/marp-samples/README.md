# Network Science — Marp deck

## Files

    network-science.md      the deck (40 slides)
    network-science.css     the theme
    figures/*.svg           node-link diagrams, exported from the HTML deck

## Build

    npm i -g @marp-team/marp-cli

    marp network-science.md --theme network-science.css -o network-science.html
    marp network-science.md --theme network-science.css --pdf
    marp network-science.md --theme network-science.css --pptx

Or in VS Code with the Marp extension, add to settings.json:

    "markdown.marp.themes": ["./marp/network-science.css"]

Math is KaTeX (`math: katex` in the front matter), so `$...$` and `$$...$$` work as written.

## Design tokens

    accent          #3959A6
    accent 2        #B14434    contrast series only (power law vs Poisson, Wrong/Missing)
    accent 3        #DAB167    third series
    text            #000000
    annotation      #6b6b6b
    rule            #dddddd
    formula panel   #f7f4f1

    body            Libre Baskerville 400
    figure labels   Caveat

## Conventions used in the markdown

    <!-- _class: lead -->    title slide
    <!-- _class: part -->     part divider (with the .band header strip)
    ## Title  +  ---          content title followed by its rule
    <div class="cols">        two-column body      .cols3 for three
    <div class="formula">     tinted formula panel
    <div class="note">        gray annotation copy
    <span class="hand">       handwriting label
    <table class="steps">     labelled derivation rows
    <div class="stats">       three-up statistic row
    <!-- ... -->              speaker notes
