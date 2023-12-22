#!/usr/bin/env python3
import json
import argparse
import os

from pathlib import Path

# Path object for the current file
current_file = Path(__file__)

# Relative path to the workspace folder
WORKSPACE_FOLDER = "${workspaceFolder}"

# Get the directory of the current file
current_dir = current_file.parent
project_dir = current_dir.resolve().parent.parent

default_c_cpp_properties_json = """{
    "configurations": [
        {
            "name": "Compile commands",
            "includePath": [],
            "forcedInclude": [],
            "defines": [],
            "compilerPath": "",
            "cStandard": "c99",
            "cppStandard": "c++17",
            "intelliSenseMode": "${default}"
        }
    ],
    "version": 4
}
"""

default_c_cpp_undef = """#ifndef C_CPP_UNDEF_H__
#define C_CPP_UNDEF_H__

#undef __x86_64
#undef __i386
#undef __APPLE__
#undef __unix__
#undef __unix
#undef unix
#undef _WIN32

#endif /* C_CPP_UNDEF_H__ */
"""


def get_path_to_workspace():
    return project_dir.absolute().as_posix()


def decode_compilie_commands(compile_commands_json):
    defines = set([])
    includes = set([])
    forced_includes = set([])
    workspace_path = get_path_to_workspace()

    for compile_command in compile_commands_json:
        command = compile_command["command"].split()
        arguments = command[1:]

        for index, argument in enumerate(arguments):
            argument = argument.replace(workspace_path, WORKSPACE_FOLDER)
            if argument.startswith("-D"):
                defines.add(argument[2:])
            elif argument.startswith("-I"):
                includes.add(argument[2:])
            elif argument.startswith("-include") or argument.startswith("-imacros"):
                forced_includes.add(
                    arguments[index + 1].replace(workspace_path, WORKSPACE_FOLDER)
                )

    compiler_path = ""
    if len(compile_commands_json) > 0:
        compiler_path = compile_commands_json[0]["command"].split()[0]

    config = {
        "compilerPath": compiler_path,
        "includePath": sorted(list(includes)),
        "defines": sorted(list(defines)),
        "forcedInclude": sorted(list(forced_includes)),
    }

    return config


def create_c_cpp_undef_h(vscode_dir):
    undef_path = "c_cpp_undef.h"
    if vscode_dir != "":
        undef_path = "{}/{}".format(vscode_dir, undef_path)

    if not os.path.isfile(undef_path):
        with open(undef_path, "w") as f:
            f.writelines(default_c_cpp_undef)


def convert_compile_commands(
    compile_commands_path, c_cpp_properties_path, include_undef=False
):
    # Extract build information from compile_commands.json
    with open(compile_commands_path, "r", encoding="utf-8") as compile_commands_file:
        compile_commands_json = json.load(compile_commands_file)
        config = decode_compilie_commands(compile_commands_json)

    # Read existing properties file if path was given otherwise use template
    if c_cpp_properties_path == None:
        c_cpp_properties_json = json.loads(default_c_cpp_properties_json)
        c_cpp_properties_path = "c_cpp_properties.json"
    else:
        if os.path.isfile(c_cpp_properties_path):
            with open(c_cpp_properties_path, "r") as c_cpp_properties_file:
                c_cpp_properties_json = json.load(c_cpp_properties_file)
        else:
            c_cpp_properties_json = json.loads(default_c_cpp_properties_json)

    if include_undef:
        vscode_dir = os.path.dirname(c_cpp_properties_path)
        create_c_cpp_undef_h(vscode_dir)
        config["forcedInclude"].append(f"{WORKSPACE_FOLDER}/.vscode/c_cpp_undef.h")

    # Update properties with extracted build information
    c_cpp_properties_json["configurations"][0].update(config)

    with open(c_cpp_properties_path, "w+", encoding="utf-8") as c_cpp_properties_file:
        json.dump(c_cpp_properties_json, c_cpp_properties_file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert cmake exported compile commands to Visual Studio "
        "Code C/C++ extension properties file."
        "\nExample usage: python3 .vscode/scripts/vscode_convert_compile_commands.py ./build/compile_commands.json -o .vscode/c_cpp_properties.json --undef",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "compile_commands_path", help="full path to compile_commands.json"
    )
    parser.add_argument("-o", metavar="FILE", help="path to c_cpp_properties.json")
    parser.add_argument("--undef", action="store_true", help="include undef header")
    args = parser.parse_args()

    convert_compile_commands(args.compile_commands_path, args.o, args.undef)

    # python3 .vscode/scripts/vscode_convert_compile_commands.py ./build/compile_commands.json -o .vscode/c_cpp_properties.json --undef
