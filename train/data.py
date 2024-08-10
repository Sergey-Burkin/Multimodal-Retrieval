import json
import os
from tqdm import tqdm
import torch
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset
from utils import createModel

def _convert_to_rgb(image):
    return image.convert('RGB')

class ImgAndCtgDataset(Dataset):
    def __init__(self, dataset, mapping):
        self.dataset = dataset
        self.mapping = mapping

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        image = _convert_to_rgb(self.dataset[idx]["image"])
        categories = list(set(self.dataset[idx]["objects"]["category"]))
        categories = [self.mapping[numb] for numb in categories]
        return {"image": image, "categories": categories}

def getDataset(dataset):
    return load_dataset(dataset)

def getLabel(labelDir):
    texts = {}
    with open(labelDir, 'r') as file:
        label_desc = json.load(file)
        for obj in label_desc['categories']:
            text_id = obj['id']
            text = obj['name']
            texts.update({text_id: text})

    return texts

def getTargets(embeddingDir):
    targets = []
    for embedding_file in tqdm(os.listdir(embeddingDir)):
        stored_embedding = torch.load(f"{embeddingDir}/{embedding_file}")
        targets.extend(stored_embedding["categories"])

    return targets

def customCollateFn(batch):
    model, preprocess = createModel()
    images = [preprocess(item["image"]) for item in batch]
    categories = [item["categories"] for item in batch]
    images = torch.stack(images, dim=0)
    return {"images": images, "categories": categories}