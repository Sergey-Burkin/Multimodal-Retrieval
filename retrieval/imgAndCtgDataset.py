from torch.utils.data import Dataset


class ImgAndCtgDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        image = self.dataset[idx]["image"].convert("RGB")
        categories = list(set(self.dataset[idx]["objects"]["category"]))
        return {"image": image, "categories": categories}
