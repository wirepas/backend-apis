#!/usr/bin/env bash
# Copyright Wirepas Ltd 2019

set -e

WIREPAS_USER=${1:-""}

# Defaults
PKG_NAME="wirepas_messaging"
PKG_PROTO_PATH="./${PKG_NAME}"
WIREPAS_GIT=${WIREPAS_GIT:-}

# For customization
WPE_REPO_DIR=${WPE_REPO_DIR:-"wpe"}
WPE_PROTO_PATH=${WPE_PROTO_PATH:-"wirepas_positioning/proto/wpe"}
WPE_GIT_PRJ=${WPE_GIT_PRJ:-"/positioning/engine"}
WPE_GIT_BRANCH="master"

WNT_REPO_DIR=${WNT_REPO_DIR:-"wnt"}
WNT_PROTO_PATH=${WNT_PROTO_PATH:-"protos"}
WNT_GIT_PRJ=${WNT_GIT_PRJ:-"nms-backend"}
WNT_GIT_BRANCH="master"

GW_REPO_DIR=${GW_REPO_DIR:-"gateway"}
GW_PROTO_PATH=${GW_PROTO_PATH:-"../../gateway_to_backend/protocol_buffers_files"}
GW_GIT_PRJ=${GW_GIT_PRJ:-""}
GW_GIT_BRANCH=""



# copy_proto
# Copies protos from the current repository
function copy_proto
{
    REPO_DIR=${1}
    COPY_FROM=${2}

    mkdir -p ${PKG_PROTO_PATH}/${REPO_DIR} || true
    cp -v ${COPY_FROM}/*.proto ${PKG_PROTO_PATH}/${REPO_DIR}/
}


# pull_proto
# Clones and copies protos from an internal location (to be removed)
function pull_proto
{
    REPO_DIR=${1}
    PROTO_PATH=${2}
    GIT_PATH=${3}
    GIT_BRANCH=${4:-"master"}

    rm ${REPO_DIR} -fr
    git clone --single-branch -b ${GIT_BRANCH} ssh://${WIREPAS_USER}@${WIREPAS_GIT}/${GIT_PATH} ${REPO_DIR}
    cp -v ${REPO_DIR}/${PROTO_PATH}/*.proto ${PKG_PROTO_PATH}/${REPO_DIR}
    rm ${REPO_DIR} -fr
}


# fix_import_path
#
# This function adjusts the proto files to match the expected import rules
# for the python package
function fix_import_path
{
    TARGET_DIR=${1}
    echo "fixing directory ${TARGET_DIR} / ${PKG_PROTO_PATH}/${TARGET_DIR}/"

    for PROTO_FILE in ${PKG_PROTO_PATH}/${TARGET_DIR}/*.proto
    do
        # Process $i
        filename=$(basename $PROTO_FILE)


        if [ ${TARGET_DIR} == ${WPE_REPO_DIR} ]
        then
            echo "altering  WPE.${PROTO_FILE}"
            sed -i "s/wirepas_positioning\/proto/wirepas_messaging/g" ${PROTO_FILE};
            sed -i "s/com.wirepas.wpe.private/com.wirepas.proto.wpe.private/g" ${PROTO_FILE};
            sed -i "s/com.wirepas.wpe/com.wirepas.proto.wpe/g" ${PROTO_FILE};

        elif [ ${TARGET_DIR} == ${GW_REPO_DIR} ]
        then

            if [ ${filename} == "nanopb.proto" ]
            then
                echo "removing ${filename}"
                rm ${PROTO_FILE}
                continue
            fi

            echo "altering  GW.${PROTO_FILE}"
            sed -i "s/import \"/import \"${PKG_NAME}\/${GW_REPO_DIR}\//g" ${PROTO_FILE};
            sed -i "s/wirepas_messaging\/gateway\/nanopb.proto/wirepas_messaging\/nanopb\/nanopb.proto/g" ${PROTO_FILE};
            sed -i "s/wirepas.proto.gateway_api/com.wirepas.proto.gateway/g" ${PROTO_FILE};

        elif [ ${TARGET_DIR} == ${WNT_REPO_DIR} ]
        then

            if [ ${filename} == "nanopb.proto" ]
            then
                echo "removing ${filename}"
                rm ${PROTO_FILE}
                continue
            fi

            echo "altering  WNT.${PROTO_FILE}"
            sed -i "s/import \"/import \"${PKG_NAME}\/${WNT_REPO_DIR}\//g" ${PROTO_FILE};
            sed -i "s/wirepas_messaging\/wnt\/nanopb.proto/wirepas_messaging\/nanopb\/nanopb.proto/g" ${PROTO_FILE};
        fi
    done
}


function main
{

    # This block pulls protos from Wirepas private servers.
    # WPE and WNT protos will be moved to this repo and once that happens
    # this block will cease to exist.
    if [[ ! -z ${WIREPAS_USER}  && ! -z ${WIREPAS_GIT} ]]
    then
        echo "pulling wpe protos..."
        pull_proto ${WPE_REPO_DIR} ${WPE_PROTO_PATH} ${WPE_GIT_PRJ} ${WPE_GIT_BRANCH}
        fix_import_path ${WPE_REPO_DIR}

        echo "pulling wnt protos..."
        pull_proto ${WNT_REPO_DIR} ${WNT_PROTO_PATH} ${WNT_GIT_PRJ} ${WNT_GIT_BRANCH}
        fix_import_path ${WNT_REPO_DIR}
    fi

    copy_proto ${GW_REPO_DIR} ${GW_PROTO_PATH}
    fix_import_path ${GW_REPO_DIR}
}


main "${@}"
