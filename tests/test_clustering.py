import os
from src.analytics.clustering import run_kmeans_clustering

def test_clustering_execution():
    run_kmeans_clustering()
    assert os.path.exists("output/cluster_labels.csv")
    assert os.path.exists("reports/elbow_plot.png")