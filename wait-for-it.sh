#!/bin/sh
# wait-for-it.sh: a script to wait for a service to be available

set -e

host="$1"
shift
cmd="$@"

# Loop until we can successfully connect to the host and port
until nc -z "$host" 8000; do
  >&2 echo "DynamoDB is unavailable - sleeping"
  sleep 1
done

>&2 echo "DynamoDB is up - executing command"
exec $cmd