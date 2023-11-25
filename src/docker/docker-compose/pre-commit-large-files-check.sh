#!/bin/bash

for VAR in $(find . -type f -size +90M | grep -v ".git" | awk -F/ '{print $NF}')
do
	echo CHECKING FOR LARGE FILE :  $VAR
	GI=$(grep $VAR .gitignore)
	LFS=$(grep $VAR .gitattributes)

if ! [[ -z $GI ]]
then
	GIRESULT=" [OK] FOUND"
else
	echo $VAR >> .gitignore
	GIRESULT=" [OK] ADDED"
	git add .gitignore && git commit -m "$(date) - .gitignore $VAR"
fi

if ! [[ -z $LFS ]]
then
	LFRESULT=" [OK] FOUND"
else
	git lfs track $VAR 
	LFRESULT=" [OK] ADDED"
	git add .gitattributes && git commit -m "$(date) - .gitattributes $VAR"
fi
	echo "..... $GIRESULT"
	echo "..... $LFRESULT"
	echo " "
done