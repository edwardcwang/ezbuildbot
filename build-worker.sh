#!/bin/bash
# Rebuild the buildbot worker image.
set -ex
set -euo pipefail

source defaults.sh

cp $(readlink -f $BUILDBOT_CONFIG) $BUILD_TEMPDIR/master.cfg
cat > $BUILD_TEMPDIR/Dockerfile.worker <<EOF
# Worker Dockerfile

FROM ${PROJ_PREFIX}-worker-base

USER root

# Make git non-interactive
RUN bash -c 'echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> /etc/ssh/ssh_config'
ENV GIT_TERMINAL_PROMPT 0

# User-provided Dockerfrag.
$(cat $BUILDBOT_WORKER_DOCKERFRAG)

# Run image (copied from parent Dockerfile)
USER buildbot
WORKDIR /buildbot

CMD ["/usr/bin/dumb-init", "twistd", "--pidfile=", "-ny", "buildbot.tac"]
EOF

cd $BUILD_TEMPDIR
docker build -t "${PROJ_PREFIX}-worker" -f Dockerfile.worker .