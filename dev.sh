#!/bin/bash

# Check for inotifywait.
which inotifywait 1>/dev/null
if [ $? -ne 0 ]; then
    echo This script uses 'inotifywait' to watch for local filesystem \
         changes. Please install it with: \'sudo apt install inotify-tools\'
    exit 1
fi

# Build the project and start the server as a background process.
host=0.0.0.0
port=5000
venv/bin/python3 run.py --context-file=context.json --development --serve \
    --host=$host --port=$port &
# Get the background process's PID.
server_pid=$!

# Register a CTRL-C interrupt handler.
trap ctrl_c INT

# On CTRL-C, terminate the background server process and exit.
function ctrl_c() {
    kill -SIGKILL $server_pid
    exit 0
}

function exit_if_server_down() {
    if ! ps -q $server_pid >/dev/null; then
        echo "server not running"
        exit 1
    fi
}

# Sleep and assert that server is up.
sleep 0.5
exit_if_server_down

# Rebuild on any changes outside of the site/ dir.
while true; do
    inotifywait -e modify --recursive --quiet --quiet --exclude site/ *;
    # Exit if server crashed.
    exit_if_server_down
    venv/bin/python3 run.py --context-file=context.json --development 2>&1 | tee .run.stderr
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        curl --silent -XPOST http://$host:$port/_reload
    else
        curl --silent http://$host:$port/_error --data-binary "@.run.stderr"
    fi
done
