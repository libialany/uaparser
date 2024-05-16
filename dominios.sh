#!/bin/sh
echo "Content-Type: text/plain"
echo

# Cache file path
CACHE_FILE="/tmp/tcpdump_cache"

# Check if the cache file exists and is less than 5 seconds old
if [ -f "$CACHE_FILE" ] && [ $(( $(date +%s) - $(stat -c %Y "$CACHE_FILE") )) -lt 5 ]; then
    # Use cached results
    cat "$CACHE_FILE"
else
    # Run tcpdump and cache the results
    touch "$CACHE_FILE"
    (tcpdump -nttttt -r /tmp/adblock-Report/adb_report.pcap0 2>/dev/null | sh /root/detect.sh | sort -n | uniq > "$CACHE_FILE") &
    cat "$CACHE_FILE"
fi
