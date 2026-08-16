--[[
  fold-static-code.lua
  --------------------
  Make code fold on a site whose code never executes.

  Quarto's own `code-fold: true` is a no-op here. Its filter
  (share/filters/main.lua, render_folded_block) begins with

      if (not block.attr.classes:includes("cell-code") or ...) then
        return block, false
      end

  and only an execution engine ever adds `cell-code`. This project sets
  `execute: enabled: false`, so every fence arrives as a plain CodeBlock and
  Quarto walks straight past it.

  This filter wraps those plain fences in the same <details> shape Quarto
  would have produced, so the reader sees prose and clicks to reveal code.

  Behaviour
    * skips blocks already carrying `cell-code` (Quarto folded them already —
      never double-wrap)
    * skips blocks carrying `no-fold`
    * skips blocks with no language class (bare ``` fences are output, not code)
    * skips diagram languages Quarto renders into figures
    * the summary text comes from a per-language map, default "Show the code"
    * `fold-open` on a fence starts it expanded

  Registered under the top-level `filters:` key in _quarto.yml at
  `at: post-quarto`, i.e. after Quarto has turned {dot} blocks into SVG and
  after its own fold pass has run.
]]

local summaries = {
  python     = "Show the Python",
  py         = "Show the Python",
  bash       = "Show the commands",
  sh         = "Show the commands",
  shell      = "Show the commands",
  zsh        = "Show the commands",
  console    = "Show the commands",
  powershell = "Show the commands",
  dot        = "Show the graph source",
  graphviz   = "Show the graph source",
  r          = "Show the R",
  julia      = "Show the Julia",
  yaml       = "Show the configuration",
  yml        = "Show the configuration",
  json       = "Show the data",
  toml       = "Show the configuration",
  latex      = "Show the LaTeX",
  tex        = "Show the LaTeX",
  html       = "Show the markup",
  css        = "Show the styles",
  scss       = "Show the styles",
  javascript = "Show the JavaScript",
  js         = "Show the JavaScript",
}

local DEFAULT_SUMMARY = "Show the code"

-- Languages Quarto turns into pictures. If one still reaches us as a code
-- block, leaving it alone is the safe move.
local rendered_diagrams = {
  mermaid = true,
  ojs     = true,
  observable = true,
}

-- Classes that mean "this is output / plain text", not source.
local not_source = {
  output  = true,
  text    = true,
  plain   = true,
  default = true,
  ["cell-output"] = true,
}

local function has_class(el, name)
  for _, c in ipairs(el.attr.classes) do
    if c == name then return true end
  end
  return false
end

--- First class that looks like a language.
local function language_of(el)
  for _, c in ipairs(el.attr.classes) do
    if c ~= "sourceCode" and c ~= "numberLines" and c ~= "code-with-copy" then
      return c
    end
  end
  return nil
end

local function escape_html(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"))
end

function CodeBlock(el)
  -- Never double-wrap what Quarto already handled.
  if has_class(el, "cell-code") then return nil end
  if has_class(el, "no-fold") then return nil end

  local lang = language_of(el)
  if lang == nil then return nil end            -- bare fence: output, not code
  if rendered_diagrams[lang] then return nil end
  if not_source[lang] then return nil end

  local summary = el.attributes["code-summary"]
               or summaries[string.lower(lang)]
               or DEFAULT_SUMMARY

  local open = has_class(el, "fold-open") and " open" or ""

  return {
    pandoc.RawBlock("html",
      '<details' .. open .. ' class="qfold">\n<summary>'
      .. escape_html(summary) .. '</summary>'),
    el,
    pandoc.RawBlock("html", "</details>"),
  }
end

return {
  { CodeBlock = CodeBlock },
}
