import os
import faiss
from tqdm import tqdm
import torch
EMBEDDINGS_DIR = "embeddings"
if not os.path.exists("ind"):
    os.makedirs("ind")
embeddings = []

all_files = os.listdir(EMBEDDINGS_DIR)
for embedding_file in tqdm(all_files):
    stored_embedding = torch.load(f"{EMBEDDINGS_DIR}/{embedding_file}")
    embeddings.append(stored_embedding["embeddings"])

embeddings = torch.cat(embeddings).numpy()
faiss.normalize_L2(embeddings)
# Получаем размерность эмбеддинга
d = embeddings.shape[1] 

# Строим брутфорс индекс
index = faiss.IndexFlatIP(d)
assert index.is_trained
index.add(embeddings)
# Сохраняем индекс
faiss.write_index(index, "ind/bruteforce_index.bin")

# создаем IVF индекс (baseline)
nlists = [2**j for j in range(9)]
quantizer = faiss.IndexFlatIP(d)  # the other index
for nlist in nlists:
    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_INNER_PRODUCT)
    assert not index.is_trained
    index.train(embeddings)
    assert index.is_trained
    index.add(embeddings)
    faiss.write_index(index, f"ind/IVF_flat_{nlist}.bin")
#создаем индекс HNSW no scalar
efConstruction = 40 # Параметр для построения графа
index = faiss.IndexHNSWFlat(d, 128, faiss.METRIC_INNER_PRODUCT)
index.hnsw.efConstruction = efConstruction

assert index.is_trained
index.add(embeddings)
faiss.write_index(index, f"ind/HNSW.bin")
# создаем индекс HNSW no scalar
# for neighbour in neighbours:
#     index = faiss.IndexHNSWSQ(d, faiss.ScalarQuantizer.QT_8bit, neighbour)
#     index.train(embeddings)
#     index.hnsw.efConstruction = 40
#     index.add(embeddings)
#     faiss.write_index(index, f"indexes/HNSW_sq_{neighbour}.bin")



