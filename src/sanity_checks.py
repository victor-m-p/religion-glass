import pandas as pd 
from tqdm import tqdm
import os
import argparse 
#import ndjson
import json
from pathlib import Path
import re
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import itertools package
import itertools
from itertools import permutations

answer_vals = ["No", "Yes", "Field doesn't know", "I don't know"]

# read this (have some problem with dtype in answer_val)
df = pd.read_csv("../data/df_raw.csv")
len(df) # 172.070

# select the columns we will be using 
df_sub = df[["q", "answers", "answer_val", "related_parent_q", "entry_name", "entry_id"]]
df_sub["answers_new"] = df['answers'].apply(lambda x: x if x in answer_vals else 'Other')
sns.countplot(x=df_sub["answers_new"])

# only the overall questions 
df1 = df_sub[df_sub["related_parent_q"].isna()] 
len(df1) # 56.012 (around 30% retained)

# plot this
sns.countplot(x=df1["answers_new"])

## but we have the problem of not answered at all ## 

