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
#include <cerrno>
#include <ios>
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
			("regex", po::value<std::string>(), "The regex pattern to be used on the target")
            ("format", po::value<std::string>(), "The string which dictates the format for the text which will replace the text matched by the regex")
			("source", po::value<std::vector<std::string>>(), "The path(s) upon which regex will be used to rename")
            ("force,f", "enable overwriting of existing files")
        ;

         po::positional_options_description p;
        p.add("regex", 1);
        p.add("format", 1);
        p.add("source", -1);

        po::variables_map vm;
        po::store(po::command_line_parser(argc, argv).options(cmdln_opts).positional(p).run(), vm);
        po::notify(vm);

        // handle run & done modes
        if(vm.count("help")){
            std::cout 
                << "Usage: " << program_invocation_short_name << " REGEX FORMAT FILE...\n"
                << '\n'
                << cmdln_opts
                << '\n'
            ;
            return 0;
        }
        else if(vm.count("version")){
            std::cout << "renm 0.1.0\n";
            return 0;
        }
        
        //
        std::vector<fs::path> paths;
        if(vm.count("source")){
            /*
                This is a work-around for what I assume is an error in
                boost::program_options version 1.74.0, where std::filesystem::path (unlike std::string)
                does not have a parsing operation capable of handling arguments which have spaces.
            */

            auto arr = vm["source"].as<std::vector<std::string>>();
            for(auto it = arr.begin(); it != arr.end(); it++){
                paths.push_back({*it});
            }
        }

        // main mode; body
        std::regex regex(vm["regex"].as<std::string>());

        for (auto it = paths.begin(); it != paths.end(); it++){
            fs::path dest = std::regex_replace(it->string(), regex, vm["format"].as<std::string>());
            std::cout << *it << " -> " << dest << '\n';
        }

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
