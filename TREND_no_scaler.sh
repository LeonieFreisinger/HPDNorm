#!/bin/bash
# re-install the packages
# pip uninstall -y neuralprophet
# pip install git+https://github.com/ourownstory/neural_prophet.git@normalization-layer
# pip uninstall -y darts
# pip install git+https://github.com/LeonieFreisinger/darts.git@lgbm_for_server#egg=darts

# ## NP
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# ## NP_localST
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_localST --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# ## TP
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# ## TP_localST
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model TorchProphetModel --params TP_localST --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# ## FNN
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# # FNN_sw
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfil20 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile21 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile22 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile23 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile24 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile25 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile26 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile27 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile28 &
# nohup python EXP_SYN_DATA.py --model NeuralProphetModel --params NP_FNN_sw --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile29 &

# # RNN
nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model RNNModel --params RNN --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# ## TF
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile10 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile11 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile12 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile13 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile14 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile15 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile16 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile17 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile18 &
# nohup python EXP_SYN_DATA.py --model TransformerModel --params TF --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile19 &

# # LGBM
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model LightGBMModel --params LGBM --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &


# ## Naive
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model NaiveModel --params Naive --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &

# ## SNaive
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 0.0 --gen_func "gen_model_and_params_none"  > soutfile0 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 1.0 --gen_func "gen_model_and_params_none" > soutfile1 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 2.0 --gen_func "gen_model_and_params_none" > soutfile2 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 3.0 --gen_func "gen_model_and_params_none"  > soutfile3 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 4.0 --gen_func "gen_model_and_params_none"  > soutfile4 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 5.0 --gen_func "gen_model_and_params_none"  > soutfile5 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 6.0 --gen_func "gen_model_and_params_none"  > soutfile6 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 7.0 --gen_func "gen_model_and_params_none"  > soutfile7 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 8.0 --gen_func "gen_model_and_params_none"  > soutfile8 &
# nohup python EXP_SYN_DATA.py --model SeasonalNaiveModel --params SNaive --heterogeneity_type "trend" --sample_upper_limit 9.0 --gen_func "gen_model_and_params_none"  > soutfile9 &
