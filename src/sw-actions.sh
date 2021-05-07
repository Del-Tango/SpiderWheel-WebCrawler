#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# ACTIONS

function action_unleash_spider () {
    ARGUMENTS=( `format_spider_wheel_arguments` )
    debug_msg "(${BLUE}$SCRIPT_NAME${RESET}) arguments"\
        "(${MAGENTA}${ARGUMENTS[@]}${RESET})"
    trap 'trap - SIGINT; echo ''[ SIGINT ]: Web Crawler Terminated.''; return 0' SIGINT
    echo; ${SW_CARGO['spider-wheel']} ${ARGUMENTS[@]}; trap - SIGINT
    return $?
}

function action_clear_saved_pattern_files () {
    echo; info_msg "You are about to remove from your system all files"\
        "containing matched patterns and words from previous crawl sessions.
        "
    fetch_ultimatum_from_user "Are you sure about this? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    FL_COUNT=`ls -1 ${MD_DEFAULT['ptn-dir']} | wc -l`
    remove_directory "${MD_DEFAULT['ptn-dir']}" &> /dev/null
    create_directory "${MD_DEFAULT['ptn-dir']}" &> /dev/null
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not clear saved pattern files."
    else
        ok_msg "Successfully cleared (${GREEN}$FL_COUNT${RESET}) saved pattern files."
    fi
    return $EXIT_CODE
}

function action_clear_saved_web_pages () {
    echo; info_msg "You are about to remove from your system all web pages"\
        "saved from previous crawl sessions.
        "
    fetch_ultimatum_from_user "Are you sure about this? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    FL_COUNT=`ls -1 ${MD_DEFAULT['pge-dir']} | wc -l`
    remove_directory "${MD_DEFAULT['pge-dir']}" &> /dev/null
    create_directory "${MD_DEFAULT['pge-dir']}" &> /dev/null
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not clear saved web pages."
    else
        ok_msg "Successfully cleared (${GREEN}$FL_COUNT${RESET}) saved web pages."
    fi
    return $EXIT_CODE
}

function action_view_saved_web_pages () {
    PAGE_FILES=( `fetch_all_directory_files "${MD_DEFAULT['pge-dir']}"` )
    FILE_NAMES=()
    for file_path in ${PAGE_FILES[@]}; do
        TRIMMED=`fetch_file_name_from_path "$file_path"`
        FILE_NAMES=( ${FILE_NAMES[@]} "$TRIMMED" )
    done
    echo; info_msg "Select the matched pattern file you want to inspect -
    "
    FILE_NAME=`fetch_selection_from_user 'WebPage' ${FILE_NAMES[@]}`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    cat -n "${MD_DEFAULT['pge-dir']}/$FILE_NAME" | more
    echo; return 0
}

function action_view_saved_pattern_files () {
    WORD_FILES=( `fetch_all_directory_files "${MD_DEFAULT['ptn-dir']}"` )
    FILE_NAMES=()
    for file_path in ${WORD_FILES[@]}; do
        TRIMMED=`fetch_file_name_from_path "$file_path"`
        FILE_NAMES=( ${FILE_NAMES[@]} "$TRIMMED" )
    done
    echo; info_msg "Select the matched pattern file you want to inspect -
    "
    FILE_NAME=`fetch_selection_from_user 'PatternFile' ${FILE_NAMES[@]}`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    cat -n "${MD_DEFAULT['ptn-dir']}/$FILE_NAME" | more
    echo; return 0
}

