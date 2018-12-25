# Base directories
export WORKDIR=/mnt/panzer/yaglikca
export TOOLSDIR=${WORKDIR}/tools
export BENCHDIR=${WORKDIR}/benchmarks
export HELPDIR=${WORKDIR}/helpers

# Simulators
export M5PATH=${TOOLSDIR}/gem5
export M5_INCLUDE_PATH=${M5PATH}/include
export M5_UTILS_PATH=${M5PATH}/util/m5
export MCPATPATH=${TOOLSDIR}/cMcPAT
export LIBRARY_PATH=${M5_UTILS_PATH}:${LIBRARY_PATH}
export LD_LIBRARY_PATH=${M5_UTILS_PATH}:${LD_LIBRARY_PATH}

# python
export PYTHONPATH=${HELPDIR}:${PYTHONPATH}
