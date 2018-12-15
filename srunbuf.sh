#!/bin/bash

num_args=$#
args=${@}
cmd_str=""
for arg in "$@"
do
  cmd_str="${cmd_str} ${arg}"
done
echo ${cmd_str}
eval ${cmd_str}
