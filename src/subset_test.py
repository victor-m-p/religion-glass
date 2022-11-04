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
import torch
import torch.utils.data
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torchvision import datasets, transforms
from torchvision.utils import make_grid , save_image
import matplotlib.pyplot as plt
# import itertools package
import itertools
from itertools import permutations

### issue: end_year not consistent ###
n_sub = 400

# read this (have some problem with dtype in answer_val)
df = pd.read_csv("../data/df_raw.csv")
len(df) # 172.070

# select the columns we will be using 
df_sub = df[["q", "answers", "answer_val", "related_parent_q", "entry_name", "entry_id"]]

# only the overall questions 
df1 = df_sub[df_sub["related_parent_q"].isna()] 
len(df1) # 56.012 (around 30% retained)

# only No, Yes, Field doesn't know, I don't know: 
answer_vals = ["No", "Yes", "Field doesn't know", "I don't know"]
df2 = df1.loc[df1['answers'].isin(answer_vals)] 
len(df2) # 51.063 (more than 90% retained)

# assign each q to an index (q_id is inconsistent)
d_q_id = df2.groupby('q').size().reset_index(name="count").sort_values("count", ascending = False)
d_q_id_20 = d_q_id[d_q_id["count"] >= n_sub].reset_index(drop = True)
d_q_id_20["q_id"] = d_q_id_20.index
d_q_id_20 = d_q_id_20[["q", "q_id"]]

# joing back only those 
df3 = df2.merge(d_q_id_20, on = "q", how = "inner")
len(df3) # 29.854 (>50% retained)

# sample randomly if more than one answer per question for each entry. (slow)
df4 = df3.groupby(['q_id', 'entry_id'], group_keys=False).apply(lambda x: x.sample(1))
len(df4) # 29.621 (almost all retained)

# put this into matrices 
## https://yizhepku.github.io/2020/12/26/dataloader.html
## can be dictionary, numpy array, etc. 

# actually we have to construct the list for all of them..
d_q_id = df4[["q_id"]].drop_duplicates()
l_q_id = list(d_q_id["q_id"]) # n = 63

d_e_id = df4[["entry_id"]].drop_duplicates()
l_e_id = list(d_e_id["entry_id"]) # n = 746

l_comb = list(itertools.product(l_q_id, l_e_id))
d_comb = pd.DataFrame(l_comb, columns=["q_id", "entry_id"])

# outer join with data and fill with some value
# for now we will just fill with NA. 
df5 = df4.merge(d_comb, on = ["q_id", "entry_id"], how = "outer")
len(df5) # 46.998
len(d_comb) # 46.998 

''' pivot then '''
df6 = pd.pivot(df5, index = "entry_id", columns = "q_id", values = 'answer_val')
len(df6) # rows (religions): 746
len(df6.columns) # columns (questions): 63

''' reproduce issue for simon: put in inspect data '''

# read this 
df = pd.read_csv("../data/df_raw.csv")

# only the overall questions 
df1 = df[df["related_parent_q"].isna()] 

# only No, Yes, Field doesn't know, I don't know: 
answer_vals = ["No", "Yes", "Field doesn't know", "I don't know"]
df2 = df1.loc[df1['answers'].isin(answer_vals)] # >90% retained

### so some question ids must have the same question name?
d_q_id_name = df2[["q_id", "q", "poll"]].drop_duplicates()
d_q_id_name.groupby('q').size().reset_index(name = "count")

test = df2[df2["q"] == "Was the place thought to have originated as the result of divine intervention:"]
test2 = test[["q", "q_id", "entry_name", "poll"]]
test2

test_qs = df2.groupby(["q", "entry_id"]).size().reset_index(name="count").sort_values("count",ascending=False)
test_qs
## for some they just answer YES a lot of times (and give various notes).
## i.e. if there are multiple temples, they will answer YES a lot of times
## and give different notes... 
d_dup = df2[df2["entry_id"] == 1230]
d_dup[["entry_name"]]
d_test = d_dup[d_dup["q"] == "Are there structures or features present:"]
d_test

