# MultiversX Node Deploy Scripts

## INTRODUCTION

The current scripts version aims to bring the validator experience to a higher standard.
This variant of the scripts can be used on any of the MultiversX Networks (mainnet,testnet or devnet) by setting the new `ENVIRONMENT` variable.
The `ENVIRONMENT` variable will direct the scripts to use the correct mx-chain-configs repositories (mx-chain-mainnet-config, mx-chain-testnet-config, or mx-chain-devnet-config).
Running an observing squad (4 nodes + proxy) is also supported on all MultiversX Networks.
Following a few simple steps, you can run your node(s) on the local machine.
Each node will run in background as a separate systemd unit.
A new addition to the scripts is the performance assessment tool which you can use to benchmark your machine and ensure performance is adequate.

## REQUIREMENTS

- Running Ubuntu 18.04, 20.04 & up
- Running the script requires a user (not root) with sudo priviledges (without password). Find more information here: <https://docs.multiversx.com/validators/nodes-scripts/config-scripts/#ensure-user-privileges>

## SCRIPT SETTINGS - MUST BE MODIFIED BEFORE FIRST RUN

- config/variables.cfg - used to define the environment, username, home path, validator keys location, Github OAUTH Token, extra node parameters. You will also find the possibility to activate the automatic configuration of your nodes (Name & Redundancy).
In this file, it is very important to set the `ENVIRONMENT`, `CUSTOM_HOME` and `CUSTOM_USER` variables. Whoever wants to use the keybase identity, should provide here the `IDENTITY` value as it will be written automatically by the upgrade script each time an upgrade occurs.
Additionally we strongly encourage you to generate your own Github OAUTH Token and add it to the `GITHUBTOKEN` variable inside the config/variables.cfg file

## KEY MANAGEMENT

Each machine must have its own key set(s) copied locally.
For each node the file validatorKey.pem should be placed in a zip file named 'node-0.zip', in the path previously specified in variables.cfg file (NODE_KEYS_LOCATION). Whithout this zip file, the node won't be able to start as the keygenerator no longer creates a default .pem file.
Note: "$NODE_KEYS_LOCATION" is created from "$CUSTOM_HOME" and the "VALIDATOR_KEYS" variables by default.
For running additional nodes on the same machine, simply create additional zip files incrementing the numeric value (i.e. for second node: 'node-1.zip', for third node: 'node-2.zip', etc..), containing the additional key sets.

File structure example:

    $CUSTOM_HOME/VALIDATOR_KEYS/node-0.zip
    $CUSTOM_HOME/VALIDATOR_KEYS/node-1.zip
    $CUSTOM_HOME/VALIDATOR_KEYS/node-2.zip
    ...
    $CUSTOM_HOME/VALIDATOR_KEYS/node-x.zip

If someone wishes to join the network as an observer, should run the following script for each installed node (replacing `node-0` string with `node-1`, `node-2` and so on)

```
~/elrond-utils/keygenerator
mv validatorKey.pem ~/elrond-nodes/node-0/config
```

Example of adding your validator keys to a zip file (node-0.zip):

1. Navigate to your current node install path and go into the /config folder
2. Issue the command to create your zip archive: `zip node-0.zip *.pem` (repeat for each node on that machine incrementing the value 0,1,2...x)
3. Move the zip archive to the `$CUSTOM_HOME/VALIDATOR_KEYS` folder: `mv node-0.zip $CUSTOM_HOME/VALIDATOR_KEYS/` (repeat for all nodes on that machine)

## RUNNING THE SCRIPT

    [INSTALL]
        #installs the node(s) on the local machine
        ./script.sh install 

        Running the script with the 'install' parameter will prompt for the following:
            - number of nodes to be ran on the machine
            - validator display name for each node (this will only be asked one time)

    [INSTALL OBSERVING SQUAD]    
        #installs four observing node(s) and an elrond proxy instance on the local machine
        ./script.sh observing_squad

        Running the script with the 'observing_squad' parameter will deploy four observers (one for each shard) plus an instance of the MultiversX Proxy
            - please make sure your machine is able to comfortably run in such a configuration 

    [UPGRADE]
        #upgrades the node(s) on the local machine
        ./script.sh upgrade - when running just nodes

        ./script.sh upgrade_squad - when running the observing squad configuration

        ./script.sh upgrade_proxy - whenever you need to update the MultiversX Proxy instance (in the observing squad configuration)

    [START]
        #starts the node(s) on the local machine
        ./script.sh start - allows you to either start all the nodes or select which ones to start (comma separated node ids) 

    [STOP]
        #stops the node(s) on the local machine
        ./script.sh stop  - allows you to either stop all the nodes or select which ones to stop (comma separated node ids)

    [ADD NODES]
        #allow users to add more nodes in addition to the ones already running on the local machine
        ./script.sh add_nodes

        Running the script with the 'add_nodes' parameter will deploy further nodes on your machine.
            - please take into account that additional hardware resources will be required for each new node
            - make sure you add the keys for the new node(s) inside the `$CUSTOM_HOME/VALIDATOR_KEYS` folder
            - this option is not compatible with the `observing_squad` configuration 

    [CLEANUP]
        #Removes all the node(s) files on the local machine
        ./script.sh cleanup
    
    [SCRIPTS UPDATE]
        #fetches the latest version of the scripts from github while backing up your configs
        ./script.sh github_pull

    [GET NODE LOGS]
        #creates a tar.gz file containing the node logs
        ./script.sh get_logs 

    [BENCHMARK]
        #runs the performance assessment tool and creates a CSV containing the results.
        #Caution: The benchmark process should be conducted with all nodes stopped as the results will be negatively affected by a running node
        ./script.sh benchmark 

