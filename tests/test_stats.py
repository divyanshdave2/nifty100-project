import os
from src.analytics.cluster_stats import generate_cluster_stats_and_outliers

def test_stats_execution():
    generate_cluster_stats_and_outliers()
    assert os.path.exists("reports/correlation_heatmap.png")
    assert os.path.exists("output/outlier_report.csv")
    assert os.path.exists("output/portfolio_stats.csv")