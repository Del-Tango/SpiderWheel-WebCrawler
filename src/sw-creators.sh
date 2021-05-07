#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# CREATORS

function create_spider_wheel_menu_controllers () {
    create_main_menu_controller
    create_spider_wheel_menu_controller
    create_log_viewer_menu_cotroller
    create_settings_menu_controller
    done_msg "${BLUE}$SCRIPT_NAME${RESET} controller construction complete."
    return 0
}

function create_spider_wheel_menu_controller () {
    create_menu_controller "$SPIDER_WHEEL_CONTROLLER_LABEL" \
        "${CYAN}$SPIDER_WHEEL_CONTROLLER_DESCRIPTION${RESET}" \
        "$SPIDER_WHEEL_CONTROLLER_OPTIONS"
    return $?
}

function create_main_menu_controller () {
    create_menu_controller "$MAIN_CONTROLLER_LABEL" \
        "${CYAN}$MAIN_CONTROLLER_DESCRIPTION${RESET}" "$MAIN_CONTROLLER_OPTIONS"
    return $?
}

function create_log_viewer_menu_cotroller () {
    create_menu_controller "$LOGVIEWER_CONTROLLER_LABEL" \
        "${CYAN}$LOGVIEWER_CONTROLLER_DESCRIPTION${RESET}" \
        "$LOGVIEWER_CONTROLLER_OPTIONS"
    return $?
}

function create_settings_menu_controller () {
    create_menu_controller "$SETTINGS_CONTROLLER_LABEL" \
        "${CYAN}$SETTINGS_CONTROLLER_DESCRIPTION${RESET}" \
        "$SETTINGS_CONTROLLER_OPTIONS"

    info_msg "Setting ${CYAN}$SETTINGS_CONTROLLER_LABEL${RESET} extented"\
        "banner function ${MAGENTA}display_spider_wheel_settings${RESET}..."
    set_menu_controller_extended_banner "$SETTINGS_CONTROLLER_LABEL" \
        'display_spider_wheel_settings'

    return 0
}

