import stat

METACHAIN_ID = 4294967295
NODE_PROCESS_ULIMIT = 1024 * 512
NODE_MONITORING_PERIOD = 5
NODE_RETURN_CODE_SUCCESS = 0
TEMPORARY_DIRECTORIES_PREFIX = "mx_chain_scripts_multistage_"

# Read, write and execute by owner, read and execute by group and others
FILE_MODE_NICE = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
