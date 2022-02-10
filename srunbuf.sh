#!/bin/bash

num_args=$#
args=${@}
cmd_str=""
outdircame=0
for arg in "$@"
do
  cmd_str="${cmd_str} ${arg}"
  if [ $outdircame -eq 1 ]; then
    mkdir -p ${arg}
    outdircame=0
  fi
  if [ ${arg} == "--outdir" ]; then
    outdircame=1
  fi
done
echo ${cmd_str}
eval ${cmd_str}
