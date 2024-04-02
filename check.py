import torch

# Check if GPU is available
if torch.cuda.is_available():
    print("GPU is available.")
    # Get the name of the GPU
    gpu_name = torch.cuda.get_device_name(0)
    print("GPU Name:", gpu_name)
    # Get the number of available GPUs
    num_gpus = torch.cuda.device_count()
    print("Number of GPUs:", num_gpus)
    # Get the compute capability of the GPU
    gpu_capability = torch.cuda.get_device_capability(0)
    print("Compute Capability:", gpu_capability)
else:
    print("GPU is not available.")
