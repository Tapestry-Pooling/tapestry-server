#!/bin/bash
cd "$HOME/covid"
cp pdf-generator/svg_draw.js ~/pdfs/
curl 'https://c19.zyxw365.in/api/debug_info' 2>/dev/null | jq -r '.matrix_labels | keys[]' | sed -r 's_(.+)_cp pdf-generator/template.html ~/pdfs/batch_\1.html_' | sh