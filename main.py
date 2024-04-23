import subprocess

gen_images = ['python', 'run.py']

train_command = [
    'python', 'train.py',
    '--dataroot', 'path/to/data/',
    '--model', 'unsup_single',
    '--dataset_mode', 'unaligned_scale',
    '--name', 'v2c_experiment',
    '--loadSizeW', '542',
    '--loadSizeH', '286',
    '--resize_mode', 'rectangle',
    '--fineSizeW', '512',
    '--fineSizeH', '256',
    '--crop_mode', 'rectangle',
    '--which_model_netG', 'resnet_6blocks',
    '--no_dropout',
    '--pool_size', '0',
    '--lambda_spa_unsup_A', '10',
    '--lambda_spa_unsup_B', '10',
    '--lambda_unsup_cycle_A', '10',
    '--lambda_unsup_cycle_B', '10',
    '--lambda_cycle_A', '0',
    '--lambda_cycle_B', '0',
    '--lambda_content_A', '1',
    '--lambda_content_B', '1',
    '--batchSize', '1',
    '--noise_level', '0.001',
    '--niter_decay', '0',
    '--niter', '2'
]

test_command = [
    'python', 'test.py',
    '--dataroot', 'path/to/data/',
    '--model', 'unsup_single',
    '--dataset_mode', 'unaligned_scale',
    '--name', 'v2c_experiment',
    '--loadSizeW', '512',
    '--loadSizeH', '256',
    '--resize_mode', 'rectangle',
    '--fineSizeW', '512',
    '--fineSizeH', '256',
    '--crop_mode', 'none',
    '--which_model_netG', 'resnet_6blocks',
    '--no_dropout',
    '--which_epoch', '2'
]

merge_frames = ['python', 'merge_frames.py']

try:
    # Run image generation script
    subprocess.run(gen_images, check=True)
    print("Video has been decomposed into frames.")

    # Run training command
    subprocess.run(train_command, check=True)
    print("Training completed successfully.")

    # Run testing command
    subprocess.run(test_command, check=True)
    print("Testing completed successfully.")

    # Run testing command
    subprocess.run(merge_frames, check=True)
    print("File ran sucessfully.")

except subprocess.CalledProcessError as e:
    print("Error occurred:", e)
