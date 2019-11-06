#!/usr/bin/env bash
# Copyright Wirepas Ltd 2019

set -e

ARTIFACT_PATH=( "${@}" )

TWINE_USERNAME=${TWINE_USERNAME:-"Wirepas"}
TWINE_PASSWORD=${TWINE_PASSWORD:-${PYPI_PWD}}


function pypi_validate_package()
{
    for _file in "${ARTIFACT_PATH[@]}"
    do
        echo "checking artifact ${_file}"
        twine check "${_file}"
    done
}


function pypi_upload()
{

    for _file in "${ARTIFACT_PATH[@]}"
    do

        if [[ "${_file}" == *"linux_x86_64.whl" ]]
        then
            echo "linux platform wheel not allowed on PyPi. Skipping upload"
            continue
        fi

        echo "uploading file ${_file}"
        twine upload "${_file}" --verbose --skip-existing

    done
}


function _main()
{

    pypi_validate_package
    pypi_upload

}

_main
