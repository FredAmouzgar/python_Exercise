#!/usr/bin/env bash

apt-get update -qq
apt-get install -y xvfb -qq
wget -q https://raw.githubusercontent.com/FredAmouzgar/python_Exercise/master/Colab_setup/xvfb -O ../xvfb
