#!/bin/sh
# Serves the client Drive folder read-only on localhost so scripts can do HTTP range reads.
# Stop with: pkill -f "rclone serve http"
REMOTE="${LEADS_REMOTE:-clientdrive:1.2B Leads-sazag}"
exec rclone serve http "$REMOTE" --drive-shared-with-me --read-only \
  --addr 127.0.0.1:8765 --dir-cache-time 24h -v
