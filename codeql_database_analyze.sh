#!/bin/bash
DATABASE="$1"
OUTPUT="$2"
codeql database analyze "$DATABASE" --format=sarif-latest --output="$OUTPUT"