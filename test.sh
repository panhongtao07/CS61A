#!/bin/bash

_py="python"

exclude_dirs=("__pycache__" "venv")

failed=0

# Directories to run test on
dirs=()
# Add current dir if this script is run from a different directory
if [ $(cd $(dirname "${BASH_SOURCE[0]}") && pwd) != $(pwd) ]; then
    dirs+=(".")
fi
for dir in */; do
    dirs+=("${dir::-1}")
done

# Loop through each directory
for dir_name in "${dirs[@]}"; do
    # Skip excluded directories
    if [[ " ${exclude_dirs[@]} " =~ " ${dir_name} " ]]; then
        continue
    fi
    true_dir=$(cd "${dir_name}" && pwd)
    true_dir_name=$(basename "${true_dir}")
    file_name="${true_dir_name}.py"
    # Run ok autograder to follow current unlock stages if it exists
    if [ -f "${dir_name}/ok" ]; then
        echo "Running ok autograder in ${dir_name}/"
        # The auto-grader always returns 0 so we need to check the output
        # but ok don't support piped output so we need to cache it
        output=$(cd "${dir_name}" && $_py ok --local)
        grep -q "No cases failed." <<< "$output"
    elif [ -f "${dir_name}/${file_name}" ]; then
        echo "Running doctest on ${dir_name}/${file_name}"
        (cd "${dir_name}" && $_py -m doctest "${file_name}")
    else
        continue
    fi
    if [ $? -ne 0 ]; then
        echo "Failed in ${dir_name}/"
        failed=$((failed+1))
    fi
done

# Fail if any tests failed
if [ $failed -ne 0 ]; then
    echo "Failed $failed tests"
    exit 1
else
    echo "Passed all tests"
    exit 0
fi
