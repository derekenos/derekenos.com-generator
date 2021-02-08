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

# Use vlc to generate video (currently only MP4) thumbnails.
for ext in mp4; do
    echo "Generating video thumbnail images for video type: $ext"
    for f in `ls $in_dir/*.$ext`; do
        # https://wiki.videolan.org/VLC_HowTo/Make_thumbnails/
        vlc $f --rate=1 --video-filter=scene --vout=dummy --start-time=10 --stop-time=11 --scene-format=png --scene-ratio=240 --scene-prefix=snap --scene-path=$out_dir --scene-replace --quiet vlc://quit 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "Could not generate poster image for video: $f"
            exit 1
        fi
        # Rename the output file to reflect the input.
        out_f="$out_dir/`basename $f .$ext`_"$ext"_poster.png"
        mv $out_dir/snap.png $out_f
        echo "Wrote: $out_f"
    done
done
