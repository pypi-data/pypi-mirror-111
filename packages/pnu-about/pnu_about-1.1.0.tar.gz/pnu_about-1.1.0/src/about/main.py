#!/usr/bin/env python
""" about - show system information
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import getpass
import locale
import logging
import os
import platform
import re
import shutil
import socket
import string
import sys
import sysconfig
import unicodedata

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: about - show system information v1.1.0 (July 3, 2021) by Hubert Tournier $"

# Unix dependencies:
try:
    import pwd
    import grp
except ModuleNotFoundError:
    pass

# Optional dependency upon py-cpuinfo
# Use "pip install py-cpuinfo" to install
try:
    import cpuinfo
except ModuleNotFoundError:
    pass

# Default parameters. Can be superseded by command line options
parameters = {
    "Environment": False,
    "Hardware": False,
    "Operating System": False,
    "Python": False,
    "System": False,
    "User": False,
}

################################################################################
def display_help():
    """Displays usage and help"""
    print()
    print("usage: about [-d|--debug] [-h|--help|-?] [-v|--version] [-a|--all]")
    print("       [-E|--env|--environment] [-H|--hw|--hardware] [-O|--os|--operating]")
    print("       [-P|--py|--python] [-S|--sys|--system] [-U|--user] [--]")
    print("  ----------------------   ---------------------------------------------")
    print("  -a|--all                 Same as -SUHOEP")
    print("  -E|--env|--environment   Show information about the environment")
    print("  -H|--hw|--hardware       Show information about the hardware")
    print("  -O|--os|--operating      Show information about the Operating System")
    print("  -P|--py|--python         Show information about Python")
    print("  -S|--sys|--system        Show information about the system")
    print("  -U|--user                Show information about the user")
    print("  -d|--debug               Enable debug mode")
    print("  -h|--help|-?             Print usage and this help message and exit")
    print("  -v|--version             Print version and exit")
    print("  --                       Options processing terminator")
    print()


################################################################################
def process_command_line():
    """Process command line"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    try:
        # option letters followed by : expect an argument
        # same for option strings followed by =
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:],
            "adhvHOSEPU?",
            [
                "all",
                "debug",
                "env",
                "environment",
                "everything",
                "hardware",
                "help",
                "hw",
                "life",
                "operating",
                "os",
                "py",
                "python",
                "sys",
                "system",
                "universe",
                "user",
                "version",
            ],
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        display_help()
        sys.exit(1)

    for option, _ in options:

        if option in ("-a", "--all"):
            parameters["Environment"] = True
            parameters["Hardware"] = True
            parameters["Operating System"] = True
            parameters["Python"] = True
            parameters["System"] = True
            parameters["User"] = True

        elif option in ("-E", "--env", "--environment"):
            parameters["Environment"] = True

        elif option in ("-H", "--hw", "--hardware"):
            parameters["Hardware"] = True

        elif option in ("-O", "--os", "--operating"):
            parameters["Operating System"] = True

        elif option in ("-P", "--py", "--python"):
            parameters["Python"] = True

        elif option in ("-S", "--sys", "--system"):
            parameters["System"] = True

        elif option in ("-U", "--user"):
            parameters["User"] = True

        elif option in ("--life", "--universe"):
            print("42!")
            sys.exit(42)

        elif option == "--everything":
            print("Mamma mia!")
            sys.exit(88)

        elif option in ("-d", "--debug"):
            logging.disable(logging.NOTSET)

        elif option in ("-h", "--help", "-?"):
            display_help()
            sys.exit(0)

        elif option in ("-v", "--version"):
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_commandline(): parameters:")
    logging.debug(parameters)
    logging.debug("process_commandline(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def printm(first_line, results):
    """Multi-lines print"""
    print(first_line + ":")
    print(">>>>>>>>>>")
    if isinstance(results, list):
        for line in results:
            print(line)
    elif isinstance(results, dict):
        for key, value in results.items():
            print("{}={}".format(key, value))
    else:
        print(results)
    print("<<<<<<<<<<")


################################################################################
# Possible values derived from https://hg.python.org/cpython/file/3.5/Lib/platform.py
def sys_type():
    """Return (approximate) system type"""
    operating_system_type = platform.system()
    if operating_system_type in (
        "FreeBSD",
        "NetBSD",
        "OpenBSD",
        "Linux",
        "Darwin",
        "MacOS X Server",
        "Solaris",
    ):
        return "Unix"
    return operating_system_type


################################################################################
def grep(filename, pattern):
    """Search a string in a file"""
    regexp = re.compile(pattern)
    results = []
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            result = regexp.match(line)
            if result:
                results.append(line.strip())
    return results


################################################################################
def about_local_system():
    """Show information about the local system"""
    if parameters["System"]:
        print("[System]")
        if sys_type() == "Unix":
            print("os.uname().nodename={}".format(os.uname().nodename))
        hostname = socket.gethostname()
        print("socket.gethostname()={}".format(hostname))
        print("socket.getfqdn()={}".format(socket.getfqdn()))
        print(
            "socket.gethostbyname('{}')={}".format(
                hostname, socket.gethostbyname(hostname)
            )
        )
        print(
            "socket.gethostbyname_ex('{}')={}".format(
                hostname, socket.gethostbyname_ex(hostname)
            )
        )
        print()

        print("[System/Network]")
        print("socket.if_nameindex()={}".format(socket.if_nameindex()))
        print("socket.getdefaulttimeout()={}".format(socket.getdefaulttimeout()))
        print("socket.has_dualstack_ipv6()={}".format(socket.has_dualstack_ipv6()))
        print()


################################################################################
def about_user():
    """Show information about the user"""
    if parameters["User"]:
        print("[User]")
        user = getpass.getuser()
        print("getpass.getuser()={}".format(user))
        print("os.getlogin()={}".format(os.getlogin()))
        if sys_type() == "Unix":
            print('pwd.getpwnam("{}")={}'.format(user, pwd.getpwnam(user)))
            print("os.getgroups()={}".format(os.getgroups()))
            for group_id in os.getgroups():
                print("grp.getgrgid({})={}".format(group_id, grp.getgrgid(group_id)))
        elif sys_type() == "Windows":
            if os.environ["USERNAME"]:
                print('os.environ["USERNAME"]={}'.format(os.environ["USERNAME"]))
            if os.environ["USERPROFILE"]:
                print('os.environ["USERPROFILE"]={}'.format(os.environ["USERPROFILE"]))
            if os.environ["USERDOMAIN"]:
                print('os.environ["USERDOMAIN"]={}'.format(os.environ["USERDOMAIN"]))
            if os.environ["USERDOMAIN_ROAMINGPROFILE"]:
                print(
                    'os.environ["USERDOMAIN_ROAMINGPROFILE"]={}'.format(
                        os.environ["USERDOMAIN_ROAMINGPROFILE"]
                    )
                )
            if os.environ["HOME"]:
                print('os.environ["HOME"]={}'.format(os.environ["HOME"]))
            if os.environ["HOMEDRIVE"]:
                print('os.environ["HOMEDRIVE"]={}'.format(os.environ["HOMEDRIVE"]))
            if os.environ["HOMEPATH"]:
                print('os.environ["HOMEPATH"]={}'.format(os.environ["HOMEPATH"]))
        print()

        print("[User/Process]")
        if sys_type() == "Unix":
            print("os.getuid()={}".format(os.getuid()))
            print("os.getgid()={}".format(os.getgid()))
            print("os.geteuid()={}".format(os.geteuid()))
            print("os.getegid()={}".format(os.getegid()))
            print("os.getresuid()={}".format(os.getresuid()))
            print("os.getresgid()={}".format(os.getresgid()))
        print()

        print("[Process]")
        pid = os.getpid()
        print("os.getpid()={}".format(pid))
        print("os.getppid()={}".format(os.getppid()))
        if sys_type() == "Unix":
            print("os.getpgid({})={}".format(pid, os.getpgid(pid)))
            print("os.getpgrp()={}".format(os.getpgrp()))
            print(
                "os.getpriority(os.PRIO_PROCESS, 0)={}".format(
                    os.getpriority(os.PRIO_PROCESS, 0)
                )
            )
            print(
                "os.getpriority(os.PRIO_PGRP, 0)={}".format(
                    os.getpriority(os.PRIO_PGRP, 0)
                )
            )
            print(
                "os.getpriority(os.PRIO_USER, 0)={}".format(
                    os.getpriority(os.PRIO_USER, 0)
                )
            )
        print()


################################################################################
def about_hardware():
    """Show information about the hardware"""
    if parameters["Hardware"]:
        print("[Hardware]")
        if sys_type() == "Unix":
            print("os.uname().machine={}".format(os.uname().machine))
        print("platform.machine()={}".format(platform.machine()))
        print("platform.processor()={}".format(platform.processor()))
        print("os.cpu_count()={}".format(os.cpu_count()))
        print("sys.byteorder={}".format(sys.byteorder))
        if platform.system() == "FreeBSD":
            printm(
                "/var/run/dmesg.boot scan",
                grep("/var/run/dmesg.boot", "^(CPU: |FreeBSD/SMP: |real memory  =)"),
            )
        elif sys_type() == "Windows":
            if os.environ["NUMBER_OF_PROCESSORS"]:
                print(
                    'os.environ["NUMBER_OF_PROCESSORS"]={}'.format(
                        os.environ["NUMBER_OF_PROCESSORS"]
                    )
                )
            if os.environ["PROCESSOR_ARCHITECTURE"]:
                print(
                    'os.environ["PROCESSOR_ARCHITECTURE"]={}'.format(
                        os.environ["PROCESSOR_ARCHITECTURE"]
                    )
                )
            if os.environ["PROCESSOR_IDENTIFIER"]:
                print(
                    'os.environ["PROCESSOR_IDENTIFIER"]={}'.format(
                        os.environ["PROCESSOR_IDENTIFIER"]
                    )
                )
            if os.environ["PROCESSOR_LEVEL"]:
                print(
                    'os.environ["PROCESSOR_LEVEL"]={}'.format(
                        os.environ["PROCESSOR_LEVEL"]
                    )
                )
            if os.environ["PROCESSOR_REVISION"]:
                print(
                    'os.environ["PROCESSOR_REVISION"]={}'.format(
                        os.environ["PROCESSOR_REVISION"]
                    )
                )
        print()

        print("[Hardware/cpuinfo optional module]")
        try:
            for key, value in cpuinfo.get_cpu_info().items():
                print("{}: {}".format(key, value))
        except NameError:
            print("# For more detailed (and portable) CPU information do:")
            print("# pip install py-cpuinfo ; cpuinfo")
        print()

        print("[Hardware/Disk usage]")
        if sys_type() == "Unix":
            if os.path.exists("/etc/fstab"):
                with open("/etc/fstab", "r") as file:
                    for line in file.readlines():
                        line = line.strip()
                        if not line.startswith("#"):
                            fields = line.split()
                            if fields[1] != "none":
                                print(
                                    "File system={}   Mount point={}".format(
                                        fields[0], fields[1]
                                    )
                                )
                                print(
                                    '  shutil.disk_usage("{}")={}'.format(
                                        fields[1], shutil.disk_usage(fields[1])
                                    )
                                )
        elif sys_type() == "Windows":
            for letter in string.ascii_uppercase:
                drive = letter + ":\\"
                if os.path.exists(drive):
                    print(
                        '  shutil.disk_usage("{}")={}'.format(
                            drive, shutil.disk_usage(drive)
                        )
                    )
        print()


################################################################################
def about_operating_system():
    """Show information about the operating system"""
    if parameters["Operating System"]:
        print("[Operating system]")
        print("os.name={}".format(os.name))
        print("platform.system()={}".format(platform.system()))
        print("platform.release()={}".format(platform.release()))
        print("sys.platform={}".format(sys.platform))
        print("sysconfig.get_platform()={}".format(sysconfig.get_platform()))
        print("platform.platform()={}".format(platform.platform()))
        print("platform.version()={}".format(platform.version()))
        print("platform.uname()={}".format(platform.uname()))
        if sys_type() == "Unix":
            print("os.uname().sysname={}".format(os.uname().sysname))
            print("os.uname().release={}".format(os.uname().release))
            print("os.uname().version={}".format(os.uname().version))
        elif sys_type() == "Windows":
            print("sys.getwindowsversion()={}".format(sys.getwindowsversion()))
            print("platform.win32_ver()={}".format(platform.win32_ver()))
            print("platform.win32_edition()={}".format(platform.win32_edition()))
            print("platform.win32_is_iot()={}".format(platform.win32_is_iot()))
        print()

        if sys_type() == "Unix":
            print("[Operating system/Configuration]")
            for name in os.confstr_names:
                try:
                    print("os.confstr('{}')={}".format(name, os.confstr(name)))
                except OSError as error:
                    print("os.confstr('{}')={}".format(name, "Error: " + str(error)))
            for name in os.sysconf_names:
                try:
                    print("os.sysconf('{}')={}".format(name, os.sysconf(name)))
                except OSError as error:
                    print("os.sysconf('{}')={}".format(name, "Error: " + str(error)))
            print()

        print("[Operating system/Portability]")
        print("os.curdir={}".format(os.curdir))
        print("os.pardir={}".format(os.pardir))
        print("os.sep={}".format(os.sep))
        print("os.altsep={}".format(os.altsep))
        print("os.extsep={}".format(os.extsep))
        print("os.pathsep={}".format(os.pathsep))
        print("os.defpath={}".format(os.defpath))
        print("os.devnull={}".format(os.devnull))
        print("os.linesep={}".format(os.linesep))


################################################################################
def about_environment():
    """Show information about the environment"""
    if parameters["Environment"]:
        print("[Environment]")
        print("os.getcwd()={}".format(os.getcwd()))
        printm("dict(os.environ)", dict(os.environ))
        print("os.supports_bytes_environ={}".format(os.supports_bytes_environ))
        print("shutil.get_terminal_size()={}".format(shutil.get_terminal_size()))
        print("sys.prefix={}".format(sys.prefix))
        if sys_type() == "Unix":
            print("os.getloadavg()={}".format(os.getloadavg()))
        print()

        print("[Environment/Locale]")
        print("locale.getlocale()={}".format(locale.getlocale()))
        printm("locale.localeconv()", locale.localeconv())
        print()

        print("locale.getlocale(locale.LC_CTYPE)={}".format(locale.getlocale(locale.LC_CTYPE)))
        try:
            print("locale.getlocale(locale.CODESET)={}".format(locale.nl_langinfo(locale.CODESET)))
        except:
            pass
        print("locale.getdefaultlocale()={}".format(locale.getdefaultlocale()))
        print("locale.getpreferredencoding()={}".format(locale.getpreferredencoding()))
        print("locale.getlocale(locale.LC_COLLATE)={}".format(locale.getlocale(locale.LC_COLLATE)))
        try:
            print("locale.getlocale(locale.CHAR_MAX)={}".format(locale.getlocale(locale.CHAR_MAX)))
        except:
            pass
        print()

        try:
            print("locale.getlocale(locale.LC_TIME)={}".format(locale.getlocale(locale.LC_TIME)))
            print("locale.getlocale(locale.D_T_FMT)={}".format(locale.nl_langinfo(locale.D_T_FMT)))
            print("locale.getlocale(locale.D_FMT)={}".format(locale.nl_langinfo(locale.D_FMT)))
            print("locale.getlocale(locale.T_FMT)={}".format(locale.nl_langinfo(locale.T_FMT)))
            print("locale.getlocale(locale.T_FMT_AMPM)={}".format(locale.nl_langinfo(locale.T_FMT_AMPM)))
            print("locale.getlocale(locale.DAY_1)={}".format(locale.nl_langinfo(locale.DAY_1)))
            print("locale.getlocale(locale.DAY_2)={}".format(locale.nl_langinfo(locale.DAY_2)))
            print("locale.getlocale(locale.DAY_3)={}".format(locale.nl_langinfo(locale.DAY_3)))
            print("locale.getlocale(locale.DAY_4)={}".format(locale.nl_langinfo(locale.DAY_4)))
            print("locale.getlocale(locale.DAY_5)={}".format(locale.nl_langinfo(locale.DAY_5)))
            print("locale.getlocale(locale.DAY_6)={}".format(locale.nl_langinfo(locale.DAY_6)))
            print("locale.getlocale(locale.DAY_7)={}".format(locale.nl_langinfo(locale.DAY_7)))
            print("locale.getlocale(locale.ABDAY_1)={}".format(locale.nl_langinfo(locale.ABDAY_1)))
            print("locale.getlocale(locale.ABDAY_2)={}".format(locale.nl_langinfo(locale.ABDAY_2)))
            print("locale.getlocale(locale.ABDAY_3)={}".format(locale.nl_langinfo(locale.ABDAY_3)))
            print("locale.getlocale(locale.ABDAY_4)={}".format(locale.nl_langinfo(locale.ABDAY_4)))
            print("locale.getlocale(locale.ABDAY_5)={}".format(locale.nl_langinfo(locale.ABDAY_5)))
            print("locale.getlocale(locale.ABDAY_6)={}".format(locale.nl_langinfo(locale.ABDAY_6)))
            print("locale.getlocale(locale.ABDAY_7)={}".format(locale.nl_langinfo(locale.ABDAY_7)))
            print("locale.getlocale(locale.MON_1)={}".format(locale.nl_langinfo(locale.MON_1)))
            print("locale.getlocale(locale.MON_2)={}".format(locale.nl_langinfo(locale.MON_2)))
            print("locale.getlocale(locale.MON_3)={}".format(locale.nl_langinfo(locale.MON_3)))
            print("locale.getlocale(locale.MON_4)={}".format(locale.nl_langinfo(locale.MON_4)))
            print("locale.getlocale(locale.MON_5)={}".format(locale.nl_langinfo(locale.MON_5)))
            print("locale.getlocale(locale.MON_6)={}".format(locale.nl_langinfo(locale.MON_6)))
            print("locale.getlocale(locale.MON_7)={}".format(locale.nl_langinfo(locale.MON_7)))
            print("locale.getlocale(locale.MON_8)={}".format(locale.nl_langinfo(locale.MON_8)))
            print("locale.getlocale(locale.MON_9)={}".format(locale.nl_langinfo(locale.MON_9)))
            print("locale.getlocale(locale.MON_10)={}".format(locale.nl_langinfo(locale.MON_10)))
            print("locale.getlocale(locale.MON_11)={}".format(locale.nl_langinfo(locale.MON_11)))
            print("locale.getlocale(locale.MON_12)={}".format(locale.nl_langinfo(locale.MON_12)))
            print("locale.getlocale(locale.ABMON_1)={}".format(locale.nl_langinfo(locale.ABMON_1)))
            print("locale.getlocale(locale.ABMON_2)={}".format(locale.nl_langinfo(locale.ABMON_2)))
            print("locale.getlocale(locale.ABMON_3)={}".format(locale.nl_langinfo(locale.ABMON_3)))
            print("locale.getlocale(locale.ABMON_4)={}".format(locale.nl_langinfo(locale.ABMON_4)))
            print("locale.getlocale(locale.ABMON_5)={}".format(locale.nl_langinfo(locale.ABMON_5)))
            print("locale.getlocale(locale.ABMON_6)={}".format(locale.nl_langinfo(locale.ABMON_6)))
            print("locale.getlocale(locale.ABMON_7)={}".format(locale.nl_langinfo(locale.ABMON_7)))
            print("locale.getlocale(locale.ABMON_8)={}".format(locale.nl_langinfo(locale.ABMON_8)))
            print("locale.getlocale(locale.ABMON_9)={}".format(locale.nl_langinfo(locale.ABMON_9)))
            print("locale.getlocale(locale.ABMON_10)={}".format(locale.nl_langinfo(locale.ABMON_10)))
            print("locale.getlocale(locale.ABMON_11)={}".format(locale.nl_langinfo(locale.ABMON_11)))
            print("locale.getlocale(locale.ABMON_12)={}".format(locale.nl_langinfo(locale.ABMON_12)))
            print("locale.getlocale(locale.ERA)={}".format(locale.nl_langinfo(locale.ERA)))
            print("locale.getlocale(locale.ERA_D_T_FMT)={}".format(locale.nl_langinfo(locale.ERA_D_T_FMT)))
            print("locale.getlocale(locale.ERA_D_FMT)={}".format(locale.nl_langinfo(locale.ERA_D_FMT)))
            print("locale.getlocale(locale.ERA_T_FMT)={}".format(locale.nl_langinfo(locale.ERA_T_FMT)))
            print()
    
            print("locale.getlocale(locale.LC_MESSAGES)={}".format(locale.getlocale(locale.LC_MESSAGES)))
            print("locale.getlocale(locale.YESEXPR)={}".format(locale.nl_langinfo(locale.YESEXPR)))
            print("locale.getlocale(locale.NOEXPR)={}".format(locale.nl_langinfo(locale.NOEXPR)))
            print()
    
            print("locale.getlocale(locale.LC_MONETARY)={}".format(locale.getlocale(locale.LC_MONETARY)))
            print("locale.getlocale(locale.CRNCYSTR)={}".format(locale.nl_langinfo(locale.CRNCYSTR)))
            print()
    
            print("locale.getlocale(locale.LC_NUMERIC)={}".format(locale.getlocale(locale.LC_NUMERIC)))
            print("locale.getlocale(locale.RADIXCHAR)={}".format(locale.nl_langinfo(locale.RADIXCHAR)))
            print("locale.getlocale(locale.THOUSEP)={}".format(locale.nl_langinfo(locale.THOUSEP)))
            print("locale.getlocale(locale.ALT_DIGITS)={}".format(locale.nl_langinfo(locale.ALT_DIGITS)))
            print()
        except:
            pass


################################################################################
def about_python():
    """Show information about the python install"""
    if parameters["Python"]:
        print("[Python]")
        print(
            "sysconfig.get_python_version()={}".format(sysconfig.get_python_version())
        )
        if sys_type() == "Windows":
            print("sys.winver={}".format(sys.winver))
        printm("sys.version", sys.version)
        print("sys.version_info={}".format(sys.version_info))
        print("sys.hexversion={}".format(sys.hexversion))
        print("sys.implementation={}".format(sys.implementation))
        print("platform.python_build()={}".format(platform.python_build()))
        print("platform.python_branch()={}".format(platform.python_branch()))
        print(
            "platform.python_implementation()={}".format(
                platform.python_implementation()
            )
        )
        print("platform.python_revision()={}".format(platform.python_revision()))
        print("platform.python_version()={}".format(platform.python_version()))
        print(
            "platform.python_version_tuple()={}".format(platform.python_version_tuple())
        )
        printm("sys.copyright", sys.copyright)
        print()

        print("[Python/Config]")
        print("sys.executable={}".format(sys.executable))
        print("sys.flags={}".format(sys.flags))
        printm("sys.builtin_module_names", sys.builtin_module_names)
        printm("sys.modules", sys.modules)
        print("sys.path={}".format(sys.path))
        python_version = platform.python_version_tuple()
        if python_version[0] == 3 and python_version[1] >= 9:
            printm("sys.platlibdir", sys.platlibdir)  # Python 3.9+
        print("sys.getrecursionlimit()={}".format(sys.getrecursionlimit()))
        print("sys.getswitchinterval()={}".format(sys.getswitchinterval()))
        print("sys.thread_info={}".format(sys.thread_info))
        print("platform.python_compiler()={}".format(platform.python_compiler()))
        if sys_type() == "Unix":
            print("platform.libc_ver()={}".format(platform.libc_ver()))
        print("sys.api_version={}".format(sys.api_version))
        print()

        print("[Python/Math]")
        print("sys.int_info={}".format(sys.int_info))
        print("sys.maxsize={}".format(sys.maxsize))
        print("sys.float_info={}".format(sys.float_info))
        print()

        print("[Python/Unicode]")
        print("sys.getdefaultencoding()={}".format(sys.getdefaultencoding()))
        print("sys.getfilesystemencoding()={}".format(sys.getfilesystemencoding()))
        print("unicodedata.unidata_version={}".format(unicodedata.unidata_version))
        print("sys.maxunicode={}".format(sys.maxunicode))
        print()


################################################################################
def main():
    """Program's entry point"""
    program_name = os.path.basename(sys.argv[0])
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)

    process_command_line()

    if True not in parameters.values():
        logging.warning("Please select something to show:")
        display_help()
        sys.exit(0)

    about_local_system()
    about_user()
    about_hardware()
    about_operating_system()
    about_environment()
    about_python()

    sys.exit(0)


if __name__ == "__main__":
    main()