## TERMUI NODE INFO

This version of scripts will start your nodes as separate systemd services and an additional termui binary will be build for you on each machine and placed in your $CUSTOM_HOME/elrond-utils folder.
This tool provides a console-graphical interface useful for providing node status in a user-friendly way. The binary will try to connect to the node over the rest API interface provided.
During the install process your nodes will have rest api sockets assigned to them following this pattern:

    elrond-node-0 will use localhost:8080
    elrond-node-1 will use localhost:8081
    elrond-node-2 will use localhost:8082
    ...
    elrond-node-x will use localhost:(8080+x)

You can check the status of each of your nodes in turn by going to your $CUSTOM_HOME/elrond-utils/ folder and using this command (making sure you select the proper socket for the desired node):

    ./elrond-utils/termui -address localhost:8080
     or
    ./elrond-utils/termui -address localhost:8081
    ...

## LOGVIEWER INFO

This version of scripts will start your nodes as separate systemd services and an additional logviewer binary will be build for you on each machine and placed in your $CUSTOM_HOME/elrond-utils folder.
This tool provides a way of capturing (and even storing) logger lines generated by an elrond-node instance. The binary will try to connect to the node over the rest API interface provided.
During the install process your nodes will have rest api sockets assigned to them following this pattern:

    elrond-node-0 will use localhost:8080
    elrond-node-1 will use localhost:8081
    elrond-node-2 will use localhost:8082
    ...
    elrond-node-x will use localhost:(8080+x)

You can check the status of each of your nodes in turn by going to your $CUSTOM_HOME/elrond-utils/ folder and using this command (making sure you select the proper socket for the desired node):

    ./elrond-utils/logviewer -address localhost:8080
    or
    ./elrond-utils/logviewer -address localhost:8081
    ...

If the log level is not provided, it will start with the provided pattern with which the node has been started.
There is another flag called `-log-level` that can be used to alter the logger pattern. The expected format is `MATCHING_STRING1:LOG_LEVEL1,MATCHING_STRING2:LOG_LEVEL2`
If matching string is *, it will change the log levels of all contained from all packages. Otherwise, the log level will be modified only on those loggers that will contain the matching string on any position.
For example, having the parameter `process:DEBUG` will set the DEBUG level on all loggers that will contain the "process" string in their name ("process/sync", "process/interceptors", "process" and so on).
The rules are applied in the exact order they are provided, starting from left to the right part of the string

  Example:
      `*:INFO,p2p:ERROR,*:DEBUG,data:INFO` will result in having the data package logger(s) on INFO log level and all other packages on DEBUG level

Defined logger levels are: `NONE, ERROR, WARN, INFO, DEBUG, TRACE`
TRACE will output anything,
NONE will practically silent everything. 
Whatever is in between will display the provided level + the left-most part from the afore mentioned list.

  Example:
      `INFO` log level will output all logger lines with the levels `INFO` or `WARN` or `ERROR`.

The flag for storing into a file the received logger lines is  `-log-save`
  
  Example:
          `./elrond-utils/logviewer -address localhost:8080 -level *:DEBUG,api:INFO -log-save` will start the binary that will try to connect to the locally-opened 8080 port, will set the log level
      to DEBUG for all packages except api package and will store all captured log lines in a file.

## SEEDNODE INFO

If there's ever a need to start a separate seed/boot node - there's a seednode binary available in the $CUSTOM_HOME/elrond-utils/seednode/ folder.
This binary will start a new seed node that can be used as a fallback if the primary seed nodes are experiencing issues.

  Example:
      `./seeednode --help` will display all available arguments/options
      `./seeednode` will start the seed node using the default settings: `--port 10000, --p2p-seed "seed", --log-level "*:INFO "`
      `./seeednode --port 12000` will start the seed node using the settings: `--port 12000, --p2p-seed "seed", --log-level "*:INFO "`

## NODE LOGS INFO  

As of version 1.3.4 of the scripts there is a new command for extracting and tarballing your node logs. The tar file will be stored in the $CUSTOM_HOME/elrond-logs folder and will contain a timestamp in their name.

 Command Example:
      `./script.sh get_logs`

## FINAL THOUGHTS

   KEEP CALM AND VALIDATE ON THE MULTIVERSX NETWORK!
