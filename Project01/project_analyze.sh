#!/usr/bin/env bash
set -u  # raise error when variable does not exist
set -e  # stop execution when error occurs

REPO_ROOT_PATH="../"

getInput(){
    echo "No parameter is given, please enter the number or the name of the feature:"
    echo "6 - del-temp-files:
    Find and delete all UNTRACKED (and untracked only) files ending in the extension .tmp"
    echo
    read -p "Your choice: " P1
    
}

delTempFiles(){
    echo "Executing feature #6 - Delete Temporary Files"
    untrackedFiles=$(git ls-files $REPO_ROOT_PATH --exclude-standard --others)
    for file in $untrackedFiles
    do
        if [[ "$file" == *.tmp ]]
            then
                echo "Removing $file"
                rm $file
        fi
    done
}

if [[ $# -eq 0 ]]
    then
        getInput
    else
        P1=$1
fi

if [[ "$P1" == "6" ]]||[[ "$P1" = 'del-temp-files' ]]
    then
        delTempFiles
fi
