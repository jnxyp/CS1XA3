#!/usr/bin/env bash
#set -u  # raise error when variable does not exist
set -e  # stop execution when error occurs

REPO_ROOT_PATH="../"

function getChoice(){
    echo -e "No parameter is given, please enter the number or the name of the feature:"
    echo "2 - create-todo-log:
    Puts each line of every file in your repo with the tag #TODO into a file todo.log"
    echo "6 - del-temp-files:
    Find and delete all UNTRACKED (and untracked only) files ending in the extension .tmp"
    echo "C1 - create-colored-file input_file_path [output_file_path]:
    This function will insert random color controlling characters into target file, to make it pretty to print in terminal lol"
    echo "==========================================="
    read -p "Your choice: " P1
    
}

function delTempFiles(){
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
    echo "DONE!"
}

function createTodoLog(){
    echo "Executing feature #2 - Create a TODO Log"
    [ -e todo.log ] && rm todo.log
    grep -E "# *TODO" $REPO_ROOT_PATH -r -n --exclude=todo.log > todo.log
    echo "DONE!"
}

function rand_color(){
    echo "\e[3$(( $RANDOM * 6 / 32767 + 1 ))m"
}

function coloredTextFile(){
    if [ -z "$2" ]
        then
            if [ "$1" = false ]
                then
                    echo "No file is given!"
                    exit 1
            else
                read -p "Please specify the file for coloring: " P1
                read -p "Please specify the output file (press enter to output to the input): " P2
            fi
    else
        P1=$2
        P2=$3
    fi
    
    if [ -z "$3" ]
        then
            P2=$P1
    fi
    
    file_str=$(cat $P1)
    
    echo -n '' > $P2
    
    for (( i=0; i<${#file_str}; i++ )); 
        do
            echo -en "$(rand_color)${file_str:$i:1}" >> $P2
    done
    
    echo -en "\e[0m" >> $P2
    
    cat $P2
    echo -e "\e[0m"
    
    echo "DONE!"
}

interactive=false

if [[ $# -eq 0 ]]
    then
        getChoice
        interactive=true
    else
        P1=$1
fi

if [[ "$P1" == "6" ]]||[[ "$P1" = 'del-temp-files' ]]
    then
        delTempFiles $interactive
elif [[ "$P1" == "2" ]]||[[ "$P1" = 'create-todo-log' ]]
    then
        createTodoLog $interactive
elif [[ "$P1" == "C1" ]]||[[ "$P1" = 'create-colored-file' ]]
    then
        coloredTextFile $interactive $2 $3
else
    echo "No such a command!"
fi
