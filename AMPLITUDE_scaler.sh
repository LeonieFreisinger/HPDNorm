#!/bin/bash
# re-install the packages
pip uninstall -y neuralprophet
pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
pip uninstall -y darts
pip install git+https://github.com/LeonieFreisinger/darts.git@lgbm_for_server#egg=darts


nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "amplitude" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_scalers_reweighting" > aoutfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting" > aoutfile1 &
nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "amplitude" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_scalers" > aoutfile2 &
nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > aoutfile3 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting"  > aoutfile4 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "amplitude" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_scalers_reweighting"  > aoutfile5 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > aoutfile6 &
nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > aoutfile7 &
nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > aoutfile8 &
nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > aoutfile9 &
nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > outfile10 &
