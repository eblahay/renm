#! /usr/bin/env bash


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


# This bash script is meant to automate the testing of the renm application

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR"

APP=$(realpath "$SCRIPT_DIR"/../build/renm)

echo "app: $APP"

cd build

# make test files
touch apple.txt orange.txt grape.txt 
printf "0:\n\t"
ls
echo

# test renm
echo "1:"
$APP "^apple" orange *
printf "\t"
ls

# clean test
rm *
printf "\n[DONE]\n" 


exit 0