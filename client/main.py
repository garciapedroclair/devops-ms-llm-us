import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

def BoxPlot(endpoint):
    load_dotenv()
    response = requests.get(os.getenv("API_URL") + endpoint)
    response.raise_for_status() 
    data = response.json()
    time_llm_true = data.get("time_llm_true", [])
    time_llm_false = data.get("time_llm_false", [])
    plt.figure(figsize=(8,6))
    plt.boxplot(
        [time_llm_true, time_llm_false],
        tick_labels=["YES", "NO"],
        patch_artist=True,
        boxprops=dict(facecolor='#4f46e5', color='#4f46e5'),
        medianprops=dict(color='yellow', linewidth=2),
        whiskerprops=dict(color='#4f46e5'),
        capprops=dict(color='#4f46e5'),
        flierprops=dict(marker='o', markerfacecolor='red', markersize=6, linestyle='none')
    )
    plt.title("Task Time vs LLM Usage")
    plt.ylabel("LLM Usage")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("./figs/boxplot_llm.png")

BoxPlot("/tasks/stats_time_llm")