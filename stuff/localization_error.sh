#!/bin/bash

source /home/autoware/Autoware/install/local_setup.bash
export PYTHON2_EGG=carla-0.9.10-py2.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:/home/autoware/PythonAPI/$PYTHON2_EGG
export CARLA_AUTOWARE_CONTENTS=/home/autoware/autoware-contents
source /home/autoware/carla_ws/devel/setup.bash
source /home/autoware/Autoware/install/setup.bash

python /home/autoware/carla-autoware/stuff/localization_error.py