function action_set_zip_files () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler archive the web pages downloaded to disk? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_zip_files "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set zip files flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set zip files flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_save_words () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler save all the words from crawled web pages to disk? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_save_words "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set save words flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set save words flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_respect_robots () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler respect robots.txt? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_respect_robots "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set respect robots flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set respect robots flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_domain_restriction () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler be constrained by a domain restriction? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_domain_restriction "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set domain restriction flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set domain restriction flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_restricted_domain () {
    echo; info_msg "Type DNS domain to restrict web crawler to"\
        "or (${MAGENTA}.back${RESET})."
    DOMAIN=`fetch_data_from_user 'DNSDomain'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_restricted_domain "$DOMAIN"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set restricted DNS domain (${RED}$DOMAIN${RESET})."
    else
        ok_msg "Successfully set restricted DNS domain (${GREEN}$DOMAIN${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_cache_overwrite () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler overwrite the caches from the previous session? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_cache_overwrite "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set cache overwrite flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set cache overwrite flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_size_override () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler discard the 500 MB size limit on web pages to crawl? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_size_override "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set size override flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set size override flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_save_pages () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler save the crawled pages to disk? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_save_pages "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set save pages flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set save pages flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_follow_links () {
    echo; fetch_ultimatum_from_user \
        "Should the web crawler jump to all encountered links in the already crawled web pages? ${YELLOW}Y/N${RESET}"
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_follow_links "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set follow links flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set follow links flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_cycle_interval () {
    echo; info_msg "Type number of seconds to wait between crawler cycles"\
        "or (${MAGENTA}.back${RESET})."
    while :
    do
        CYCLE_INTERVAL=`fetch_data_from_user 'CycleInterval'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $CYCLE_INTERVAL
        if [ $? -ne 0 ]; then
            warning_msg "Cycle interval must be a number,"\
                "not (${RED}$CYCLE_INTERVAL${RESET})."
            echo; continue
        fi; break
    done
    set_cycle_interval "$CYCLE_INTERVAL"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set crawler cycle interval"\
            "(${RED}$CYCLE_INTERVAL${RESET})."
    else
        ok_msg "Successfully set crawler cycle interval"\
            "(${GREEN}$CYCLE_INTERVAL${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_browser_header () {
    echo; info_msg "Specify web browser to masquerade as or (${MAGENTA}.back${RESET}).
    "
    BROWSER=`fetch_selection_from_user 'Browser' 'Chrome' 'Firefox' 'IE' 'Edge'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 1
    fi
    set_browser_header "$BROWSER"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set browser header (${RED}$BROWSER${RESET})."
    else
        ok_msg "Successfully set browser header (${GREEN}$BROWSER${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_thread_count () {
    echo; info_msg "Type number of threads available to crawler"\
        "or (${MAGENTA}.back${RESET})."
    while :
    do
        THREAD_COUNT=`fetch_data_from_user 'CrawlerThreads'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $THREAD_COUNT
        if [ $? -ne 0 ]; then
            warning_msg "Thread count must be a number, not (${RED}$THREAD_COUNT${RESET})."
            echo; continue
        fi; break
    done
    set_thread_count "$THREAD_COUNT"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set crawler thread count (${RED}$THREAD_COUNT${RESET})."
    else
        ok_msg "Successfully set crawler thread count (${GREEN}$THREAD_COUNT${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_pattern_scout () {
    echo; PSCOUT=`fetch_ultimatum_from_user \
        "Should the web crawler scout REGEX patterns in page content? ${YELLOW}Y/N${RESET}"`
    if [ $? -ne 0 ]; then
        local FLAG='off'
    else
        local FLAG='on'
    fi
    set_pattern_scout "$FLAG"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set pattern scout flag (${RED}$FLAG${RESET})."
    else
        ok_msg "Successfully set pattern scout flag (${GREEN}$FLAG${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_start_url () {
    echo; info_msg "Type target URL or (${MAGENTA}.back${RESET})."
    TARGET=`fetch_data_from_user 'TargetURL'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_target_url "$TARGET"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set target URL (${RED}$TARGETS${RESET})."
    else
        ok_msg "Successfully set target URL (${GREEN}$TARGETS${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_cycle_count () {
    echo; info_msg "Type number of web crawler cycles"\
        "(${WHITE}0${RESET} for endless crawling) or (${MAGENTA}.back${RESET})."
    while :
    do
        CYCLE_COUNT=`fetch_data_from_user 'CrawlerCycles'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $CYCLE_COUNT
        if [ $? -ne 0 ]; then
            warning_msg "Cycle count must be a number, not (${RED}$CYCLE_COUNT${RESET})."
            echo; continue
        fi; break
    done
    set_cycle_count "$CYCLE_COUNT"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set crawler cycle count (${RED}$CYCLE_COUNT${RESET})."
    else
        ok_msg "Successfully set crawler cycle count (${GREEN}$CYCLE_COUNT${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_search_pattern () {
    echo; info_msg "Type REGEX pattern to search in web pages or (${MAGENTA}.back${RESET})."
    REGEX=`fetch_data_from_user 'REGEX'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_search_pattern "$REGEX"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set REGEX search pattern (${RED}$REGEX${RESET})."
    else
        ok_msg "Successfully set REGEX search pattern (${GREEN}$REGEX${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_pattern_file () {
    echo; info_msg "Type absolute file path or (${MAGENTA}.back${RESET})."
    while :
    do
        FILE_PATH=`fetch_data_from_user 'FilePath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_file_exists "$FILE_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "File (${RED}$FILE_PATH${RESET}) does not exists."
            echo
        fi; break
    done
    set_pattern_file "$FILE_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$FILE_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) pattern file."
    else
        ok_msg "Successfully set pattern file (${GREEN}$FILE_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_spider_wheel_self_destruct () {
    echo; info_msg "You are about to delete all (${RED}$SCRIPT_NAME${RESET})"\
        "project files from directory (${RED}$MD_DEFAULT['project-path']${RESET})."
    fetch_ultimatum_from_user "${YELLOW}Are you sure about this? Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    check_safety_on
    if [ $? -ne 0 ]; then
        echo; warning_msg "Safety is (${GREEN}ON${RESET})! Aborting self destruct sequence."
        return 0
    fi; echo
    symbol_msg "${RED}$SCRIPT_NAME${RESET}" "Initiating self destruct sequence!"
    action_self_destruct
    local EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "(${RED}$SCRIPT_NAME${RESET}) self destruct sequence failed!"
    else
        ok_msg "Destruction complete!"\
            "Project (${GREEN}$SCRIPT_NAME${RESET}) removed from system."
    fi
    return $EXIT_CODE
}


