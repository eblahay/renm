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

def test_0(APP):
    # create & move into test dir
    os.mkdir("test-0")
    os.chdir("test-0")

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
        


def main():
    # set up important vars
    SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
    APP=os.path.realpath(SCRIPT_DIR+"/../build/renm")

    # handle argument parsing
    parser = ArgumentParser()

    parser.add_argument('test-id', type=str, help="the ID for the specific test to be run")
    
    args = parser.parse_args()

    # change dir to testing dir
    os.chdir(SCRIPT_DIR)

    # move into testing build dir; mk it if it doesn't exist
    if not os.path.isdir("build"):
        os.mkdir("build")
    os.chdir("build")

    # run test(s)
    test_0(APP)

    # clean test(s)
    os.chdir(SCRIPT_DIR + "/build")

    os.system("rm -rf *")

    # display finished execution status
    print("\n[\033[32mDONE\033[0m]\n")


if __name__ == "__main__":
    main()