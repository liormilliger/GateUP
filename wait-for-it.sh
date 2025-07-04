#!/bin/sh
# wait-for-it.sh: a script to wait for a service to be available

set -e

host="$1"
shift
# FIX: The command to execute is now taken from the remaining arguments.
cmd="$@"

# Loop until we can successfully connect to the host and port
# The port '8000' is now hardcoded as it's specific to this project's dynamodb.
until nc -z "$host" 8000; do
  >&2 echo "DynamoDB is unavailable - sleeping"
  sleep 5
done

>&2 echo "DynamoDB is up - executing command"
# FIX: Use 'exec "$@"' to pass all arguments to the executed command.
exec $cmd