# No = 0
# Yes = 1
# Field doesn't know = -1
# I don't know = -1 
# A state = -1 or 4, ...

## how many questions in total?
df_q_n = df_count(df_raw, "q")
len(df_q_n) # 1672 total Q.

## how many overall questions
df_overall = df_raw[df_raw["related_parent_q"].isna()]
df_q_n_o = df_count(df_overall, "q")
len(df_q_n_o) # 287 overall Q. 
df_q_n_o.head(50)
df_q_n_o.tail(20)

# compile ACTUAL list of qusetions
questions = []

## check rare questions (under testing...) ## 
## has to just be manual cleaning ... ## 
df_overall = df_overall.assign(contains_star = lambda x: x["q"].str.contains("\*"))
df_tst = df_overall[df_overall["contains_star"] == True]
df_tst

df_raw.head(5)
df_taiping = df_raw[df_raw["entry_name"] == "Taiping jing"]
df_taiping_main = df_taiping[df_taiping["related_parent_q"].isna()]
df_taiping_main.head(5)

## how many questions in total (unique) ## 


# print sources: answer_val: actual answer: 1
# methods of composition: Written (-1) -- has sub.
df_test[df_test["q"] == "Methods of Composition"]

# test some stuff
def df_count(df, col): 
    df_count = df.groupby(col).size().reset_index(name="count").sort_values("count", ascending=False)
    return df_count

## related question id 
d_related_q_id = df_count(df_raw, "related_q_id")
d_related_q_id.head(5) # not equal amount

## related question 
d_related_q = df_count(df_raw, "related_q")
d_related_q.head(5)

## answers (fucked)
d_answers = df_count(df_raw, "answer_val")
d_answers.head(5) # all sorts of answers

# ENTRIES
## entries (fucked)
d_entry_n = df_count(df_raw, "entry_name") # did not work
d_entry_n.head(5) # not equal
len(d_entry_n) # 799

## entries and entry_id
### entry_name is not unique 
d_entry2 = df_count(df_raw, ["entry_name", "entry_id"])
d_entry2.head(5) # not equal
len(d_entry2) # 838
d_donat = d_entry2[d_entry2["entry_name"] == "Donatism"]

## entry_id 
### entry_id does appear to be unique
d_entry_id = df_count(df_raw, "entry_id")
d_entry_id # not equal
len(d_entry_id)

# CHECK MOST COMPLETE (longest)
## Print Sources: printed sources used to understand religion (val: 1)
## Methods of Composition: (val: -1?)
df_raw.columns
d_taiping_jing = df_raw[df_raw["entry_name"] == "Taiping jing"]
d_taiping_jing = d_taiping_jing[["related_q", "related_parent_q", "poll", "q", "answers", "answer_val"]]
d_taiping_jing

## 
tmp = df_raw[df_raw["entry_name"] == "Islamic modernists"]

d_taiping_jing.columns
d_taiping_jing.groupby("answer_val").size()
d_taiping_jing[["end_year"]]
d_taiping_jing.dtypes

# Column overview
## related questions
### related_q: the sub-header, not useful I think

## parent questions

## questions / answers
### q (str): the questions (e.g. Print Sources, Methods of Composition)
### q_id (int): the question id (several one can appear multiple times, e.g. several printed sources)
### answers (string): the qualitative (written) response (can be yes/no)
### answer_val (string): e.g. 0, 1, -1, etc. 

## time 
### end_year <int>: but not consistent within
### start_year <int>: but not consistent
### date_range <str>: start and end year. 

## misc
### brancing_q (str): status of readership (at least in one)

## entry
### entry_desc (str): in at least some cases comprehensive and cool. 
### entry_tags (str): not sure what this is. 
### entry_src (str): e.g. DRH
### entry_id (int): the id of the entry
### entry_name (str): the name of the religion

## region columns
### region (tricky because it can change name over time, e.g. shangong --> people's republic of china)
#### region_tags (string): can be extracted, but in funky format. 
#### region_desc (str): probably not useful. 
#### region_id (int): id for region 
#### region_name (str): name of region 