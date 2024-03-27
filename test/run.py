#! /usr/bin/env python3


#    renm — a bulk file renamer
#    Copyright (C) 2024 Ethan Blahay
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


from argparse import ArgumentParser
import os

def listdirRecursivePrint(dir='.', step=0):
    INIT_DIR = os.getcwd()
    os.chdir(dir)

    for f in os.listdir():
        for i in range(step):
            print('\t',end='')
        print(" - "+f)

        # chk if dir
        if os.path.isdir(f):
            listdirRecursivePrint(f, step=step+1)

    os.chdir(INIT_DIR)

def case_0(APP):
    # create & move into test dir
    dirname = "dgs_0"
    os.mkdir(dirname)
    os.chdir(dirname)

    # create test-specific files
    files = ["apple", "grape"]

    for f in files:
        a="This file was originally called " + f
        with open(f, "w") as file:
            file.write(a)

    # print info about unaltered files
    print("Dir Contents [PRE-APP]:")
    for f in os.listdir():
        print(" - "+f)

    # run app
    cmdstr=APP+" \"^apple\" orange *"
    print("Cmd String:\033[33m", cmdstr, "\033[0m")

    os.system(cmdstr)

    # display results
    print("Dir Contents [POST-APP]:")
    for f in os.listdir():
        print("==\033[1mSTART=(",f,")\033[0m==")
        with open(f, "r") as file:
            print(file.read())
        print("==\033[1mEND\033[0m==")
        

def case_1(APP):
    # create & move into test dir
    dirname = os.path.realpath("dgs_1")
    os.mkdir(dirname)
    os.chdir(dirname)

    # create test-specific files
    files = ["f-alpha", "d-0/f-beta", "d-0/d-1/f-gamma", "d-a/f-delta"]

    for f in files:
        # find any parent dirs
        d=os.path.dirname(f)

        if len(d) > 0:
            # there IS 1 or more parent directories
            os.system("mkdir -p " + d)
            os.chdir(d)
            
        # write to file
        a="This file was originally called " + os.path.basename(f)
        with open(os.path.basename(f), "w") as file:
            file.write(a)

        os.chdir(dirname)

    # print info about unaltered files
    print("Dir Contents [PRE-APP]:")
    listdirRecursivePrint()

    # run app
    cmdstr=APP+" \"a\" A f-alpha d-0/f-beta d-a d-a/f-delta"
    print("Cmd String:\033[33m", cmdstr, "\033[0m")

    os.system(cmdstr)

    # print info about altered files
    print("Dir Contents [POST-APP]:")
    listdirRecursivePrint()


# clean up temporary test files
def clean(TEST_BUILD_DIR):
    # move into right dir
    if os.getcwd() != TEST_BUILD_DIR:
        os.chdir(TEST_BUILD_DIR)

    # remove all files & dirs recursively
    os.system("rm -rf *")
    

def main():
    # set up important vars
    SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
    APP=os.path.realpath(SCRIPT_DIR+"/../build/renm")
    TEST_BUILD_DIR = SCRIPT_DIR + "/build"

    # handle argument parsing
    parser = ArgumentParser()

    parser.add_argument('run', choices=['clean', '0', '1'], help="the ID for the specific task to be run")
    parser.add_argument('--no-clean', action="store_true", help="prevents the \"clean\" step from being run")
    
    args = parser.parse_args()

    # change dir to testing dir
    os.chdir(SCRIPT_DIR)

    # move into testing build dir; mk it if it doesn't exist
    if not os.path.isdir("build"):
        os.mkdir("build")
    os.chdir("build")

    # run primary task(s)
    if args.run == 'clean':
        clean(TEST_BUILD_DIR)
        exit(0)
    elif args.run == '0':
        case_0(APP)
    elif args.run == '1':
        case_1(APP)
    else:
        print("< No Diagnostic tests were Run >")

    # clean test(s)
    if not args.no_clean:
        clean(TEST_BUILD_DIR)

    # display finished execution status
    print("\n[\033[32mDONE\033[0m]\n")


if __name__ == "__main__":
    main()