#include <iostream>
#include <stdexcept>
#include <filesystem>

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
