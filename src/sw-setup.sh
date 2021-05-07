#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# SETUP

# LOADERS

function load_spider_wheel_config () {
    load_spider_wheel_script_name
    load_spider_wheel_prompt_string
    load_settings_spider_wheel_default
    load_spider_wheel_logging_levels
    load_spider_wheel_cargo
    load_spider_wheel_dependencies
    load_spider_wheel_safety
}

function load_spider_wheel_dependencies () {
    load_apt_dependencies ${SW_APT_DEPENDENCIES[@]}
    load_pip3_dependencies ${SW_PIP3_DEPENDENCIES[@]}
    return $?
}

function load_spider_wheel_prompt_string () {
    load_prompt_string "$SW_PS3"
    return $?
}

function load_spider_wheel_logging_levels () {
    load_logging_levels ${SW_LOGGING_LEVELS[@]}
    return $?
}

function load_spider_wheel_safety () {
    load_safety "$SW_SAFETY"
    return $?
}

function load_spider_wheel_cargo () {
    for spider_wheel_cargo in ${!SW_CARGO[@]}; do
        load_cargo \
            "$spider_wheel_cargo" ${SW_CARGO[$spider_wheel_cargo]}
    done
    return $?
}

function load_settings_spider_wheel_default () {
    for spider_wheel_setting in ${!SW_DEFAULT[@]}; do
        load_default_setting \
            "$spider_wheel_setting" ${SW_DEFAULT[$spider_wheel_setting]}
    done
    return $?
}

function load_spider_wheel_script_name () {
    load_script_name "$SW_SCRIPT_NAME"
    return $?
}

# PROJECT SETUP

function spider_wheel_project_setup () {
    lock_and_load
    load_spider_wheel_config
    create_spider_wheel_menu_controllers
    setup_spider_wheel_menu_controllers
}

function setup_spider_wheel_menu_controllers () {
    setup_spider_wheel_dependencies
    setup_main_menu_controller
    setup_log_viewer_menu_controller
    setup_spider_wheel_menu_controller
    setup_settings_menu_controller
    done_msg "${BLUE}$SCRIPT_NAME${RESET} controller setup complete."
    return 0
}

# SETUP DEPENDENCIES

function setup_spider_wheel_dependencies () {
    apt_install_dependencies
    pip3_install_dependencies
    return $?
}

# LOG VIEWER SETUP

function setup_log_viewer_menu_controller () {
    setup_log_viewer_menu_option_display_tail
    setup_log_viewer_menu_option_display_head
    setup_log_viewer_menu_option_display_more
    setup_log_viewer_menu_option_clear_log
    setup_log_viewer_menu_option_back
    done_msg "(${CYAN}$LOGVIEWER_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_log_viewer_menu_option_clear_log () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Clear-Log' 'action_clear_log_file'
    return $?
}

function setup_log_viewer_menu_option_display_tail () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-Tail' 'action_log_view_tail'
    return $?
}

function setup_log_viewer_menu_option_display_head () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-Head' 'action_log_view_head'
    return $?
}

function setup_log_viewer_menu_option_display_more () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-More' 'action_log_view_more'
    return $?
}

function setup_log_viewer_menu_option_back () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Back' 'action_back'
    return $?
}

# SPIDER WHEEL SETUP

function setup_spider_wheel_menu_controller () {
    setup_spider_wheel_menu_option_unleash_spider
    setup_spider_wheel_menu_option_view_matched_patterns
    setup_spider_wheel_menu_option_view_saved_web_pages
    setup_spider_wheel_menu_option_clear_matched_patterns
    setup_spider_wheel_menu_option_clear_saved_web_pages
    setup_spider_wheel_menu_option_help
    setup_spider_wheel_menu_option_back
    done_msg "(${CYAN}$SPIDER_WHEEL_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_spider_wheel_menu_option_clear_matched_patterns () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "Clear-Matched-Patterns" \
        "action_clear_saved_pattern_files"
    return $?
}

function setup_spider_wheel_menu_option_clear_saved_web_pages () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "Clear-Saved-Web-Pages" \
        "action_clear_saved_web_pages"
    return $?
}

function setup_spider_wheel_menu_option_view_matched_patterns () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "View-Matched-Patterns" \
        "action_view_saved_pattern_files"
    return $?
}

function setup_spider_wheel_menu_option_view_saved_web_pages () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "View-Saved-Web-Pages" \
        "action_view_saved_web_pages"
    return $?
}

function setup_spider_wheel_menu_option_unleash_spider () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "Unleash-Spider" \
        "action_unleash_spider"
    return $?
}

function setup_spider_wheel_menu_option_help () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "Help" \
        "action_help"
    return $?
}

function setup_spider_wheel_menu_option_back () {
    setup_menu_controller_action_option \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"  "Back" \
        "action_back"
    return $?
}

# SETTINGS SETUP

