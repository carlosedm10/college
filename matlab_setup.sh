#!/bin/bash

# Check if gtimeout is available
if ! command -v gtimeout &> /dev/null
    echo "gtimeout is already installed"
then
    echo "gtimeout could not be found, attempting to install coreutils using Homebrew."
    # Install Homebrew if it's not installed
    if ! command -v brew &> /dev/null
    then
        echo "Homebrew not found. Please install Homebrew and rerun this script."
        exit 1
    fi
    # Install coreutils
    brew install coreutils
    echo "coreutils installed successfully."
fi

# Attempt to find MATLAB path automatically
MATLAB_PATH=$(find /Applications -name matlab -type f -print -quit)

# Attempt to find the 'college/TDS' directory automatically
PROJECT_DIR=$(gtimeout 2s find ~/ -type d -path "*/college/TDS" 2>/dev/null)

# Check if MATLAB was found
if [ -n "$MATLAB_PATH" ]; then
    echo "MATLAB directory set to: $MATLAB_PATH"
    export MATLAB_PATH
else
    echo "MATLAB not found. Please set MATLAB_PATH manually."
fi

# Check if PROJECT_DIR was successfully set
if [ -n "$PROJECT_DIR" ]; then
    echo "Project directory set to: $PROJECT_DIR"
    export PROJECT_DIR
else
    echo "Project directory not found. Please check the path."
fi

# Continue with the intended commands or make call
# make
