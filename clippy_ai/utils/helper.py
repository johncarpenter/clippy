import os
import subprocess
import pkgutil

import clippy_ai.utils.logger as logger


def cmd_exec(str):
    # Check for potentially destructive commands
    dangerous_commands = ['rm -rf', 'sudo rm', 'mkfs', 'dd', 'shutdown', 'reboot', '> /', 'chmod -R 777']
    for cmd in dangerous_commands:
        if cmd in str.lower():
            logger.log_r("ERROR: Potentially destructive command detected: " + cmd)
            logger.log_r("This command could cause system damage and has been blocked")
            exit(1)
    logger.debug("\n------------------------ Executing Command: Start ------------------------")
    logger.debug("\n$>>" + str)    
    output = os.popen(str).read().strip()
    logger.debug("\n$>>" + output)
    logger.debug("\n------------------------ Executing Command: END ------------------------")
    return output


def join_me(stringList):
    return "".join(string for string in stringList)


def running_cmd(cmd):
    logger.log_c("Running command: " , cmd)
    subprocess.call(cmd.split(" "))


def load_file(file):
    logger.debug("Loading file : " + file)
    if not os.path.exists(file):
        logger.log_r("File not found : " + file)
        exit()
        
    with open(file, 'r') as f:
        return f.read()
    