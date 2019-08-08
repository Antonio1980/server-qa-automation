#!/bin/bash

filepath=$HOME/reportAPI
mails=(antons@eyenet-mobile.com)

declare -A envs
envs["prod"]="$HOME/src/repo/files/[].json"
col = "$HOME/src/repo/files/[].json"

for e in ${!envs[@]}; do
    echo Running environment ${envs[$e]}
    'newman' run col -e ${envs[$e]} | tee $filepath
    for m in ${mails[@]}; do
	echo "File $filepath"
        echo "Sending report message to $m with env $e"
        mail -s "Report Postman. ENV: $e" $m < $filepath
    done
done
