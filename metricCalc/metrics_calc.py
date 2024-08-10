import torch
import numpy as np
import pandas as pd
from tqdm import tqdm



class MetricsCalculator:
    
    def __init__(self, img_embeddings, categories, index, batch_size=1000):
        self.img_embeddings = img_embeddings
        self.index = index
        self.batch_size = batch_size
        self.categories = categories

   
    def compute_precision_at_k(self, predictions, true_categories, k):
        """ function to calculate metric precision at rank k for a query(a image)

        Args:
            predictions (list): list of predicted categories on the image
            true_categories (list): list of correct categories on the image
            k (int): rank for calculate

        Returns:
            precision@k
        """
        relevant_count = sum(1 for p in predictions if p in true_categories)
        precision = relevant_count / k
        return precision
    
    def compute_recall_at_k(self, predictions, true_categories, k):
        """function to calculate metric precision at rank k for a query(a image)

        Args:
            predictions (list): list of predicted categories on the image
            true_categories (list): list of correct categories on the image
            k (int): rank for calculate

        Returns:
            recall@k
        """
        relevant_count = sum(1 for p in predictions if p in true_categories)
        recall = relevant_count / len(true_categories)
        return recall
    
    def dcg_at_k(self, r, k):
        r = np.asfarray(r)[:k]
        if r.size:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        return 0.

    def compute_ndcg_at_k(self, predictions, true_categories, k):
        """function to calculate metric precision at rank k for a query(a image)

        Args:
            predictions (list): list of predicted categories on the image
            true_categories (list): list of correct categories on the image
            k (int): rank for calculate

        Returns:
            ndcg@k
        """
        predictions = np.array(predictions)
        r = np.array([1 if cat in true_categories else 0 for cat in predictions])
        idcg = self.dcg_at_k(sorted(r, reverse=True), k)
        if not idcg:
            return 0.
        return self.dcg_at_k(r, k) / idcg

    def compute_metric(self, metric_name, metric_calc_func, top_k):
        """compute img2text rank metrics

        Args:
            metric_name (str): the name of the metric to calculate
            metric_calc_func (function): funtion to calculate metric
            top_k (int): _description_

        Returns:
            retrieval metric
        """
        _, indices = self.index.search(self.img_embeddings, top_k)
        metric = 0
        for i in tqdm(range(len(self.img_embeddings))):
            metric += metric_calc_func(indices[i], self.categories[i], top_k)
        print(f'{metric_name}@{top_k} = ', metric / len(self.img_embeddings))
        return metric / len(self.img_embeddings)
    
    def recall_calc(self, topk=[1, 5, 7, 10]):
        recall = []
        for k in topk:
            recall_at_k = self.compute_metric("recall", self.compute_recall_at_k, k)
            recall.append(recall_at_k)
        return recall
    
    def precision_calc(self, topk=[1, 5, 7, 10]):
        precision = []
        for k in topk:
            precision_at_k = self.compute_metric("precision", self.compute_precision_at_k, k)
            precision.append(precision_at_k)
        return precision
    
    def ndcg_calc(self, topk=[1, 5, 7, 10]):
        ndcg = []
        for k in topk:
            ndcg_at_k = self.compute_metric("ndcg", self.compute_ndcg_at_k, k)
            ndcg.append(ndcg_at_k)
        return ndcg
    
    def all_metrics_calc(self, topk=[1, 5, 7, 10]):
        return {"recall": self.recall_calc(topk),
                "precision": self.precision_calc(topk),
                "ndcg": self.ndcg_calc(topk)}