#!/bin/bash
curl 'https://c19.zyxw365.in/api/batch_data' 2>/dev/null | jq '.data | keys[] ' | sed -r 's<"(.+)"<cp ~/pdfs/template.html ~/pdfs/batch_\1.html<' | sh
