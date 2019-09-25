#!/usr/bin/env bash
# Copyright Wirepas Ltd 2019

set -e

# Defaults
PKG_NAME="wirepas_messaging"
PKG_PROTO_PATH="./${PKG_NAME}"

# For customization
WPE_REPO_DIR=${WPE_REPO_DIR:-"wpe"}
WPE_PROTO_PATH=${WPE_PROTO_PATH:-"../../wpe/protocol_buffers_files"}

WNT_REPO_DIR=${WNT_REPO_DIR:-"wnt"}
WNT_PROTO_PATH=${WNT_PROTO_PATH:-"../../wnt/protocol_buffers_files"}

GW_REPO_DIR=${GW_REPO_DIR:-"gateway"}
GW_PROTO_PATH=${GW_PROTO_PATH:-"../../gateway_to_backend/protocol_buffers_files"}

# copy_proto
# Copies protos from the current repository
function copy_proto
{
    REPO_DIR=${1}
    COPY_FROM=${2}

    mkdir -p "${PKG_PROTO_PATH}/${REPO_DIR}" || true
    cp -v "${COPY_FROM}"/*.proto "${PKG_PROTO_PATH}/${REPO_DIR}/"
}


# fix_import_path
#
# This function adjusts the proto files to match the expected import rules
# for the python package
function fix_import_path
{
    local TARGET_DIR
    local _PROTO_FILE
    local _FILENAME

    TARGET_DIR=${1}
    echo "fixing directory ${TARGET_DIR} / ${PKG_PROTO_PATH}/${TARGET_DIR}/"

    for _PROTO_FILE in "${PKG_PROTO_PATH}/${TARGET_DIR}"/*.proto
    do
        # Process $i
        _FILENAME=$(basename "${_PROTO_FILE}")


        if [[ "${TARGET_DIR}" == "${WPE_REPO_DIR}" ]]
        then
            echo "altering  WPE.${_PROTO_FILE}"
            sed -i "s#wirepas_positioning/proto#wirepas_messaging#g" "${_PROTO_FILE}"
            sed -i "s#com.wirepas.wpe.private#com.wirepas.proto.wpe.private#g" "${_PROTO_FILE}"
            sed -i "s#com.wirepas.wpe#com.wirepas.proto.wpe#g" "${_PROTO_FILE}"

        elif [[ "${TARGET_DIR}" == "${GW_REPO_DIR}" ]]
        then

            if [[ "${_FILENAME}" == "nanopb.proto" ]]
            then
                echo "removing ${_FILENAME}"
                rm "${_PROTO_FILE}"
                continue
            fi

            echo "altering  GW.${_PROTO_FILE}"
            sed -i "s#import \"#import \"${PKG_NAME}/${GW_REPO_DIR}/#g" "${_PROTO_FILE}"
            sed -i "s#wirepas_messaging/gateway/nanopb.proto#wirepas_messaging/nanopb/nanopb.proto#g" "${_PROTO_FILE}"
            sed -i "s#wirepas.proto.gateway_api#com.wirepas.proto.gateway#g" "${_PROTO_FILE}"

        elif [ "${TARGET_DIR}" == "${WNT_REPO_DIR}" ]
        then

            if [ "${_FILENAME}" == "nanopb.proto" ]
            then
                echo "removing ${_FILENAME}"
                rm "${_PROTO_FILE}"
                continue
            fi

            echo "altering  WNT.${_PROTO_FILE}"
            sed -i "s#import \"#import \"${PKG_NAME}/${WNT_REPO_DIR}/#g" "${_PROTO_FILE}"
            sed -i "s#wirepas_messaging/wnt/nanopb.proto#wirepas_messaging/nanopb/nanopb.proto#g" "${_PROTO_FILE}"
        fi
    done
}


function main
{

    copy_proto "${WPE_REPO_DIR}" "${WPE_PROTO_PATH}"
    fix_import_path "${WPE_REPO_DIR}"

    copy_proto "${WNT_REPO_DIR}" "${WNT_PROTO_PATH}"
    fix_import_path "${WNT_REPO_DIR}"

    copy_proto "${GW_REPO_DIR}" "${GW_PROTO_PATH}"
    fix_import_path "${GW_REPO_DIR}"
}


main "${@}"
