import clip
import torch

def createModel():
    device = "cuda:2" if torch.cuda.is_available() else "cpu"
    modelName = "ViT-B/32"
    model, preprocess = clip.load(modelName, device=device, jit=False)
    model.to(device)
    return model, preprocess