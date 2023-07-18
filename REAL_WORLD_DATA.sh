#!/bin/bash
# re-install the packages for full length scalers
# pip uninstall -y neuralprophet
# pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
# pip uninstall -y darts
# pip install git+https://github.com/LeonieFreisinger/darts.git@lgbm_for_server#egg=darts


### NP
# nohup python EXP_REAL_DATA.py --dataset EIA --model NeuralProphetModel --params NP --gen_func "gen_model_and_params_scalers_reweighting" > npoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NeuralProphetModel --params NP --gen_func "gen_model_and_params_scalers_reweighting" > npoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NeuralProphetModel --params NP --gen_func "gen_model_and_params_scalers_reweighting" > npoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NeuralProphetModel --params NP --gen_func "gen_model_and_params_scalers_reweighting" > npoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NeuralProphetModel --params NP --gen_func "gen_model_and_params_scalers_reweighting" > npoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NeuralProphetModel --params NP --gen_func "gen_model_and_params_scalers_reweighting" > npoutfile5 &

### NP_localST
# nohup python EXP_REAL_DATA.py --dataset EIA --model NeuralProphetModel --params NP_localST --gen_func "gen_model_and_params_scalers_reweighting" > nploutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NeuralProphetModel --params NP_localST --gen_func "gen_model_and_params_scalers_reweighting" > nploutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NeuralProphetModel --params NP_localST --gen_func "gen_model_and_params_scalers_reweighting" > nploutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NeuralProphetModel --params NP_localST --gen_func "gen_model_and_params_scalers_reweighting" > nploutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NeuralProphetModel --params NP_localST --gen_func "gen_model_and_params_scalers_reweighting" > nploutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NeuralProphetModel --params NP_localST --gen_func "gen_model_and_params_scalers_reweighting" > nploutfile5 &

### NP_FNN
# nohup python EXP_REAL_DATA.py --dataset EIA --model NeuralProphetModel --params NP_FNN --gen_func "gen_model_and_params_scalers_reweighting" > npfoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NeuralProphetModel --params NP_FNN --gen_func "gen_model_and_params_scalers_reweighting" > npfoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NeuralProphetModel --params NP_FNN --gen_func "gen_model_and_params_scalers_reweighting" > npfoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NeuralProphetModel --params NP_FNN --gen_func "gen_model_and_params_scalers_reweighting" > npfoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NeuralProphetModel --params NP_FNN --gen_func "gen_model_and_params_scalers_reweighting" > npfoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NeuralProphetModel --params NP_FNN --gen_func "gen_model_and_params_scalers_reweighting" > npfoutfile5 &

### NP_FNN_sw
# nohup pythonEXP_REAL_DATA.py --dataset EIA --model NeuralProphetModel --params NP_FNN_sw --gen_func "gen_model_and_params_scalers_reweighting" > npfsoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NeuralProphetModel --params NP_FNN_sw --gen_func "gen_model_and_params_scalers_reweighting" > npfsoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NeuralProphetModel --params NP_FNN_sw --gen_func "gen_model_and_params_scalers_reweighting" > npfsoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NeuralProphetModel --params NP_FNN_sw --gen_func "gen_model_and_params_scalers_reweighting" > npfsoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NeuralProphetModel --params NP_FNN_sw --gen_func "gen_model_and_params_scalers_reweighting" > npfsoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NeuralProphetModel --params NP_FNN_sw --gen_func "gen_model_and_params_scalers_reweighting" > npfsoutfile5 &

### TP
# nohup python EXP_REAL_DATA.py --dataset EIA --model TorchProphetModel --params TP --gen_func "gen_model_and_params_scalers" > tpoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model TorchProphetModel --params TP --gen_func "gen_model_and_params_scalers" > tpoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model TorchProphetModel --params TP --gen_func "gen_model_and_params_scalers" > tpoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model TorchProphetModel --params TP --gen_func "gen_model_and_params_scalers" > tpoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model TorchProphetModel --params TP --gen_func "gen_model_and_params_scalers" > tpoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model TorchProphetModel --params TP --gen_func "gen_model_and_params_scalers" > tpoutfile5 &

