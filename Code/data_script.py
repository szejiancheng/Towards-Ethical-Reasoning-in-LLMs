from datasets import load_dataset
import json
import os

def download_ethics_data():
    # Download data from the web
    dataset = load_dataset("hendrycks/ethics", "commonsense", trust_remote_code=True)
    print(dataset['train'])
    dataset['train'].to_json("Code/dataset/ethics_commonsense.json")

if __name__ == "__main__":
    download_ethics_data()