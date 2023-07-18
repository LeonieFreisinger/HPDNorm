#!/bin/bash
# re-install the packages
pip uninstall -y neuralprophet
pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
pip uninstall -y darts
pip install git+https://github.com/LeonieFreisinger/darts.git@revin_nonlearnable#egg=darts

# ## all NP-based variants and RNN instance
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_wb --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_norm"  > aoutfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw_wb --heterogeneity_type "amplitude" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_norm"  > aoutfilet1 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_in --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > aoutfile2 &

nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_wb --heterogeneity_type "offset" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_norm"  > ooutfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw_wb --heterogeneity_type "offset" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_norm"  > ooutfilet1 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_in --heterogeneity_type "offset" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none"  > ooutfile2 &

nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_wb --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_norm"  > toutfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw_wb --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_norm"  > toutfilet1 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_in --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > toutfile2 &

nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_wb --heterogeneity_type "heteroscedasticity" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_norm"  > houtfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw_wb --heterogeneity_type "heteroscedasticity" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_norm"  > houtfilet1 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_in --heterogeneity_type "heteroscedasticity" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > houtfile2 &

nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_wb --heterogeneity_type "structural_break" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_norm"  > soutfile0 &
nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw_wb --heterogeneity_type "structural_break" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_norm"  > soutfilet1 &
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_in --heterogeneity_type "structural_break" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile2 &

# re-install for RNN_ba
# pip uninstall -y darts
# pip install git+https://github.com/LeonieFreisinger/darts.git@revba_nonlearnable#egg=darts

# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_ba --heterogeneity_type "amplitude" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > aoutfile4 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_ba --heterogeneity_type "offset" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none"  > ooutfile4 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_ba --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > toutfile4 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_ba --heterogeneity_type "heteroscedasticity" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > houtfile4 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN_wb_ba --heterogeneity_type "structural_break" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
