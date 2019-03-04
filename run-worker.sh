#!/bin/bash
# Re-run a worker instance from the worker image.
set -ex
set -euo pipefail

source defaults.sh

if [ -z "${1-}" ]; then
  echo "Usage: $0 [worker-name] [worker-password]" >&2
  echo "Try $0 exampleworker password123456" >&2
  exit 1
fi

WORKER_NAME="$1"
# TODO(edwardw): parametrize this as a script argument
WORKER_PASSWORD="password123456"

# Worker instance name
inst_name="${PROJ_PREFIX}-worker-inst-${WORKER_NAME}"

# Terminate any previous running instance.
docker rm "$inst_name" --force || true

# These are settings defined by the base buildbot image.
# Docker settings are set up for host networking by default.
# BUILDMASTER: the dns or IP address of the master to connect to
# BUILDMASTER_PORT: the port of the worker protocol
# WORKERNAME: the name of the worker as declared in the master configuration
# WORKERPASS: worker password

# TODO(edwardw): extra options for passing in settings like SSH
#~ -v "$HOME/.ssh:/home/buildbot/.ssh:ro"

docker run \
  --name "$inst_name" \
  -it \
  --network host \
  -e "BUILDMASTER=localhost" \
  -e "BUILDMASTER_PORT=${BUILDBOT_COMMS_PORT}" \
  -e "WORKERNAME=${WORKER_NAME}" \
  -e "WORKERPASS=${WORKER_PASSWORD}" \
  -d \
  "${PROJ_PREFIX}-worker"
