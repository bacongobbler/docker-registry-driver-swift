#!/bin/bash

# the date in which the policy takes effect
date=${1:-"2014-07-08"}

commit_regex='^Merge\|^feat(\|^fix(\|^docs(\|^style(\|^refactor(\|^test(\|^chore('
commits=$(git log --format="%s" --after={"$date"} | grep -v $commit_regex)

if [ -n "$commits" ];
then
    echo "Some commit messages are malformed and require editing."
    echo "Please amend your commit[s] to follow the commit style guidelines:"
    echo "http://docs.deis.io/en/latest/contributing/standards/#commit-style-guide"
    exit 1
fi
