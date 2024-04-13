cmake_minimum_required(VERSION 3.20.0)

set(BUILD_TYPE
    "release"
    CACHE STRING "Build type chosen by the user at CMake configure time")

set_property(CACHE BUILD_TYPE PROPERTY STRINGS debug release)

# Let CMake create a compile_commands.json file for use by the IDE and other
# tools.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Include the Zephyr build system.
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

# Name of the application.
project(
    zephyr-application-template
    VERSION 0.0.1
    DESCRIPTION "Zero to hero with Zephyr"
    HOMEPAGE_URL "https://github.com/pflonz/zephyr-application-template"
    LANGUAGES C ASM)

# Print out build type.
message(STATUS "Build type: \t 🚀 ${BUILD_TYPE}")
message(STATUS "Board root: \t 📁 ${BOARD_ROOT}")
message(STATUS "Board: \t 🎛️  ${BOARD}")

# Configure application version information. c
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/include/version.h.in
               ${CMAKE_CURRENT_BINARY_DIR}/include/version.h)

# List of application include directories.
set(INCLUDES include ${CMAKE_CURRENT_BINARY_DIR}/include)

# Add the application include directories.
target_include_directories(app PRIVATE ${INCLUDES})

# List of application source files.
set(SOURCES src/main.c)

# Add the application source files.
target_sources(app PRIVATE ${SOURCES})

# Generate a git hash that's used as part of the software_version, eg
# 1.0.0+12345678. Permit overriding at command line for CI builds.
if (NOT DEFINED ZEPHYR_PROJECT_GIT_SHA1)
  EXECUTE_PROCESS(
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND git rev-parse --short HEAD
    RESULT_VARIABLE commit_sha1
    OUTPUT_VARIABLE ZEPHYR_PROJECT_GIT_SHA1
    OUTPUT_STRIP_TRAILING_WHITESPACE
    COMMAND_ERROR_IS_FATAL ANY
  )
endif()

zephyr_compile_definitions(
    ZEPHYR_PROJECT_GIT_SHA1=\"${ZEPHYR_PROJECT_GIT_SHA1}\"
)

# Check if Doxygen is installed
find_package(Doxygen OPTIONAL_COMPONENTS dot OPTIONAL_COMPONENTS mscgen dia)

# Set documentation inputs
set(DOCU_INPUT ${CMAKE_CURRENT_SOURCE_DIR}/../README.md
               ${CMAKE_CURRENT_SOURCE_DIR}/../docs ${CMAKE_CURRENT_SOURCE_DIR})

# Set Doxygen output directory
set(DOXYGEN_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/docs)

# Set Doxygen configuration variables
set(DOXYGEN_GENERATE_HTML YES)
set(DOXYGEN_FULL_PATH_NAMES NO)
set(DOXYGEN_USE_MDFILE_AS_MAINPAGE ${CMAKE_CURRENT_SOURCE_DIR}/../README.md)
set(DOXYGEN_EXCLUDE_PATTERNS */tests/* */lib/*)

# If Doxygen is found, build the documentation
if(DOXYGEN_FOUND)
    doxygen_add_docs(doxygen ${DOCU_INPUT}
                     COMMENT "Generate doxygen documentation")
else()
    message(
        "Doxygen need to be installed to generate the doxygen documentation")
endif()
