import os
import sys


sys.path.append(os.getcwd())
from retrieval.createIndex import CreateModelAndIndex, getIndex
from retrieval.utils import (
    FindNearestImage,
    createModel,
    getDataset,
    searchImage2Image,
    searchImage2Text,
    searchText2Image,
)


def PrintHi():
    print(
        "Hello Woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooorld"
    )


def KostyaDemo():
    model, preprocess, imageIndex, trainDataset = CreateModelAndIndex()
    test_image = trainDataset[0]["image"]
    print(trainDataset[0])
    FindNearestImage(
        test_image,
        model,
        preprocess,
        imageIndex,
        trainDataset,
        upload_dir=f"{os.getcwd()}/end2end_proj/frontend/data",
    )
    # FindNearestImage(test_image, model, preprocess, imageIndex, trainDataset, upload_dir=f"end2end_proj/frontend/data")


def clipWrapper():
    # device = torch.device("cuda:2" if torch.cuda.is_available() else "cpu")
    device = "cpu"
    trainDataset, testDataset = getDataset().values()
    model, preprocess = createModel(device="cpu")
    print("Create Model")
    imageIndex, textIndex = getIndex(
        "retrieval/indexes/imageIndex.bin",
        "retrieval/indexes/textIndex.bin",
        device="cpu",
    )
    print("Create Index")
    test_image = trainDataset[0]["image"]
    test_text = "red dress with neckline"
    k = 3
    # Text2image search
    print("searchText2Image")
    indexes = searchText2Image(imageIndex, test_text, k, model, device=device)[0]
    print(indexes, type(indexes))
    print(trainDataset[indexes])
    for pil_id, pil_image in zip(
        trainDataset[indexes]["image_id"], trainDataset[indexes]["image"]
    ):
        pil_image.save(f"rogov/test/images/{pil_id}.jpg")
    # print(trainDataset[indexes]["image"])
    # image2image search
    print(searchImage2Image(imageIndex, test_image, k, model, preprocess, device=device))
    # Image2Text search
    print(searchImage2Text(textIndex, test_image, k, model, preprocess, device=device))


if __name__ == "__main__":
    # clipWrapper()
    KostyaDemo()
