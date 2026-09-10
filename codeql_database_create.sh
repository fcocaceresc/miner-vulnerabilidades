#!/bin/bash
DATABASE="$1"
LANGUAGE="$2"
SOURCE_ROOT="$3"
codeql database create "$DATABASE" --language="$LANGUAGE" --source-root="$SOURCE_ROOT"