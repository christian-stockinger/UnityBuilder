import subprocess
import sys
from optparse import OptionParser

from util import fileLogger
from util import logger


def parse_start_arguments():
    parser = OptionParser()
    parser.add_option("--unityPath", dest="UnityPath", default=True, help="Path to Unity application")
    parser.add_option("--projectPath", dest="ProjectPath", default=True, help="Path to Unity Project")
    parser.add_option("--logPath", dest="LogPath", default=True, help="Path to Unity Log File")
    parser.add_option("-e", "--executionMessage", dest="ExecutionMethod", default=True, help="Execution method after unit started completly")
    parser.add_option("-t", "--target", dest="Target", help="Build Target of the Build")
    parser.add_option("--noTimer", dest="NoTimer", action='store_true', help="no timestamp should be displayed")
    parser.add_option("--mac", dest="MacBuild", action='store_true', help="build unity on an mac device")

    (options, args) = parser.parse_args()
    return options


options = parse_start_arguments()
LOGGER = logger.Logger(options.NoTimer)


def start_unity_build_command():
    LOGGER.info("Start Unity Build")
    try:
        build_command = options.UnityPath + " -projectPath " + options.ProjectPath + \
                       " -logfile " + options.LogPath + \
                       " -buildTarget " + options.Target + \
                       " -quit " \
                       "-batchmode " \
                       "-nographics " \
                       "-executeMethod " + options.ExecutionMethod
        if options.MacBuild:
            subprocess.call(build_command, shell=True)
        else:
            subprocess.call(build_command)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


def cleanup_unity_process():
    try:
        LOGGER.info("Cleaning up Unity process")
        subprocess.call(r'TASKKILL /F /IM Unity.exe', stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as error:
        LOGGER.warn("Couldn't kill unity " + str(error))


try:
    LOGGER.log("DEBUG", "Starting with arguments: " + str(options))
    LOGGER.info("Read logfile tailing")
    logfile = fileLogger.ContinuousFileLogger(options.LogPath, options.NoTimer)
    logfile.start()
    LOGGER.info("Start unity")
    start_unity_build_command()
    if not options.MacBuild:
        LOGGER.info("Cleanup Processes")
        cleanup_unity_process()
    LOGGER.info("Cleanup logger")
    logfile.stop()

except Exception as e:
    LOGGER.error("Failed to start a thread" + str(e))
