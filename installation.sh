#!/bin/bash

pip install -r requirements.txt
pip install -e git+https://github.com/ourownstory/test-of-time.git@evolution_experiments_2#egg=test-of-time
pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
pip install git+https://github.com/LeonieFreisinger/darts.git@lgbm_for_server#egg=darts