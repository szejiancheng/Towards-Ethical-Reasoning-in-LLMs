
from datasets import load_dataset
import random

ds = load_dataset("hendrycks/ethics", "commonsense", trust_remote_code=True, split="test")

example = ds.shuffle(seed=12).select(range(2))
print(example[0])
print(example[1])

print(ds.split)
print(ds.info.dataset_name)
print(ds.info.config_name)

ds2 = load_dataset("demelin/moral_stories", "full", trust_remote_code=True, split="train")
example = ds2.shuffle(seed=12).select(range(2))
print(example[0])
print(example[1])

print(ds2.split)
print(ds2.info.dataset_name)
print(ds2.info.config_name)