#!/bin/bash

_py="python"

exclude_dirs=("__pycache__" "venv")

failed=0

# Loop through each directory
for dir in */; do
    # Run doctest on the Python file in the directory
    dir_name="${dir::-1}"
    if [[ " ${exclude_dirs[@]} " =~ " ${dir_name} " ]]; then
        continue
    fi
    file_name="${dir_name}.py"
    if [ ! -f "${dir_name}/${file_name}" ]; then
        continue
    fi
    echo "Running doctest on ${dir_name}/${file_name}"
    # Update the failed count
    (
    cd "${dir_name}"
    $_py -m doctest "${file_name}"
    )
    if [ $? -ne 0 ]; then
        failed=$((failed+1))
    fi
done

# Fail if any tests failed
if [ $failed -ne 0 ]; then
    echo "Failed $failed tests"
    exit 1
fi
