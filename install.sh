#!/bin/bash

#install numpy
sudo apt-get install build-essential python-dev python-setuptools python-numpy python-scipy libatlas-dev libatlas3gf-base
sudo apt-get install build-essential python3-dev python3-setuptools python3-numpy python3-scipy libatlas-dev libatlas3gf-base

sudo update-alternatives --set libblas.so.3 /usr/lib/atlas-base/atlas/libblas.so.3
sudo update-alternatives --set liblapack.so.3 /usr/lib/atlas-base/atlas/liblapack.so.3

#install pip
sudo apt-get install python-pip

#install scikit
pip install --user --install-option="--prefix=" -U scikit-learn

#install yaafe
sudo apt-get install cmake cmake-curses-gui libargtable2-0 libargtable2-dev libsndfile1 libsndfile1-dev libmpg123-0 libmpg123-dev libfftw3-3 libfftw3-dev liblapack-dev libhdf5-serial-dev

cd yaafe-v0.64
mkdir build
cd build

cmake -DWITH_FFTW3=ON -DWITH_HDF5=ON -DWITH_LAPACK=ON -D -DWITH_MPG123=ON -DWITH_SNDFILE=ON -DWITH_TIMERS=ON ..

make
make install

INSTALL_DIR='/usr/local'
export YAAFE_PATH=$INSTALL_DIR/yaafe_extensions
export PATH=$INSTALL_DIR/bin:$PATH
# on MacOsX replace LD_LIBRARY_PATH => DYLD_LIBRARY_PATH
export LD_LIBRARY_PATH=$INSTALL_DIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$INSTALL_DIR/python_packages:$PYTHONPATH

