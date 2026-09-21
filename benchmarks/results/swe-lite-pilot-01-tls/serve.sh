#!/bin/bash
set -eu
gunicorn -b 0.0.0.0:80 httpbin:app -k gevent &
http_pid=$!
gunicorn -b 0.0.0.0:443 httpbin:app -k gevent --certfile /fixture/server.pem --keyfile /fixture/server.key &
https_pid=$!
trap 'kill "$http_pid" "$https_pid" 2>/dev/null || true; wait || true' EXIT TERM INT
wait -n "$http_pid" "$https_pid"
