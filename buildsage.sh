#!/bin/bash

# Find all .sage files excluding "old_code" and "tests" directories
find . -name "*.sage" \
  -not -path "./old_code/*" \
  -not -path "./tests/*" | while read -r sage_file; do

    echo "Processing $sage_file"

    # Run sage --preparse on the file
    sage --preparse "$sage_file"

    # Construct the expected output filename
    py_file="${sage_file}.py"

    # Construct the desired target filename (same path but .py extension)
    target_file="${sage_file%.sage}.py"

    # Move the .sage.py to .py
    mv "$py_file" "$target_file"
done
