import subprocess
import shlex
import logging
import os

log = logging.getLogger(__name__)


def checkGtk(program_name, locale):
    """
    Starts a given program in the specified ``locale_code``.
    Checks whether given ``program_name`` is a ``GTK`` application or not.

    :param program_name: The program which is to be launched.
    :param locale: The locale in which program is to be launched.
    :type program_name: str
    :type locale: str
    :returns: ``0`` if ``program_name`` is ``GTK``
    :rtype: int
    """

    try:
        # Start the program with the given name
        command = program_name
        command = shlex.split(command)
        print command
        program = subprocess.Popen(command, env={'LANG': locale, 'DISPLAY': os.environ['DISPLAY']})
    except OSError:
        log.error("Invalid application name", exc_info=True)
        isGtk = 1
        return isGtk

    log.info("Application %s started successfully.", program_name)

    # Get the path of the executable by using pid of program.
    executable_path = subprocess.check_output(['readlink', '/proc/'+str(program.pid)+'/exe'])
    executable_path = executable_path.strip('\n')
    log.info("Executable path: %s", executable_path)

    # Check program dependencies to check whether application is Gtk.
    command = "ldd " + executable_path
    command = shlex.split(command)
    ldd = subprocess.Popen(command, stdout=subprocess.PIPE)
    isGtk = subprocess.call(('grep', 'gtk'), stdin = ldd.stdout)
    log.debug("Program GTK? command exited with %d", isGtk)

    return isGtk


def kill(app_name):
    command = "kill $(ps aux | grep '" + app_name + "' | awk '{print $2}')"
    subprocess.call(command, shell=True)
