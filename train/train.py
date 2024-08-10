import clip
import copy
import math
import time
import torch
import tqdm

def train_model(args, model, dataloaders, datasetSizes, batchSizes, criterion, optimizer, scheduler, num_epochs=32):
    since = time.time()
    bets_model_wts = copy.deepcopy(model.state_dict())
    best_i2t_acc = 0.0
    best_t2i_acc = 0.0
    all_loss = []
    all_t2i_accuracy = []
    all_i2t_accuracy = []
    
    for epoch in range(num_epochs):
        print(f'Epoch {epoch}/{num_epochs - 1}')
        print('-' * 10)
    
        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode
    
            running_loss = 0.0
            running_i2t_corrects = 0.0
            running_t2i_corrects = 0.0
    
            # Iterate over data.
            for idx, batch in tqdm(enumerate(dataloaders[phase]), total=math.ceil(datasetSizes[phase] / batchSizes[phase])):
                images, categories = batch.values()
                images = images.to(args.device)
                categories = [', '.join(map(str, row)) for row in categories]
                categories = torch.concat([clip.tokenize("An image of " + txt) for txt in categories]).to(args.device)
                # Encode image and text
                image_features = model.encode_image(images)
                text_features = model.encode_text(categories)
    
                # Normalize features
                image_features = image_features / image_features.norm(dim=1, keepdim=True)
                text_features = text_features / text_features.norm(dim=1, keepdim=True)
    
                # Calculate similarity
                logit_scale = model.logit_scale.exp()
                logits_per_image = logit_scale * image_features @ text_features.t()
                logits_per_text = logits_per_image.t()
    
                # Calculate ground truth labels
                ground_truth = torch.arange(len(images)).to(args.device)
                # zero the parameter gradients
                optimizer.zero_grad()
    
                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    #Тут бы logits = (100.0 * image_features @ text_features).softmax(dim=-1)
                    # _, preds = torch.max(outputs, 1)
                    loss_img = criterion(logits_per_image, ground_truth)
                    loss_text = criterion(logits_per_text, ground_truth)
                    loss = (loss_img + loss_text) / 2
    
                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
    
                # statistics
                running_loss += loss.item()
                running_i2t_corrects += torch.sum(logits_per_image.argmax(-1) == ground_truth)
                running_t2i_corrects += torch.sum(logits_per_text.argmax(-1) == ground_truth)
    
            if phase == 'train':
                scheduler.step()
    
            epoch_loss = running_loss / datasetSizes[phase]
            epoch_i2t_acc = running_i2t_corrects.double() / datasetSizes[phase]
            epoch_t2i_acc = running_t2i_corrects.double() / datasetSizes[phase]
    
            print(f'{phase} Loss: {epoch_loss:.4f} Acc i2t: {epoch_i2t_acc:.4f} Acc t2i {epoch_t2i_acc:.4f}')
    
            all_loss.append(epoch_loss)
            all_i2t_accuracy.append(epoch_i2t_acc)
            all_t2i_accuracy.append(epoch_t2i_acc)
    
            # deep copy the model
            if phase == 'val' and (epoch_i2t_acc > best_i2t_acc or epoch_t2i_acc > best_t2i_acc):
                if epoch_i2t_acc > best_i2t_acc:
                    best_i2t_acc = epoch_i2t_acc
    
                if epoch_t2i_acc > best_t2i_acc:
                    best_t2i_acc = epoch_t2i_acc
    
                best_model_wts = copy.deepcopy(model.state_dict())
    
        print()
    
    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc i2t: {best_i2t_acc:4f}')
    print(f'Best val Acc t2i: {best_t2i_acc:4f}')
    
    # load best model weights
    model.load_state_dict(best_model_wts)
    return model
