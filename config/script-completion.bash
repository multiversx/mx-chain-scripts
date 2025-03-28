#!/bin/bash

# Bash completion function for script.sh
_script_sh_completion() {
    local CURRENT_TEXT SCRIPT_OPTIONS #PREVIOUS_TEXT 

    # Get the current typed text
    COMPREPLY=()
    CURRENT_TEXT="${COMP_WORDS[COMP_CWORD]}"
    #PREVIOUS_TEXT="${COMP_WORDS[COMP_CWORD-1]}" - possible future sub-commands expansion

    # Define the available options
    SCRIPT_OPTIONS="observing_squad multikey_group upgrade upgrade_multikey upgrade_squad upgrade_proxy remove_db start start_all stop stop_all cleanup github_pull add_nodes get_logs benchmark quit"

    # Generate completion suggestions
    COMPREPLY=( $(compgen -W "$SCRIPT_OPTIONS" -- "$CURRENT_TEXT") )
}

# Register the completion function
complete -F _script_sh_completion script.sh