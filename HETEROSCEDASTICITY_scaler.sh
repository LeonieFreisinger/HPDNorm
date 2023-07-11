#!/bin/bash
# re-install the packages
# pip uninstall -y neuralprophet
# pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
# pip uninstall -y darts
# pip install git+https://github.com/LeonieFreisinger/darts.git@lgbm_for_server#egg=darts


nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting"  > houtfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting" > houtfile1 &
nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers" > houtfile2 &
nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params TP_localST --heterogeneity_type "heteroscedasticity" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_scalers"  > houtfile3 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting"  > houtfile4 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers_reweighting"  > houtfile5 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > houtfile6 &
nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > houtfile7 &
nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > houtfile8 &
nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > houtfile9 &
nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "heteroscedasticity" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_scalers"  > houtfile10 &

