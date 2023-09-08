SRC_DOMAIN="real"
TGT_DOMAIN="clipart"
SRC_MODEL_DIR="/opt/tta/hwc_TTA/output/domainnet-126/source"

PORT=10013
MEMO="Confidence"
SUB_MEMO="CE-KL+PSL_FILTER+FIRST_CONFI_VER2+PL_FNOISE"

for SEED in 2020
do
    CUDA_VISIBLE_DEVICES=2,3 python main_adacontrast.py \
    seed=${SEED} port=${PORT} memo=${MEMO} sub_memo=${SUB_MEMO} project="domainnet-126" \
    data.data_root="/mnt/data" data.workers=8 \
    data.dataset="domainnet-126" data.source_domains="[${SRC_DOMAIN}]" data.target_domains="[${TGT_DOMAIN}]" \
    model_src.arch="resnet50" \
    model_tta.src_log_dir=${SRC_MODEL_DIR} \
    optim.lr=2e-4
done