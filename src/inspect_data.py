import pandas as pd 
from tqdm import tqdm
import os
import argparse 
#import ndjson
import json
from pathlib import Path
import re
import pickle

# write this 
df_raw = pd.read_csv("../data/df_raw.csv")

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