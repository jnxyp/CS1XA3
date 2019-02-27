# CS 1XA3 Project 01

Author: `Xin Yipeng`

Mac ID: `xiny13`

## Introduction

This utility script provides several useful features to manage a git repository ~~(and a custom command for fun)~~.

You can either pass the choice of feature (and their arguments) through console parameters, or you can also execute the script without entering parameters to use the interactive execution mode, which the script will guide the user to choose the function and input required parameters.

## Usage

|Command|Description|
|--|--|
|`.\project_analyze.sh`|Enter the interactive execution mode|
|`.\project_analyze.sh 2` OR `.\project_analyze.sh create-todo-log`|Puts each line of every file in your repo with the tag `#TODO` into a file todo.log|
|`.\project_analyze.sh 6` OR `.\project_analyze.sh del-temp-files`|Find and delete all **UNTRACKED** (and untracked only) files ending in the extension `.tmp`|
|`.\project_analyze.sh C1 input_file_path [output_file_path]` OR `.\project_analyze.sh create-colored-file input_file_path [output_file_path]`|This function will insert **random color** controlling characters into the content of `input_file_path`, and output to the `output_file_path`, to make it pretty to print in terminal lol|

## Note
- Leave the `output_file_path` empty if you want to output colored text to the input file directly
- For the non-interactive execution mode, all the parameters (include command choice and arguments for each command) must be filled at once for the script to run automatically.