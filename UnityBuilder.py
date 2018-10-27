import os
import sys
import threading
import time
from optparse import OptionParser
import tailer
import datetime
import subprocess


def parse_start_arguments():
    parser = OptionParser()
    parser.add_option("--unityPath", dest="UnityPath", default=True, help="Path to Unity application")
    parser.add_option("--projectPath", dest="ProjectPath", default=True, help="Path to Unity Project")
    parser.add_option("--logPath", dest="LogPath", default=True, help="Path to Unity Log File")

    (options, args) = parser.parse_args()
    return options


options = parse_start_arguments()


def start_unity_build_command():
    log("INFO", "Start Unity Build")
    try:
        subprocess.run(options.UnityPath + " -projectPath " + options.ProjectPath +
                       " -logfile " + options.LogPath +
                       " -quit "
                       "-batchmode "
                       "-nographics "
                       "-executeMethod MyEditorScript.BuildWin", check=True, shell=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


def read_log_file():
    log("INFO", "Start tailing for logfile")
    while (not os.path.exists(options.LogPath)):
        log("DEBUG", "Logfile is non existent now, retrying in 0.1s")
        time.sleep(0.1)

    log("INFO", "Tail for log file started")
    for line in tailer.follow(open(options.LogPath)):
        log("UNITY", line)


def run_headless_thread(callback):
    t = threading.Thread(target=callback)
    t.daemon = True
    t.start()
    return t


def log(level, msg):
    print(str(datetime.datetime.now()) + " [" + level + "] " + msg)


try:
    log("DEBUG", "Starting with arguments: " + str(options))
    log("INFO", "Read logfile tailing")
    logFileThread = run_headless_thread(read_log_file)

    log("INFO", "Start unity")
    start_unity_build_command()
except Exception as e:
    log("ERROR", "Failed to start a thread" + str(e))
