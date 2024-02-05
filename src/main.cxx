/*
    renm — a bulk file renamer
    Copyright (C) 2024 Ethan Blahay

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

#include <boost/program_options/value_semantic.hpp>
#include <iostream>
#include <stdexcept>
#include <filesystem>
#include <regex>

#include <boost/program_options.hpp>

namespace po = boost::program_options;
namespace fs = std::filesystem;

int main(int argc, char* argv[]){
	try{
		// parse command-line arguments
        po::options_description cmdln_opts("Options");
        cmdln_opts.add_options()
            ("help,h", "prints this message")
            ("version", "prints program version information")
			("regex", po::value<std::regex>(), "The regex pattern to be used on the target")
			("target", po::value<fs::path>(), "The path upon which regex will be used to rename")
        ;

        po::variables_map vm;
        po::store(po::command_line_parser(argc, argv).options(cmdln_opts).run(), vm);
        po::notify(vm);

        // handle run & done modes
        if(vm.count("help")){
            std::cout << cmdln_opts << '\n';
            return 0;
        }
        else if(vm.count("version")){
            std::cout << "renm 0.1.0\n";
            return 0;
        }
        
        // main mode; body

		return 0;
	}
	catch(const std::exception &e){
        std::cout <<
            "\e[1m" << 
            program_invocation_short_name << 
            ": \e[31mFatal Error: \e[0m" <<
            e.what() <<
            '\n'
        ;
        return 1;
    }

    return 1;
}
