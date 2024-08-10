import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from arguments import Arguments
from utils import createModel
from data import getDataset, getLabel, ImgAndCtgDataset, customCollateFn
from torch.utils.data import Dataset, DataLoader
from train import train_model

def run(args):
    model_ft, preprocess_ft = createModel()
    criterion = nn.CrossEntropyLoss()
    optimizer_ft = optim.Adam(model_ft.parameters(), lr=0.07)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    train_dataset, val_dataset = getDataset(args.dataset).values()
    labels = getLabel(args.labelDir)
    train_dataset = ImgAndCtgDataset(train_dataset, labels)
    val_dataset = ImgAndCtgDataset(val_dataset, labels)
    train_loader = DataLoader(train_dataset, batch_size=args.trainBatch, shuffle=True, collate_fn=customCollateFn)
    val_loader = DataLoader(val_dataset, batch_size=args.valBatch, shuffle=False, collate_fn=customCollateFn)

    dataloaders = {"train": train_loader, "val": val_loader}
    datasetSizes = {'train': len(train_dataset), 'val': len(val_dataset)}
    batchSizes = {"train": args.trainBatch, "val": args.valBatch}

    model = train_model(model_ft, dataloaders, datasetSizes, batchSizes, criterion, optimizer_ft, exp_lr_scheduler, 3)
    return model


if __name__ == "__main__":
    args = Arguments()
    trained_model = run(args)
