#!/bin/bash

# Read the input dir and strip any trailing slash.
in_dir=${1%/}
if [ -z "$in_dir" ]; then
    echo "usage: $0 <input-dir> [<output-dir>]"
    exit 1
fi

# Derive the output directory.
if [ -z "$2" ]; then
    out_dir=$in_dir/thumbs
else
    # Read the output dir and strip any trailing slash.
    out_dir=${2%/}
    # If the value comprised only a trailing slash, exit.
    if [ -z "$out_dir" ]; then
        echo 'Output dir "/" not supported'
        exit 1
    fi
fi

flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval \
     -b "import sys; sys.path = ['.'] + sys.path; import generate_derivatives; generate_derivatives.run('$in_dir', '$out_dir')" \
     -b "pdb.gimp_quit(1)"
