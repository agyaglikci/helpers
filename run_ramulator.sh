#!/bin/bash

num_args=$#
args=${@}
cmd_str=""
outdircame=0
for arg in "$@"
do
  cmd_str="${cmd_str} ${arg}"
  if [[ ${arg} == *"outdir"* ]]; then
    outdir=`cut -d "=" -f 2 <<< "${arg}"`
    echo "Creating ${outdir}"
    mkdir -p ${outdir}
  fi
done
echo "Running the following code on ${HOSTNAME}:"
echo ${cmd_str}
eval ${cmd_str}

cp ${outdir}/ramulator.stats ${outdir/local/panzer}/ramulator.stats
