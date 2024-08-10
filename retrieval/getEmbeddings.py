import math
import os

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from retrieval.imgAndCtgDataset import ImgAndCtgDataset
from retrieval.utils import createModel, getDataset


BATCH_SIZE = 1024
OUTPUT_DIR = "retrieval/embeddings"


def customCollateFn(batch):
    model, preprocess = createModel()
    images = [preprocess(item["image"]) for item in batch]
    categories = [item["categories"] for item in batch]
    images = torch.stack(images, dim=0)
    return {"images": images, "categories": categories}


def createEmbeddingsForIndex(device=None):
    train_dataset, _ = getDataset().values()
    customDataset = ImgAndCtgDataset(train_dataset)
    if device is None:
        device = "cuda:2" if torch.cuda.is_available() else "cpu"
    model, preprocess = createModel(device=device)
    dataLoader = DataLoader(
        customDataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=customCollateFn
    )
    for idx, batch in tqdm(
        enumerate(dataLoader), total=math.ceil(len(customDataset) / BATCH_SIZE)
    ):
        images, categories = batch.values()
        with torch.inference_mode():
            images = images.to(device)
            embedding = model.encode_image(images).float().cpu()
        output_path = os.path.join(OUTPUT_DIR, f"batch-{str(idx)}.pkl")
        torch.save({"embeddings": embedding, "categories": categories}, output_path)
