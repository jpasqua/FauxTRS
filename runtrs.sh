#!/bin/bash

# Function to handle SIGINT
cleanup() {
    echo "Caught SIGINT, terminating both processes..."
    kill -SIGINT $led_pid
    kill $trs_pid
    wait $led_pid $trs_pid 2>/dev/null
    exit 1
}

# Trap SIGINT
trap cleanup SIGINT

# Start the background process
python FauxLEDs.py &
led_pid=$!

# Start the foreground process
./trs80gp "$@" &
trs_pid=$!

# Wait for the foreground process to complete
wait $trs_pid

# If the foreground process completes, kill the background process
kill -SIGINT $led_pid
wait $led_pid
