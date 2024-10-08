PORT=10014
CUDA=1,2
MEMO="VISDAC"
SUB_MEMO="offline"
SRC_MODEL_DIR="/opt/tta/CNA_TTA/output/VISDA-C/source/"

for SEED in 2021 2022 2023
do
    CUDA_VISIBLE_DEVICES=${CUDA} python ../main.py \
    seed=${SEED} port=${PORT} memo=${MEMO} sub_memo=${SUB_MEMO} project="VISDA-C" \
    data.data_root="/mnt/data" data.workers=8 \
    data.dataset="VISDA-C" data.source_domains="[train]" data.target_domains="[validation]" \
    model_src.arch="resnet101" \
    model_tta.src_log_dir=${SRC_MODEL_DIR} \
    learn.epochs=30 \
    optim.lr=2e-4 
done

