#!/usr/bin/env python3

import os, sys
import time

from random import randint
from hashlib import md5

VERSION = 0.5
PROGRAM = __file__[2:]
RC_FILE = ".uwurc"
NO_SAVE = [
    '..',
    PROGRAM,
    RC_FILE,
    ".git/",
    ".gitignore/"
]
UWU_COLLECTION = [
    "(ᵘﻌᵘ)", "˯˽˯", "(◡ ω ◡)", "(◡ ꒳ ◡)",
    "(◡ w ◡)", "(◡ ሠ ◡)", "(˘ω˘)", "(⑅˘꒳˘)",
    "(˘ε˘)", "(˘³˘)", "(ᵕᴗ ᵕ⁎)", "( ͡U ω ͡U )",
    "(U ᵕ U❁)", "(灬´ᴗ`灬)"
]

def daemonize():
    
    with open(RC_FILE, "rt") as stream:
        values = [s.strip() for s in stream.readlines()]
    
    try:
        pid = os.fork()
        if pid > 0:
            exit(0)
    except OSError as e:
        print("error fork 1")

    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            exit(0)
    except OSError as e:
        print("error fork 2")

    values[2] = str(os.getpid())
    with open(RC_FILE, "wt") as stream:
        for value in values:
            print(value, file=stream)

    sys.stdout.flush()
    sys.stderr.flush()
    null = os.devnull
    null_in, null_out, null_err = open(null, 'r'), open(null, 'w'), open(null, 'w')
    os.dup2(null_in.fileno(), sys.stdin.fileno())
    os.dup2(null_out.fileno(), sys.stdout.fileno())
    os.dup2(null_err.fileno(), sys.stdout.fileno())


def file_hashes(directory):
    for fd in os.walk(directory):
        parent = os.path.normpath(fd[0]).split('/')[0] + '/'
        if parent not in NO_SAVE:
            for f in fd[2]:
                if f not in NO_SAVE:
                    filename = "%s%s" % (parent, f)
                    if parent == './':
                        filename = f
                    try:
                        stream = open(filename, "rb")
                        filehash = md5(stream.read()).hexdigest()
                        stream.close()
                        yield [filename, filehash]
                    except Exception as e:
                        print(dir(e))
                        print("%s no longer exists" % filename)

def copy(src, dst):

    dirs = os.path.dirname(dst)
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    with open(dst, "wb+") as remote:
        with open(src, "rb") as local:
            remote.write(local.read())

def check_for_git():

    lines = []
    if os.path.isdir(".git"):
        mode = "wt+"
        if os.path.isfile(".gitignore"):
            mode = "at+"
            with open(".gitignore", "rt") as stream:
                lines = [l.strip() for l in stream.readlines()]
        with open(".gitignore", mode) as stream:
            if PROGRAM not in lines:
                print(PROGRAM, file=stream)
            if RC_FILE not in lines:
                print(RC_FILE, file=stream)


def get_project(filepath) -> (str, str, str):

    if not os.path.isfile(filepath):
    
        check_for_git()

        try:
            os.makedirs(os.path.dirname(filepath))
        except:
            pass

        project_name = os.path.basename(os.path.realpath('.'))
        webroot = input("path/to/webroot => ")

        if webroot[-1] != '/':
            webroot += '/'

        with open(filepath, "wt+") as stream:
            print(project_name, file=stream)
            print(webroot, file=stream)
            print("0", file=stream)

        for item in file_hashes('.'):
            copy(item[0], webroot + item[0])

        return (project_name, webroot, 0)

    with open(filepath, "rt+") as stream:
        return (i.strip() for i in stream.readlines()[:3])

    return 'no name found', 'tmp-update-dir', 0


def watch_files(directory, webroot, verbosity=False):

    hashes = list(file_hashes(directory))

    while 1:
        for old, new in zip(hashes, file_hashes(directory)):
            if old != new:
                if verbosity >= 1:
                    print("[+] updated: %s" % old[0])
                if verbosity >= 2:
                    print("old: %s | new: %s" % (old[1], new[1]))
                copy(old[0], webroot + old[0]) 
        hashes = list(file_hashes(directory))
        time.sleep(0.5)


def main(args):

    verbosity = 0
    if len(args) == 2:
        verbosity = len(args[1][1:])

    project_name, webroot, pid = get_project(RC_FILE)

    if int(pid) > 0:
        print("proc id [%s] already running for %s" % (pid, project_name))
        print("  k - kill")
        print("  r - restart")
        print("  c - cancel")
        while((answer := input("[k/r/c]: ")) not in ('k', 'r', 'c')):
            print("answer should be 'k' or or 'r' or 'c'")
        
        if answer == 'k' or answer == 'r':
            os.kill(int(pid), 9) 
            with open(RC_FILE, "rt") as stream:
                values = [s.strip() for s in stream.readlines()]
            values[2] = '0'
            with open(RC_FILE, "wt") as stream:
                for value in values:
                    print(value, file=stream)
            if answer == 'k':
                print("process [%s] killed" % pid)
                exit(0)
            print("restarting...")
        
    NO_SAVE.append(webroot)

    if len(args) == 2 and args[1] == "-b":
        print("Warning: process now running in the background")
        daemonize()

    print("[*] waiting for \"%s\" files to change..." % project_name)

    watch_files('.', webroot, verbosity)


if __name__ == "__main__":
    
    argv = sys.argv

    if len(argv) == 2 and argv[1] == "-r":
        try:
            os.remove(RC_FILE)
            if os.path.exists(".gitignore"):
                with open(".gitignore", "rt") as stream:
                    lines = [l.strip() for l in stream.readlines()]
                with open(".gitignore", "wt") as stream:
                    for line in lines:
                        if not (PROGRAM in line or RC_FILE in line):
                            print(line, file=stream)
            print("project was reset")
        except:
            print("no need to reset")
        exit(0)

    uwu_end = len(UWU_COLLECTION) - 1
    print(UWU_COLLECTION[randint(0, uwu_end)])
    
    if len(argv) == 2 and argv[1] == "-h":
        print("help:")
        print("    -b to run in the background")
        print("    -h to print this screen")
        print("    -r to reset the webroot path")
        print("    -v to show which files are saved")
        print("    -vv to show hashes")
        print("    -V to print the version")
        exit(0)
    elif len(argv) == 2 and argv[1] == "-V":
        print("Update Webroot Util -- v%s" % VERSION)
        exit(0)

    try:
        main(argv)
    except KeyboardInterrupt:
        exit(0)

