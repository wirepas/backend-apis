#!/usr/bin/env bash


TEMPLATE=${1:-".ci/settings-template.yml"}
OUTPUT=${2:-".settings.yml"}

# create_settings
#
# copies and fills in the template
# shellcheck disable=SC1090
function create_settings
{
    local _TEMPLATE
    local _OUTPUT

    # input name is basename
    _TEMPLATE=${1:-".ci/settings-template.yml"}
    _OUTPUT=${2:-".settings.yml"}

    rm -f "${_OUTPUT}" "${_OUTPUT}.tmp"
    ( echo "cat <<EOF >${_OUTPUT}" && \
      cat "${_TEMPLATE}" && \
      echo "EOF" \
    ) > "${_OUTPUT}.tmp"
    . "${_OUTPUT}.tmp"
    rm "${_OUTPUT}.tmp"
}

create_settings "${TEMPLATE}" "${OUTPUT}"
