#!/bin/bash
set -e

# If running at test level
IF_TEST=0
# Directory storing tiles sampled from S01-preprocessing/scripts/4-Extracting-Patches-Features.sh
# IT MUST BE UNDER DIR_DATA or DIR_DATA_EXP
DIR_FEAT=feats-l1-s256-mrandom_be-n1000-color_norm 

# Build initial KNN graph
method=knn
K=6
T=0
# The output directory UNDER ${DIR_DATA}/${DIR_FEAT} or ${DIR_DATA_EXP}/${DIR_FEAT}
DIR_GRAPH=graph-${method}-k${K}-t${T}-mysplit #用HistoFL的split划分新的knn
# DIR_GRAPH=graph-knn-k6-t0

# Path of CLAM Library
DIR_REPO=../tools

# Path of pathology images, only used for tuning experiments
# DIR_DATA_EXP=/home/liup/tmp/NLST_Path_Tmp
# Path of pathology images, only used for formal experiments
# DIR_DATA=/NAS/Dataset/NLST/PathologySlide
# DIR_DATA=/NAS/Dataset/NLST/PathologySlide
DIR_DATA=/home/jupyter-ljh/data/mntdata/data0/LIU_shaojun/TCGA-BRCA/WSI
# tables directory
# TBS_DATA=/NAS/Dataset/NLST/Pathology
# TBS_DATA=/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/data_split/tcga_brca/tcga_brca_path_full_ljh.csv
TBS_DATA=/home/jupyter-ljh/data/mydata/GraphLSurv-main/S02-modeling/data_split/tcga_brca_ljh/tcga_brca_path_full_ljh.csv #改放置在代码目录下
DIR_SAVE=/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA

cd ${DIR_REPO}

if [ ${IF_TEST} -eq 1 ]; then
    echo "running for test"
    python3 graph_builder.py \
        --dir_input ${DIR_DATA_EXP}/${DIR_FEAT}/h5_files \
        --dir_output ${DIR_DATA_EXP}/${DIR_FEAT}/${DIR_GRAPH} \
        --csv_sld2pat ${TBS_DATA}/nlst_path_path2pat.csv \
        --graph_level patient \
        --num_neighbours ${K} \
        --threshold ${T} \
        --num_workers 1 \
        --verbose
else
    echo "running for building graphs of all slides"
    python3 graph_builder.py
fi
    # python3 graph_builder.py \
    #     --dir_input ${DIR_DATA}/${DIR_FEAT}/h5_files \
    #     --dir_output ${DIR_DATA}/${DIR_FEAT}/${DIR_GRAPH} \
    #     --csv_sld2pat ${TBS_DATA}/nlst_path_path2pat.csv \
    #     --graph_level patient \
    #     --method ${method} \
    #     --num_neighbours ${K} \
    #     --threshold ${T} \
    #     --num_workers 2 \
    #     --verbose
    # echo "running for building graphs of all slides"
    # python3 graph_builder.py \
    #     --dir_input ${DIR_SAVE}/${DIR_FEAT}/h5_files \
    #     --dir_output ${DIR_SAVE}/${DIR_FEAT}/${DIR_GRAPH} \
    #     --csv_sld2pat ${TBS_DATA} \
    #     --graph_level patient \
    #     --method ${method} \
    #     --num_neighbours ${K} \
    #     --threshold ${T} \
    #     --num_workers 0 \
    #     --verbose
    # echo "running for building graphs of all slides"
    # python3 graph_builder.py \
    #     --dir_input ${DIR_SAVE}/${DIR_FEAT}/h5_files \
    #     --dir_output ${DIR_SAVE}/${DIR_FEAT}/${DIR_GRAPH} \
    #     --csv_sld2pat ${TBS_DATA} \
    #     --graph_level patient \
    #     --method ${method} \
    #     --num_neighbours ${K} \
    #     --threshold ${T} \
    #     --num_workers 0 \
    #     --verbose