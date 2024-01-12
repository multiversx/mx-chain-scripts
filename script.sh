#!/bin/bash
set -e

#Make script aware of its location
SCRIPTPATH="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 ; pwd -P )"

source $SCRIPTPATH/config/variables.cfg
source $SCRIPTPATH/config/functions.cfg
source $SCRIPTPATH/config/menu_functions.cfg

#Check if there are newer versions of the scripts available
check_scripts_version

#See if the user has passed any command line arguments and if not show the menu
if [ $# -eq 0 ]
  then

  show_menu #Show all the menu options

  COLUMNS=18
  PS3="Please select an action:"
  options=("install" "observing_squad" "multikey_squad" "upgrade" "upgrade_multikey" "upgrade_squad" "upgrade_proxy" "remove_db" "start" "start_all" "stop" "stop_all" "cleanup" "github_pull" "add_nodes" "get_logs" "benchmark" "quit")

  select opt in "${options[@]}"
  do

  case $opt in

  'install')
    install
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'observing_squad')
    observers
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'multikey_squad')
    multikey
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'upgrade')
    #Check if running a squad
    if [ -e $CUSTOM_HOME/.squad_install ]; then 
                    SQUAD_VER=$(cat $CUSTOM_HOME/.squad_install)
                    echo -e "${RED}--> You are running in the ${CYAN}$SQUAD_VER${RED} configuration. Redirecting to the ${CYAN}upgrade_squad${RED} option instead.${NC}"
                    echo -e
                    upgrade_squad                
                else
                  upgrade    
        fi
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

'upgrade_multikey')
    upgrade_squad
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'upgrade_squad')
    upgrade_squad
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'upgrade_proxy')
    upgrade_proxy
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'remove_db')
    remove_db
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'start')
    start
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'start_all')
    start_all
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'stop')
    stop
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'stop_all')
    stop_all
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'cleanup')
    cleanup
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'github_pull')
    github_pull
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'add_nodes')
    add_node
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'get_logs')
    get_logs
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'benchmark')
    run_benchmark
    echo -e
    read -n 1 -s -r -p "  Process finished. Press any key to continue..."
    clear
    show_menu
    ;;

  'quit')
    echo -e
    echo -e "${GREEN}---> Exiting scripts menu...${NC}"
    echo -e
    break
    ;;

  esac

  done

else

case "$1" in
'install')
  install
  ;;

'observing_squad')
  observers
  ;;

'multikey_squad')
  multikey
  ;;

'upgrade')
  ##Check if running a squad
    if [ -e $CUSTOM_HOME/.squad_install ]; then 
                    SQUAD_VER=$(cat $CUSTOM_HOME/.squad_install)
                    echo -e "${RED}--> You are running in the ${CYAN}$SQUAD_VER${RED} configuration. Redirecting to the ${CYAN}upgrade_squad${RED} option instead.${NC}"
                    echo -e
                    upgrade_squad                
                else
                  upgrade    
        fi
  ;;

'upgrade_multikey')
  upgrade_squad
  ;;

'upgrade_squad')
  upgrade_squad
  ;;

'upgrade_proxy')
  upgrade_proxy
  ;;

'remove_db')
  remove_db
  ;;

'start')
  start
  ;;

'start_all')
  start_all
  ;;

'stop')
  stop
  ;;

'stop_all')
  stop_all
  ;;

'cleanup')
  cleanup
  ;;

'github_pull')
  github_pull
  ;;

'add_nodes')
  add_node
  ;;

'get_logs')
  get_logs
  ;;

'benchmark')
  run_benchmark
  ;;

'migrate')
  migrate_scripts
  ;;

esac

fi
