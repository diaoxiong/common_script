#!/bin/bash
from=$1
to=$2

if test -z ${from}
then
	echo "param missing"
	exit -1
fi

if [ ${from} = "-h" ] || [ ${from} = "--help" ]
then
	echo "usage: ./git_replace_branch.sh <from> <to>"
	exit -1
fi

if test -z ${to}
then
	echo "param missing"
	exit -1
fi

echo "replace from ${from} to ${to} start..."
echo -e "\n$ git checkout ${from}"
git checkout ${from}

echo -e "\n$ git push origin --delete ${to}"
git push origin --delete ${to}
echo -e "\n$ git branch -D ${to}"
git branch -D ${to}

echo -e "\n$ git checkout -b ${to}"
git checkout -b ${to}
echo -e "\n$ git push --set-upstream origin ${to}"
git push --set-upstream origin ${to}

echo -e "\n$ git push origin --delete ${from}"
git push origin --delete ${from}
echo -e "\n$ git branch -D ${from}"
git branch -D ${from}