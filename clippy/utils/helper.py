import os
import subprocess
import pkgutil

import clippy.utils.logger as logger


def cmd_exec(str):
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
    