# Zephyr RTOS Template Project

![Build](https://github.com/pflonz/zephyr-application-template/actions/workflows/build.yml/badge.svg)

- [Zephyr RTOS Template Project](#zephyr-rtos-template-project)
  - [About the project](#about-the-project)
  - [Setup development environment](#setup-development-environment)
  - [Clone the project](#clone-the-project)
  - [Setup project](#setup-project)
  - [Build project](#build-project)
  - [Configure project](#configure-project)
  - [Flash project](#flash-project)
  - [Run the serial monitor](#run-the-serial-monitor)
  - [Unit Testing and Code Coverage with Twister](#unit-testing-and-code-coverage-with-twister)
    - [Build and run unit tests manually](#build-and-run-unit-tests-manually)
    - [Build and run unit tests automatically](#build-and-run-unit-tests-automatically)
  - [Build Documentation](#build-documentation)
  - [ToDo](#todo)

## About the project

This repository contains the source code for a [Zephyr RTOS](https://docs.zephyrproject.org/latest/index.html) template application.

## Setup development environment

> TODO: Add description for development environment setup

## Clone the project

You can clone the project by running the following command from WSL2:

```bash
# cd to your projects root folder e.g. ~/projects
$ cd ~/projects 

# clone the repository and it's submodules
$ git clone --recursive git@github.com:pflonz/zephyr-application-template.git
```

## Setup project

If your're using the VSCode devcontainer, there is nothing to do.

If you want to setup the project within WSL2 please run these commands:

```bash
# cd into the application project folder
$ cd ~/projects/zephyr-application-template

# run west update to initialize the project and it's dependencies
$ west update

# export the project's CMake configuration
$ west zephyr-export
```

## Build project

```bash
# cd into the project folder
$ cd ~/projects/zephyr-application-template

# Release build
$ west build -b <your-board> -s apps/template
# or
$ west build -b <your-board> -s apps/template -- -DBUILD_TYPE=release

# Debug build
$ west build -b <your-board> -s apps/template -- -DBUILD_TYPE=debug
```

## Configure project

The configuration of the project can be done in two different ways:

1. Customize the project configuration file.

    The project configuration file `prj.conf` can be edited directly in the editor and can be found under the path `app/prj.conf`

2. Customize the project configuration via the GUI.

    The build target `menuconfig` can be used to start the GUI for the project configuration. The command for this is: `$ west build -b <your-board> -s apps/template -t menuconfig`

    > **Note:** The GUI can only be used if the project has been built at least once.

## Flash project

From project root folder call:

```bash
west flash
```

## Run the serial monitor

From project root folder call:

```bash
west espressif monitor
```

## Unit Testing and Code Coverage with Twister

The following approaches currently works only for specific modules.

### Build and run unit tests manually

This approach is useful when you want to run unit tests manually, for example, when you want to build software according to the concept of test-driven development (TDD).

```bash
# Basic approach
$ west build -b unit_testing -d build/unit_testing/<your_module> deps/modules/<your_module>/tests && build/unit_testing/<<our_module>/testbinary

# Example for "sample_module"
$ west build -b unit_testing -d build/unit_testing deps/modules/sample_module/tests && build/unit_testing/testbinary
```

### Build and run unit tests automatically

This approach is useful when you want to run all unit tests automatically, for example when you want to run unit tests in a CI/CD pipeline.

> If you want to run one specific test you can use the `-T`option to specify the folder where the test is located.

```bash
# Build and run ALL unit tests and create coverage reports (around 200)
$ west twister --coverage -p unit_testing -O build/twister-out

# Build and run unit tests for a specific module (e.g. smaple_modules) and create coverage reports
$ west twister --coverage -p unit_testing -O build/twister-out -T ./deps/modules/sample_module/
```

## Build Documentation

The documentation is based on [Doxygen](https://www.doxygen.nl/index.html) and can be build with the following command:

```bash
# Build documentation
$ west build -b <your-board> -s apps/template -t doxygen
```

## ToDo

- [ ] Add unit test suite for the application
- [ ] Automate c_cpp_properties.json update by script
