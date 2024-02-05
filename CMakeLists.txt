cmake_minimum_required(VERSION 3.22)

# set project name
project(renm)

# specify C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# find libs
find_package(Boost 1.74 COMPONENTS program_options REQUIRED)

# set up executable
set(
    APP_SRC
    src/main.cxx
)
add_executable(renm ${APP_SRC})
target_link_libraries(renm Boost::program_options)

# include directories must come AFTER the executable's been added
include_directories(include ${Boost_INCLUDE_DIR})