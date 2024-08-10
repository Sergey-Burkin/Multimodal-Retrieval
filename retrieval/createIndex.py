import json
import os

import clip
import faiss
import torch
from tqdm import tqdm

from retrieval.getEmbeddings import createEmbeddingsForIndex
from retrieval.utils import createModel, getDataset


EMBEDDINGS_DIR = "retrieval/embeddings"


def loadEmbeddings(device=None):
    if device is None:
        device = "cuda:2" if torch.cuda.is_available() else "cpu"
    model, _ = createModel(device=device)
    imageEmbeddings = []
    # если отсутствует хотя бы 1 сохраненный батч, то создаем батчи
    if not os.path.isfile("retrieval/embeddings/batch-0.pkl"):
        createEmbeddingsForIndex(device=device)
    all_files = os.listdir(EMBEDDINGS_DIR)
    for embedding_file in tqdm(all_files):
        if ".gitkeep" in embedding_file:
            continue
        stored_embedding = torch.load(f"{EMBEDDINGS_DIR}/{embedding_file}")
        imageEmbeddings.append(stored_embedding["embeddings"])
    imageEmbeddings = torch.cat(imageEmbeddings).numpy()
    faiss.normalize_L2(imageEmbeddings)

    file_path = "./categories.json"
    with open(file_path, "r") as file:
        id2label = json.load(file)
    category = clip.tokenize(["This is " + query for query in id2label.values()]).to(
        device
    )
    with torch.no_grad():
        textEmbeddings = model.encode_text(category.to(device)).detach().cpu().numpy()
    faiss.normalize_L2(textEmbeddings)
    return imageEmbeddings, textEmbeddings


def createIndex(device=None):
    imageEmbeddings, textEmbeddings = loadEmbeddings(device=device)
    d = imageEmbeddings.shape[1]  # размерность вектора
    imageIndex = faiss.IndexFlatIP(d)
    assert imageIndex.is_trained
    imageIndex.add(imageEmbeddings)

    d = textEmbeddings.shape[1]
    textIndex = faiss.IndexFlatIP(d)
    assert textIndex.is_trained
    textIndex.add(textEmbeddings)

    faiss.write_index(imageIndex, "retrieval/indexes/imageIndex.bin")
    faiss.write_index(textIndex, "retrieval/indexes/textIndex.bin")


def getIndex(imageIndexPath, textIndexPath, device=None):
    if not os.path.isfile(imageIndexPath) or not os.path.isfile(textIndexPath):
        createIndex(device=device)
    imageIndex = faiss.read_index(imageIndexPath)
    textIndex = faiss.read_index(textIndexPath)
    return imageIndex, textIndex


def CreateModelAndIndex(root_dir="./"):
    trainDataset, testDataset = getDataset().values()
    model, preprocess = createModel(device="cpu")
    print("Create Model")
    imageIndex, textIndex = getIndex(
        f"{root_dir}/retrieval/indexes/imageIndex.bin",
        f"{root_dir}/retrieval/indexes/textIndex.bin",
        device="cpu",
    )
    print("Create Index")
    return model, preprocess, imageIndex, trainDataset
