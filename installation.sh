#!/bin/bash

pip install -r requirements.txt
pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer # install neuralprophet first to have the right torch version
pip install git+https://github.com/LeonieFreisinger/darts.git@master
pip install git+https://github.com/ourownstory/test-of-time.git # install test-of-time last to have the right neuralprophet and darts version