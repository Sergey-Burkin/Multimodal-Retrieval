import torch

class Arguments:
    def __init__(self):
        self.dataset = "detection-datasets/fashionpedia"
        self.outputDir = "embeddings"
        self.embeddingDir = "embeddings"
        self.labelDir = "label_descriptions.json"
        self.trainBatch = 32
        self.valBatch = 25
        self.device = "cuda:2" if torch.cuda.is_available() else "cpu"
        self.modelName = "ViT-B/32"