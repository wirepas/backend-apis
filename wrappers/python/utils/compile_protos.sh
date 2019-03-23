#!/bin/bash
# Wirepas Oy


PKG_NAME=${1:-"wirepas_messaging"}
GENERATE_PYTHON="true"

if [ ${GENERATE_PYTHON} == "true" ]
then
    echo "compiling protos"
    python3 \
        -m grpc_tools.protoc \
        -I . \
        --python_out=. \
        --grpc_python_out=. \
        ./${PKG_NAME}/*/*.proto
    echo "done"
fi
