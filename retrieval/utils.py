import clip
import faiss
import numpy as np
import torch
from datasets import load_dataset


def getDataset():
    datasetName = "detection-datasets/fashionpedia"
    dataset = load_dataset(datasetName)
    return dataset


def createModel(device=None):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    modelName = "ViT-B/32"
    model, preprocess = clip.load(modelName, device=device, jit=False)
    model.to(device)
    return model, preprocess


def searchText2Image(index, query, k, model, device=None):
    if device is None:
        device = "cuda:2" if torch.cuda.is_available() else "cpu"
    with torch.inference_mode():
        text = clip.tokenize(["This is " + query])
        text_embedding = model.encode_text(text.to(device)).float().cpu().numpy()
        faiss.normalize_L2(text_embedding)

    _, indexes = index.search(text_embedding, k)
    return indexes


def searchImage2Image(index, query, k, model, preprocess, device=None):
    if device is None:
        device = "cuda:2" if torch.cuda.is_available() else "cpu"
    with torch.inference_mode():
        image = preprocess(query).unsqueeze(0).to(device)
        image_features = model.encode_image(image).float().cpu()
    image_features = np.float32(image_features)
    faiss.normalize_L2(image_features)

    _, indices = index.search(image_features, k)
    return indices


def searchImage2Text(index, query, k, model, preprocess, device=None):
    if device is None:
        device = "cuda:2" if torch.cuda.is_available() else "cpu"
    with torch.inference_mode():
        image = preprocess(query).unsqueeze(0).to(device)
        image_features = model.encode_image(image).float().cpu()
    image_features = np.float32(image_features)
    faiss.normalize_L2(image_features)

    _, indices = index.search(image_features, k)
    return indices


def FindNearestImage(
    test_image, model, preprocess, imageIndex, trainDataset, upload_dir="./"
):
    print(test_image)
    print(type(test_image))
    print("searchText2Image")
    top_k = 3
    indexes = searchImage2Image(
        imageIndex, test_image, top_k, model, preprocess, device="cpu"
    )[0]
    print(indexes, type(indexes))
    print(trainDataset[indexes])
    print("CCCCCCCCC")
    print(upload_dir)
    return trainDataset[indexes]["image_id"], trainDataset[indexes]["image"]
    # for pil_id, pil_image in zip(trainDataset[indexes]['image_id'], trainDataset[indexes]['image']):
    #     print(f"{upload_dir}/{pil_id}.jpg")
    #     pil_image.save(f"{upload_dir}/{pil_id}.jpg")
    # print("END")
