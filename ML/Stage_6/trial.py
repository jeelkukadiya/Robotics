import torch

# Create a tensor (replace this with your actual tensor) 
my_tensor = torch.tensor([[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]])
#my_tensor=torch.unsqueeze(my_tensor,0)
print(len(my_tensor.shape),my_tensor.shape==torch.Size([5, 3]))