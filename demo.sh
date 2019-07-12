#!/bin/bash

if [ -f "example/alice_prev.csv" ]; then
    echo "(bash) - FYI: You have an old report we don't need anymore. Continuing..."
    echo "(bash) - ACTION: Removing old alice_prev.csv report."
    rm 'example/alice_prev.csv'
fi

if [ -f "example/alice_today.csv" ]; then
    echo "(bash) - ACTION: Converting alice_today.csv report to be the previous alice_prev.csv report."
    mv 'example/alice_today.csv' 'example/alice_prev.csv';
fi

echo "(bash) - ACTION: Crawling site to automatically create a current report for today."
scrapy crawl ../openfindit/findfiles -a urls='http://joelcrawfordsmith.com/openassessit/demo/test-pdf-links.html' -s DEPTH_LIMIT=1 -o 'example/alice_today.csv'
echo "(bash) - ACTION: Creating unique hashes for files found in todays new alice_today.csv report."
python3 opendiffit/add_hash.py \
--input-file='example/alice_today.csv' \
--output-file='-';

if [ -f "example/alice_prev.csv" ] && [ -f "example/alice_prev.csv" ]; then
    echo "(bash) - ACTION: Comparing files and create/update diff column."
    python3 opendiffit/identify_diffs.py \
    --new='example/alice_today.csv' \
    --old='example/alice_prev.csv' \
    --diff='-';
    echo "(bash) - HUMAN: Go manually check alice_today.csv 'diff' column for NEW or UPDATED files. Test them for compliance and update the 'comply' column."
    echo "(bash) - Human: Then rerun bash.sh next time you want to check for new or modified PDF files."
else
    echo "(bash) - Human: You only have one report. We need a current and a previous to compare. Rerun this report to convert current to old."
    exit 1
fi
echo "(bash) - Done."
