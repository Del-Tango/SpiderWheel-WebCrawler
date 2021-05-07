#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# SETTERS

function set_zip_files () {
    local FLAG="$1"
    MD_DEFAULT['zip-files']="$FLAG"
    return 0
}

function set_pattern_file () {
    local FILE_PATH="$1"
    MD_DEFAULT['ptn-file']="$FILE_PATH"
    return 0
}

function set_search_pattern () {
    local REGEX="$1"
    MD_DEFAULT['search-pattern']="$REGEX"
    return 0
}

function set_cycle_count () {
    local CYCLES=$1
    check_value_is_number $CYCLES
    if [ $? -ne 0 ]; then
        error_msg "Cycle count must be a number, not (${RED}$CYCLES${RESET})."
        return 1
    fi
    MD_DEFAULT['cycle-count']=$CYCLES
    return 0
}

function set_pattern_scout () {
    local FLAG="$1"
    MD_DEFAULT['pattern-scout']="$FLAG"
    return 0
}

function set_domain_restriction () {
    local FLAG="$1"
    MD_DEFAULT['restrict']="$FLAG"
    return 0
}

function set_restricted_domain () {
    local DOMAIN="$1"
    MD_DEFAULT['domain']="$DOMAIN"
    return 0
}

function set_thread_count () {
    local THREADS=$1
    check_value_is_number $THREADS
    if [ $? -ne 0 ]; then
        error_msg "Thread count must be a number, not (${RED}$THREADS${RESET})."
        return 1
    fi
    MD_DEFAULT['threads']=$THREADS
    return 0
}

function set_browser_header () {
    local HEADER="$1"
    MD_DEFAULT['header']="$HEADER"
    return 0
}

function set_cycle_interval () {
    local INTERVAL=$1
    check_value_is_number $INTERVAL
    if [ $? -ne 0 ]; then
        error_msg "Cycle interval must be a number, not (${RED}$INTERVAL${RESET})."
        return 1
    fi
    MD_DEFAULT['cycle-interval']=$INTERVAL
    return 0
}
function set_save_pages () {
    local FLAG="$1"
    MD_DEFAULT['save-pages']="$FLAG"
    return 0
}

function set_save_words () {
    local FLAG="$1"
    MD_DEFAULT['save-words']="$FLAG"
    return 0
}

function set_respect_robots () {
    local FLAG="$1"
    MD_DEFAULT['respect-robots']="$FLAG"
    return 0
}

function set_cache_overwrite () {
    local FLAG="$1"
    MD_DEFAULT['overwrite']="$FLAG"
    return 0
}

function set_size_override () {
    local FLAG="$1"
    MD_DEFAULT['override-size']="$FLAG"
    return 0
}

function set_follow_links () {
    local FLAG="$1"
    MD_DEFAULT['follow-links']="$FLAG"
    return 0
}


