#!/bin/bash
# re-install the packages
pip uninstall -y neuralprophet
pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
pip uninstall -y darts
pip install git+https://github.com/LeonieFreisinger/darts.git@lgbm_for_server#egg=darts

nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting"  > ooutfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting" > ooutfile1 &
nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "offset" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_scalers" > ooutfile2 &
nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > ooutfile3 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting"  > ooutfile4 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "offset" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_scalers_reweighting"  > ooutfile5 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "offset" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_scalers"  > ooutfile6 &
nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "offset" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_scalers"  > ooutfile7 &
nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > ooutfile8 &
nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > ooutfile9 &
nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > ooutfile10 &