function setup_settings_menu_controller () {
    setup_settings_menu_option_set_safety_on
    setup_settings_menu_option_set_safety_off
    setup_settings_menu_option_set_silent_on
    setup_settings_menu_option_set_silent_off
    setup_settings_menu_option_set_pattern_scout
    setup_settings_menu_option_set_search_pattern
    setup_settings_menu_option_set_cycle_count
    setup_settings_menu_option_set_pattern_file
    setup_settings_menu_option_set_start_url
    setup_settings_menu_option_set_restricted_domain
    setup_settings_menu_option_set_thread_count
    setup_settings_menu_option_set_browser_header
    setup_settings_menu_option_set_cycle_interval
    setup_settings_menu_option_set_save_words
    setup_settings_menu_option_set_respect_robots
    setup_settings_menu_option_set_domain_restriction
    setup_settings_menu_option_set_cache_overwrite
    setup_settings_menu_option_set_size_override
    setup_settings_menu_option_set_save_pages
    setup_settings_menu_option_set_zip_files
    setup_settings_menu_option_set_follow_links
    setup_settings_menu_option_set_log_file
    setup_settings_menu_option_set_log_lines
    setup_settings_menu_option_set_temporary_file
    setup_settings_menu_option_install_dependencies
    setup_settings_menu_option_back
    done_msg "(${CYAN}$SETTINGS_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_settings_menu_option_set_zip_files () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Zip-Files' \
        'action_set_zip_files'
    return $?
}

function setup_settings_menu_option_set_pattern_scout () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Pattern-Scout' \
        'action_set_pattern_scout'
    return $?
}

function setup_settings_menu_option_set_search_pattern () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Search-Pattern' \
        'action_set_search_pattern'
    return $?
}

function setup_settings_menu_option_set_cycle_count () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Cycle-Count' \
        'action_set_cycle_count'
    return $?
}

function setup_settings_menu_option_set_pattern_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Pattern-File' \
        'action_set_pattern_file'
    return $?
}

function setup_settings_menu_option_set_start_url () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Start-URL' \
        'action_set_start_url'
    return $?
}

function setup_settings_menu_option_set_restricted_domain () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Restricted-Domain' \
        'action_set_restricted_domain'
    return $?
}

function setup_settings_menu_option_set_thread_count () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Thread-Count' \
        'action_set_thread_count'
    return $?
}

function setup_settings_menu_option_set_browser_header () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Browser-Header' \
        'action_set_browser_header'
    return $?
}

function setup_settings_menu_option_set_cycle_interval () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Cycle-Interval' \
        'action_set_cycle_interval'
    return $?
}

function setup_settings_menu_option_set_save_words () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Save-Words' \
        'action_set_save_words'
    return $?
}

function setup_settings_menu_option_set_respect_robots () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Respect-Robots' \
        'action_set_respect_robots'
    return $?
}

function setup_settings_menu_option_set_domain_restriction () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Domain-Restriction' \
        'action_set_domain_restriction'
    return $?
}

function setup_settings_menu_option_set_cache_overwrite () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Cache-Overwrite' \
        'action_set_cache_overwrite'
    return $?
}

function setup_settings_menu_option_set_size_override () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Size-Override' \
        'action_set_size_override'
    return $?
}

function setup_settings_menu_option_set_save_pages () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Save-Pages' \
        'action_set_save_pages'
    return $?
}

function setup_settings_menu_option_set_follow_links () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Follow-Links' \
        'action_set_follow_links'
    return $?
}

function setup_settings_menu_option_set_safety_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Safety-ON' \
        'action_set_safety_on'
    return $?
}

function setup_settings_menu_option_set_safety_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Safety-OFF' \
        'action_set_safety_off'
    return $?
}

function setup_settings_menu_option_set_silent_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Silent-ON' \
        'action_set_silent_flag_on'
    return $?
}

function setup_settings_menu_option_set_silent_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Silent-OFF' \
        'action_set_silent_flag_off'
    return $?
}

function setup_settings_menu_option_set_temporary_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Temporary-File' \
        'action_set_temporary_file'
    return $?
}

function setup_settings_menu_option_set_log_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Log-File' \
        'action_set_log_file'
    return $?
}

function setup_settings_menu_option_set_log_lines () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Log-Lines' \
        'action_set_log_lines'
    return $?
}

function setup_settings_menu_option_install_dependencies () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Install-Dependencies' \
        'action_install_dependencies'
    return $?
}

function setup_settings_menu_option_back () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Back' 'action_back'
    return $?
}

# MAIN MENU SETUP

function setup_main_menu_controller() {
    setup_main_menu_option_spider_wheel
    setup_main_menu_option_self_destruct
    setup_main_menu_option_log_viewer
    setup_main_menu_option_control_panel
    setup_main_menu_option_back
    done_msg "(${CYAN}$MAIN_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_main_menu_option_log_viewer () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "Log-Viewer" \
        "$LOGVIEWER_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_control_panel () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "Control-Panel" \
        "$SETTINGS_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_back () {
    setup_menu_controller_action_option \
        "$MAIN_CONTROLLER_LABEL"  "Back" \
        'action_back'
    return $?
}

function setup_main_menu_option_spider_wheel () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "Spider-Wheel" \
        "$SPIDER_WHEEL_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_self_destruct () {
    setup_menu_controller_action_option \
        "$MAIN_CONTROLLER_LABEL"  "Self-Destruct" \
        'action_spider_wheel_self_destruct'
    return $?
}



