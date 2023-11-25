#!/bin/bash

# simple script to recursively add current folder contents
# to a git repository - using git-lfs for files over 100M 
#
# typical function 
# - if pre-requisites missing, install and prompt
# - checkout branch
# - manage large files with git-lfs (.gitattributes)
# - add files using git add . (.gitignore applicable)
# - commit with date
# - push 
#
#

default_branch_name="testing"

 
function lfs_required() {
if [[ $(find . -type f -size +90M) ]]
then
echo "files >100MB found - checking for git-lfs" 	
  if ! [[ $(which git-lfs) ]]
  then
    echo "git-lfs missing: install manually or run ${0} --depends" && exit 
  else
    echo "git-lfs installed: files will be added" 
  fi  
else
  echo "no files >100MB found - preparing normal backup" 
fi
}

function git_status() {
  if [ -d .git ]
  then
    echo ".git folder found - no paramaters passed"
    echo $(git status)
    echo "  "
    ${0} -help
  else
    echo " "
    echo " no .git folder"
    echo " "
    exit 41
  fi
}

function go_backup() {
 if [[ -z ${target_folder} ]]
 then 
   target_folder=$(pwd)
   echo "default folder: ${target_folder}"
 else
   echo "backup folder : ${target_folder}"
 fi

 if [[ -z ${branch_name} ]]
 then
   branch_name=${default_branch_name}
   echo "default branch: ${branch_name}"
 else
   echo "target branch : ${branch_name}"
 fi

 if [[ "$1" == "dry" ]]; 
 then 
   echo " "
   echo $(git status -s)| sed 's/??/§-/g'| tr '§' '\n'|sort; fi
   echo " "
   echo "sources"
   echo "    from ${target_folder}"
   echo "    added to branch ${branch_name}"
   echo " "
   dry_run=$(cat <<EOF
 ██████╗ ██████╗ ██╗   ██╗    ██████╗ ██╗   ██╗███╗   ██╗
 ██╔══██╗██╔══██╗╚██╗ ██╔╝ P  ██╔══██╗██║   ██║████╗  ██║
 ██║  ██║██████╔╝ ╚████╔╝  K  ██████╔╝██║   ██║██╔██╗ ██║
 ██║  ██║██╔══██╗  ╚██╔╝   N  ██╔══██╗██║   ██║██║╚██╗██║
 ██████╔╝██║  ██║   ██║ PKNW1 ██║  ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚═╝  ╚═╝   ╚═╝    1  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
EOF)
   echo "${dry_run}"
   echo " run command without -d to process"
} 

if [[ $# -eq -0 ]]; then git_status; fi 

while getopts "t:h:sb:riad" arg; do
  case $arg in
    h|help)
      cat <<EOF

  backup-to-git-repo help
  -----------------------

  -target
  -help
  -branch
  -restore
  -install
  -setup
  -approve

  usage "${0}" opts

EOF
      ;;
    t|target)
      target_folder=$OPTARG
      echo $target_folder
      ;;
    b|branch) 
      branch_name=$OPTARG
      echo "new branch named ${OPTARG} requested"
      ;;
    r|restore)
      echo restore ${branch_name}
      ;;
    i|install)
      echo "install required components"
      ;;
    s|setup)
      echo "new git setup"
      ;;
    a|approve)
      echo "auto-approve all commands"
      go_backup
      ;;
    d) 
      go_backup dry
      ;;
  esac
done

