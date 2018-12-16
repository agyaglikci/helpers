#!/bin/bash

InstallDirectory=/opt
# AnacondaVersion=5.3.1 # uncomment this line if you prefer Anaconda

if [ `whoami` != "root" ]; then
    echo "First run su root. Then run this script."
    exit
fi

cd ~
mkdir -p tmp
cd tmp
echo "Working under: "`pwd`
apt-get update

echo "Installing essentials"
for package in "g++" "byobu" "vim" "ca-certificates" "git" "make" "r-cran-pkgmaker" "locales" "libc6-dev-i386 gcc-multilib g++-multilib"; do
  echo ""
  echo ">>> Installing $package"
  apt-get install $package
done

# echo ""
# echo "Installing Anaconda2 (I prefer this over Python because of large library support. You can also run the following:"
# echo "apt-get install python-dev"
# wget https://repo.anaconda.com/archive/Anaconda2-${AnacondaVersion}-Linux-x86_64.sh
# echo "  The next script will run interactively."
# echo "  Hit Enter to continue."
# echo "  Type yes to accept the terms and conditions"
# echo "  Install anaconda under ${InstallDirectory}/anaconda2"
# echo "  Type no to not to install Microsoft VSCode (it is not needed)."
# bash Anaconda2-${AnacondaVersion}-Linux-x86_64.sh

echo "Installing gem5 dependencies"
for package in "zlib1g-dev" "automake" "scons" "libprotobuf-dev python-protobuf protobuf-compiler libgoogle-perftools-dev" "python-dev"; do
  echo ""
  echo ">>> Installing $package"
  apt-get install $package
done

echo "Installing some helper packages"
for package in "flex" "bison"; do
  echo ""
  echo ">>> Installing $package"
  apt-get install $package
done
