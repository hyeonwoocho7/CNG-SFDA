PORT=17012
CUDA=1,2,3,4
SRC_MODEL_DIR="/opt/tta/hwc_TTA/output/domainnet-126/source"
SRC_DOMAINS=(real    real    real     sketch    clipart painting)
TGT_DOMAINS=(sketch  clipart painting painting  sketch  real    )
PORTS=(${PORT} ${PORT} ${PORT} ${PORT} ${PORT} ${PORT} ${PORT})
CUDAS=(${CUDA} ${CUDA} ${CUDA} ${CUDA} ${CUDA} ${CUDA} ${CUDA})
MEMO="domainnet_online_constant_lr_logging"
SUB_MEMO="fix_method_constant_lr_logging"

for SEED in 2023
do
    for i in "${!SRC_DOMAINS[@]}"
    do
        CUDA_VISIBLE_DEVICES=${CUDAS[i]} python ../main_adacontrast.py \
        seed=${SEED} port=${PORTS[i]} memo=${MEMO} sub_memo=${SUB_MEMO} project="domainnet-126" \
        data.data_root="/mnt/data" data.workers=8 \
        data.dataset="domainnet-126" data.source_domains="[${SRC_DOMAINS[i]}]" data.target_domains="[${TGT_DOMAINS[i]}]" \
        learn.epochs=1 \
        ckpt_path=False \
        model_src.arch="resnet50" \
        model_tta.src_log_dir=${SRC_MODEL_DIR} \
        learn=targetv1.yaml \
        optim.lr=2e-4
    done
done 