### TP_localST
# nohup python EXP_REAL_DATA.py --dataset EIA --model TorchProphetModel --params TP_localST --gen_func "gen_model_and_params_scalers" > tploutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model TorchProphetModel --params TP_localST --gen_func "gen_model_and_params_scalers" > tploutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model TorchProphetModel --params TP_localST --gen_func "gen_model_and_params_scalers" > tploutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model TorchProphetModel --params TP_localST --gen_func "gen_model_and_params_scalers" > tploutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model TorchProphetModel --params TP_localST --gen_func "gen_model_and_params_scalers" > tploutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model TorchProphetModel --params TP_localST --gen_func "gen_model_and_params_scalers" > tploutfile5 &

### TF
# nohup python EXP_REAL_DATA.py --dataset EIA --model TransformerModel --params TF --gen_func "gen_model_and_params_scalers" >tfoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model TransformerModel --params TF --gen_func "gen_model_and_params_scalers" > tfoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model TransformerModel --params TF --gen_func "gen_model_and_params_scalers" > tfoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model TransformerModel --params TF --gen_func "gen_model_and_params_scalers" > tfoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model TransformerModel --params TF --gen_func "gen_model_and_params_scalers" > tfoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model TransformerModel --params TF --gen_func "gen_model_and_params_scalers" > tfoutfile5 &

### RNN
# nohup python EXP_REAL_DATA.py --dataset EIA --model RNNModel --params RNN --gen_func "gen_model_and_params_scalers" > routfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model RNNModel --params RNN --gen_func "gen_model_and_params_scalers" > routfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model RNNModel --params RNN --gen_func "gen_model_and_params_scalers" > routfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model RNNModel --params RNN --gen_func "gen_model_and_params_scalers" > routfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model RNNModel --params RNN --gen_func "gen_model_and_params_scalers" > routfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model RNNModel --params RNN --gen_func "gen_model_and_params_scalers" > routfile5 &

### LGBM
# nohup python EXP_REAL_DATA.py --dataset EIA --model LightGBMModel --params LGBM --gen_func "gen_model_and_params_scalers" > loutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model LightGBMModel --params LGBM --gen_func "gen_model_and_params_scalers" > loutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model LightGBMModel --params LGBM --gen_func "gen_model_and_params_scalers" > loutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model LightGBMModel --params LGBM --gen_func "gen_model_and_params_scalers" > loutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model LightGBMModel --params LGBM --gen_func "gen_model_and_params_scalers" > loutfile4 &
nohup python EXP_REAL_DATA.py --dataset ETTh --model LightGBMModel --params LGBM --gen_func "gen_model_and_params_scalers" > loutfile5 &

### Naive
# nohup python EXP_REAL_DATA.py --dataset EIA --model NaiveModel --params Naive --gen_func "gen_model_and_params_scalers" > noutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NaiveModel --params Naive --gen_func "gen_model_and_params_scalers" > noutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NaiveModel --params Naive --gen_func "gen_model_and_params_scalers" > noutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NaiveModel --params Naive --gen_func "gen_model_and_params_scalers" > noutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NaiveModel --params Naive --gen_func "gen_model_and_params_scalers" > noutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NaiveModel --params Naive --gen_func "gen_model_and_params_scalers" > noutfile5 &

### SNaive
# nohup python EXP_REAL_DATA.py --dataset EIA --model SeasonalNaiveModel --params SNaive --gen_func "gen_model_and_params_scalers" > snoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model SeasonalNaiveModel --params SNaive --gen_func "gen_model_and_params_scalers" > snoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model SeasonalNaiveModel --params SNaive --gen_func "gen_model_and_params_scalers" > snoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model SeasonalNaiveModel --params SNaive --gen_func "gen_model_and_params_scalers" > snoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model SeasonalNaiveModel --params SNaive --gen_func "gen_model_and_params_scalers" > snoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model SeasonalNaiveModel --params SNaive --gen_func "gen_model_and_params_scalers" > snoutfile5 &

