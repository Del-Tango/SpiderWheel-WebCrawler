#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# FORMATTERS

function format_spider_wheel_arguments () {
    local ARGUMENTS=(
        "--log-file=${MD_DEFAULT['log-file']}"
        "--search-pattern=${MD_DEFAULT['search-pattern']}"
        "--dump-file=${MD_DEFAULT['ptn-file']}"
        "--load-url=${MD_DEFAULT['start-url']}"
        "--restricted-url=${MD_DEFAULT['domain']}"
        "--saved-dir-path=${MD_DEFAULT['pge-dir']}"
        "--header=${MD_DEFAULT['header']}"
        "--cycles=${MD_DEFAULT['cycle-count']}"
        "--thread-count=${MD_DEFAULT['threads']}"
        "--cycle-interval=${MD_DEFAULT['cycle-interval']}"
    )
    if [[ ${MD_DEFAULT['pattern-scout']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--pattern-scout' )
    fi
    if [[ ${MD_DEFAULT['save-swords']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--save-words' )
    fi
    if [[ ${MD_DEFAULT['respect-robots']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--respect-robots' )
    fi
    if [[ ${MD_DEFAULT['restrict']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--restrict' )
    fi
    if [[ ${MD_DEFAULT['overwrite']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--overwrite' )
    fi
    if [[ ${MD_DEFAULT['zip-files']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--zip-files' )
    fi
    if [[ ${MD_DEFAULT['override-size']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--override-size' )
    fi
    if [[ ${MD_DEFAULT['save-pages']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--save-pages' )
    fi
    if [[ ${MD_DEFAULT['follow-links']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--follow-links' )
    fi
    if [[ ${MD_DEFAULT['silent']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--quiet' )
    fi
    echo -n "${ARGUMENTS[@]}"
    return $?
}
