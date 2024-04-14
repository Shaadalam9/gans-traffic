import subprocess

# Run test_train.py
try:
    subprocess.run(["python", "new_gen.py"], check=True)
    print("tnew_gen.py ran successfully")
except subprocess.CalledProcessError as e:
    print("Error running test_train.py:", e)

# Run train.py with arguments
train_command = [
    "python", "train.py",
    "--dataroot", "data",
    "--model", "unsup_single",
    "--dataset_mode", "unaligned_scale",
    "--name", "v2c_experiment",
    "--loadSizeW", "542",
    "--loadSizeH", "286",
    "--resize_mode", "rectangle",
    "--fineSizeW", "512",
    "--fineSizeH", "256",
    "--crop_mode", "rectangle",
    "--which_model_netG", "resnet_6blocks",
    "--no_dropout",
    "--pool_size", "0",
    "--lambda_spa_unsup_A", "10",
    "--lambda_spa_unsup_B", "10",
    "--lambda_unsup_cycle_A", "10",
    "--lambda_unsup_cycle_B", "10",
    "--lambda_cycle_A", "0",
    "--lambda_cycle_B", "0",
    "--lambda_content_A", "1",
    "--lambda_content_B", "1",
    "--batchSize", "1",
    "--noise_level", "0.001",
    "--niter_decay", "0",
    "--niter", "80"
]

try:
    subprocess.run(train_command, check=True)
    print("train.py ran successfully")
except subprocess.CalledProcessError as e:
    print("Error running train.py:", e)
