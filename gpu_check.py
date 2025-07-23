import torch

print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("Number of GPUs:", torch.cuda.device_count())
    print("Current Device:", torch.cuda.current_device())
    print("PyTorch Version:", torch.__version__)
else:
    print("⚠️ GPU not available, using CPU.")
