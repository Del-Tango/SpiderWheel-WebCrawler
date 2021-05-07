#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# DISPLAY

function display_banner_file () {
    local CLEAR_SCREEN=${1:-clear-screen-on}
    cat "${MD_DEFAULT['banner-file']}" > "${MD_DEFAULT['tmp-file']}"
    case "$CLEAR_SCREEN" in
        'clear-screen-on')
            clear
            ;;
    esac; echo "${RED} `cat ${MD_DEFAULT['tmp-file']}` ${RESET}"
    return 0
}

function display_spider_wheel_banner () {
    local CLEAR_SCREEN=${1:-clear-screen-on}
    display_banner_file "$CLEAR_SCREEN"
    display_script_banner "clear-screen-off"
    return $?
}

function display_formatted_settings () {
    display_formatted_setting_conf_file
    display_formatted_setting_log_file
    display_formatted_setting_pattern_file
    display_formatted_setting_temporary_file
    display_formatted_setting_start_url
    display_formatted_setting_search_pattern
    display_formatted_setting_restricted_domain
    display_formatted_setting_browser_header
    display_formatted_setting_log_lines
    display_formatted_setting_cycle_count
    display_formatted_setting_thread_count
    display_formatted_setting_cycle_interval
    display_formatted_setting_safety
    display_formatted_setting_silent
    display_formatted_setting_pattern_scout
    display_formatted_setting_save_words
    display_formatted_setting_respect_robots
    display_formatted_setting_domain_restriction
    display_formatted_setting_cache_overwrite
    display_formatted_setting_size_override
    display_formatted_setting_save_pages
    display_formatted_setting_zip_files
    display_formatted_setting_follow_links

    return 0
}

function display_spider_wheel_settings () {
    display_formatted_settings | column
    echo; return 0
}

# GENERAL

function display_formatted_setting_pattern_file () {
    echo "[ ${CYAN}Dump File${RESET}           ]: ${YELLOW}${MD_DEFAULT['ptn-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_temporary_file () {
    echo "[ ${CYAN}Temporary File${RESET}      ]: ${YELLOW}${MD_DEFAULT['tmp-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_conf_file () {
    echo "[ ${CYAN}Conf File${RESET}           ]: ${YELLOW}${MD_DEFAULT['conf-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_log_file () {
    echo "[ ${CYAN}Log File${RESET}            ]: ${YELLOW}${MD_DEFAULT['log-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_log_lines () {
    echo "[ ${CYAN}Log Lines${RESET}           ]: ${WHITE}${MD_DEFAULT['log-lines']:-${RED}Unspecified}${RESET} lines"
    return $?
}

function display_formatted_setting_search_pattern () {
    if [[ "${MD_DEFAULT['pattern-scout']}" == 'off' ]]; then
        return 0
    fi
    echo "[ ${CYAN}Search Pattern${RESET}      ]: ${MAGENTA}${MD_DEFAULT['search-pattern']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_start_url () {
    echo "[ ${CYAN}Target URL${RESET}          ]: ${BLUE}${MD_DEFAULT['start-url']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_restricted_domain () {
    if [[ "${MD_DEFAULT['restrict']}" == 'off' ]]; then
        return 0
    fi
    echo "[ ${CYAN}Restricted Domain${RESET}   ]: ${BLUE}${MD_DEFAULT['domain']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_browser_header () {
    echo "[ ${CYAN}Browser Header${RESET}      ]: ${MAGENTA}${MD_DEFAULT['header']:-${RED}Unspecified}${RESET} header"
    return $?
}

function display_formatted_setting_cycle_count () {
    if [ ${MD_DEFAULT['cycle-count']} -eq 0 ]; then
        local CYCLES="${RED}Endless${RESET}"
    else
        local CYCLES="${WHITE}${MD_DEFAULT['cycle-count']}${RESET}"
    fi
    echo "[ ${CYAN}Crawler Cycles${RESET}      ]: ${CYCLES:-${RED}Unspecified${RESET}} iterations"
    return $?
}

function display_formatted_setting_thread_count () {
    echo "[ ${CYAN}Crawler Threads${RESET}     ]: ${WHITE}${MD_DEFAULT['threads']:-${RED}Unspecified}${RESET} threads"
    return $?
}

function display_formatted_setting_cycle_interval () {
    if [ ${MD_DEFAULT['cycle-count']} -eq 0 ]; then
        return 0
    fi
    echo "[ ${CYAN}Cycle Interval${RESET}      ]: ${WHITE}${MD_DEFAULT['cycle-interval']:-${RED}Unspecified}${RESET} seconds"
    return $?
}

function display_formatted_setting_safety () {
    FLAG=`format_flag_colors "$MD_SAFETY"`
    echo "[ ${CYAN}Safety${RESET}              ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_silent () {
    FLAG=`format_flag_colors "${MD_DEFAULT['silent']}"`
    echo "[ ${CYAN}Silent${RESET}              ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_pattern_scout () {
    FLAG=`format_flag_colors "${MD_DEFAULT['pattern-scout']}"`
    echo "[ ${CYAN}REGEX Pattern Scout${RESET} ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_save_words () {
    FLAG=`format_flag_colors "${MD_DEFAULT['save-words']}"`
    echo "[ ${CYAN}Save Words${RESET}          ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_respect_robots () {
    FLAG=`format_flag_colors "${MD_DEFAULT['respect-robots']}"`
    echo "[ ${CYAN}Respect Robots.txt${RESET}  ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_domain_restriction () {
    FLAG=`format_flag_colors "${MD_DEFAULT['restrict']}"`
    echo "[ ${CYAN}Domain Restriction${RESET}  ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_cache_overwrite () {
    FLAG=`format_flag_colors "${MD_DEFAULT['overwrite']}"`
    echo "[ ${CYAN}Cache Overwrite${RESET}     ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_size_override () {
    FLAG=`format_flag_colors "${MD_DEFAULT['override-size']}"`
    echo "[ ${CYAN}Page Size Override${RESET}  ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_save_pages () {
    FLAG=`format_flag_colors "${MD_DEFAULT['save-pages']}"`
    echo "[ ${CYAN}Save Pages${RESET}          ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_zip_files () {
    if [[ "${MD_DEFAULT['save-pages']}" == 'off' ]]; then
        return 0
    fi
    FLAG=`format_flag_colors "${MD_DEFAULT['zip-files']}"`
    echo "[ ${CYAN}Zip Files${RESET}           ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

function display_formatted_setting_follow_links () {
    FLAG=`format_flag_colors "${MD_DEFAULT['follow-links']}"`
    echo "[ ${CYAN}Follow Links${RESET}        ]: ${FLAG:-${RED}Unspecified${RESET}}"
    return $?
}