#pip uninstall -y darts
#pip install git+https://github.com/LeonieFreisinger/darts.git@revin_nonlearnable#egg=darts

# #### NP_FNN_wb
# nohup python EXP_REAL_DATA.py --dataset EIA --model NeuralProphetModel --params NP_FNN_wb --gen_func "gen_model_and_params_norm" > npfwoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NeuralProphetModel --params NP_FNN_wb --gen_func "gen_model_and_params_norm" > npfwoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NeuralProphetModel --params NP_FNN_wb --gen_func "gen_model_and_params_norm" > npfwoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NeuralProphetModel --params NP_FNN_wb --gen_func "gen_model_and_params_norm" > npfwoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NeuralProphetModel --params NP_FNN_wb --gen_func "gen_model_and_params_norm" > npfwoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NeuralProphetModel --params NP_FNN_wb --gen_func "gen_model_and_params_norm" > npfwoutfile5 &

# #### NP_FNN_sw_wb
# nohup python EXP_REAL_DATA.py --dataset EIA --model NeuralProphetModel --params NP_FNN_sw_wb --gen_func "gen_model_and_params_norm" > npfswoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model NeuralProphetModel --params NP_FNN_sw_wb --gen_func "gen_model_and_params_norm" > npfswoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model NeuralProphetModel --params NP_FNN_sw_wb --gen_func "gen_model_and_params_norm" > npfswoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model NeuralProphetModel --params NP_FNN_sw_wb --gen_func "gen_model_and_params_norm" > npfswoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model NeuralProphetModel --params NP_FNN_sw_wb --gen_func "gen_model_and_params_norm" > npfswoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model NeuralProphetModel --params NP_FNN_sw_wb --gen_func "gen_model_and_params_norm" > npfswoutfile5 &

# #### RNN_wb_in
# nohup python EXP_REAL_DATA.py --dataset EIA --model RNNModel --params RNN_wb_in --gen_func "gen_model_and_params_none" > rwoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model RNNModel --params RNN_wb_in --gen_func "gen_model_and_params_none" > rwoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model RNNModel --params RNN_wb_in --gen_func "gen_model_and_params_none" > rwoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model RNNModel --params RNN_wb_in --gen_func "gen_model_and_params_none" > rwoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model RNNModel --params RNN_wb_in --gen_func "gen_model_and_params_none" > rwoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model RNNModel --params RNN_wb_in --gen_func "gen_model_and_params_none" > rwoutfile5 &

#pip uninstall -y darts
#pip install git+https://github.com/LeonieFreisinger/darts.git@revba_nonlearnable#egg=darts

# #### RNN_wb_ba
# nohup python EXP_REAL_DATA.py --dataset EIA --model RNNModel --params RNN_wb_ba --gen_func "gen_model_and_params_none" > rwoutfile0 &
# nohup python EXP_REAL_DATA.py --dataset London --model RNNModel --params RNN_wb_ba --gen_func "gen_model_and_params_none" > rwoutfile1 &
# nohup python EXP_REAL_DATA.py --dataset ERCOT --model RNNModel --params RNN_wb_ba --gen_func "gen_model_and_params_none" > rwoutfile2 &
# nohup python EXP_REAL_DATA.py --dataset Australian --model RNNModel --params RNN_wb_ba --gen_func "gen_model_and_params_none" > rwoutfile3 &
# nohup python EXP_REAL_DATA.py --dataset Solar --model RNNModel --params RNN_wb_ba --gen_func "gen_model_and_params_none" > rwoutfile4 &
# nohup python EXP_REAL_DATA.py --dataset ETTH_panel --model RNNModel --params RNN_wb_ba --gen_func "gen_model_and_params_none" > rwoutfile5 &
