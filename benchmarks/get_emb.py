from datasets import load_dataset
import clip
import torch
import math
import os
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
if not os.path.exists("embeddings"):
    os.makedirs("embeddings")
embeddings = []
OUTPUT_DIR = "./embeddings"
BATCH_SIZE = 1024
dataset = load_dataset("detection-datasets/fashionpedia")
dataset = dataset['train']

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device, jit=False)
model.to(device)
class ImageOnlyDataset(Dataset):
    def __init__(self, data_list):
        self.data_list = data_list
    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, index):
        image = self.data_list[index]['image'].convert('RGB')
        return preprocess(image)

customDataset = ImageOnlyDataset(dataset)
data_loader = DataLoader(customDataset, batch_size=BATCH_SIZE, shuffle=False)
for idx, batch in tqdm(enumerate(data_loader), total=math.ceil(len(dataset) / BATCH_SIZE)):
    images = batch

    with torch.inference_mode():
        images = images.to(device)
        embedding = model.encode_image(images).float().cpu()

    output_path = os.path.join(OUTPUT_DIR, f"batch-{str(idx)}.pkl")
    torch.save({"embeddings": embedding}, output_path)