import json
import pathlib
import pandas as pd
import tensorflow as tf
from tqdm import tqdm

train = pd.read_csv("train.csv")
text_ids = set(sum(train["pair_id"].str.split("_"), []))

phase = ["test"]

def fetch_dateframe(text_id: str, meta):
    search_results = list(meta.glob(f"*/{text_id}.json"))
    text_path = str(search_results[0])
    try:
        with open(text_path) as f:
            text_json = f.read()
        text_json = json.loads(text_json)
        res_df = pd.json_normalize(text_json)
        res_df["text_id"] = text_id
        return res_df
    except:
        pass


if "train" in phase:
    train = pd.read_csv("train.csv")
    text_ids = list(sum(train["pair_id"].str.split("_"), []))
    meta = pathlib.Path("train")
    print(len(text_ids))
    text_dfs = []
    cnt = 0
    tr = 0
    ex = 0
    for text_id in tqdm(text_ids):
        try:
            res = fetch_dateframe(text_id, meta)
            #res = res.loc[:,["title", "text", "text_id"]]
            text_dfs.append(res)
            print(cnt,"try",tr)
            cnt += 1
            tr += 1
        except:
            print(cnt,"except",ex)
            cnt += 1
            ex += 1
            pass
    text_df = pd.concat(text_dfs).reset_index(drop=True)
    text_df.to_csv("train_dataframe.csv", index=False)
    
if "test" in phase:
    train = pd.read_csv("test.csv")
    text_ids = list(sum(train["pair_id"].str.split("_"), []))
    meta = pathlib.Path("test")
    
    text_dfs = []
    for text_id in tqdm(text_ids):
        try:
            res = fetch_dateframe(text_id, meta)
            text_dfs.append(res)
        except IndexError:
            pass
    text_df = pd.concat(text_dfs).reset_index(drop=True)
    text_df.to_csv("test_dataframe.csv", index=False)