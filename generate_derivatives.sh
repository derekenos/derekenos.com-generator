#!/bin/bash

# Read the input dir and strip any trailing slash.
in_dir=${1%/}
if [ -z "$in_dir" ]; then
    echo "usage: $0 <input-dir> [<output-dir>]"
    exit 1
fi

# Derive the output directory.
if [ -z "$2" ]; then
    out_dir=$in_dir/derivatives
else
    # Read the output dir and strip any trailing slash.
    out_dir=${2%/}
    # If the value comprised only a trailing slash, exit.
    if [ -z "$out_dir" ]; then
        echo 'Output dir "/" not supported'
        exit 1
    fi
fi

# Create out_dir if it doesn't exist.
if [ ! -d "$out_dir" ]; then
    mkdir $out_dir
fi

# Define a helper function that prints the repr for a specified context field.
get_context_value () {
    python3.9 -c "import json; context = json.load(open('context.json', 'r', encoding='utf-8')); print(context['$1'])"
}

# Read the output formats and widths arguments from context.json.
formats=`get_context_value "prioritized_derivative_image_formats"`
widths=`get_context_value "derivative_image_widths"`

flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval \
     -b "import sys; sys.path = ['.'] + sys.path; import generate_derivatives; generate_derivatives.run('$in_dir', '$out_dir', $formats, $widths)" \
     -b "pdb.gimp_quit(1)"
