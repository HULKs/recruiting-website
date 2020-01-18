#!/bin/ash

set -e -u

convert_markdown2html() {
  local relative_path="$(echo $1 | cut -d'/' -f2-)"
  local markdown_path="pages/${relative_path}"
  local html_path="static/$(dirname "${relative_path}")/$(basename "${relative_path}" .md).html"

  echo "${markdown_path} -> ${html_path} ..."
  mkdir -p "$(dirname "${html_path}")"
  pandoc \
    --standalone \
    --highlight-style pandoc.theme \
    --from gfm \
    --to html5 \
    --output "${html_path}" \
    --css /style.css \
    "${markdown_path}"
}

echo

pandoc --print-highlight-style pygments > pandoc.theme
find pages -name \*.md | while read f; do convert_markdown2html $f; done

echo
