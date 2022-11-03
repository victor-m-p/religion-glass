import pandas as pd 
from tqdm import tqdm
import os
import argparse 
#import ndjson
import json
from pathlib import Path
import re
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import itertools

# read data
df = pd.read_csv("../data/df_raw.csv")

# select the columns we will be using 
df = df[["q", "answers", "answer_val", "related_parent_q", "entry_name", "entry_id"]]

# overall number of C and N
len(df["q"].unique()) # 1672
len(df["entry_id"].unique()) # 838

# the answers we currently understand
answer_vals = ["No", "Yes", "Field doesn't know", "I don't know"]

# select the columns we will be using 
df["answers_new"] = df['answers'].apply(lambda x: x if x in answer_vals else 'Other Values')

# only the overall questions 
df_o = df[df["related_parent_q"].isna()] 

######### plot answers ##########
def plot_double(d1, d2, col, t1, t2, rot, xlabel, fname): 
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    # all questions
    sns.countplot(
        ax = axes[0],
        x = col,
        data = d1,
        order = d1[col].value_counts().index)
    axes[0].set_title(t1)
    axes[0].set_xlabel(xlabel)
    axes[0].set_xticklabels(d1[col].value_counts().index, rotation = rot)
    # overall questions
    sns.countplot(
    ax = axes[1],
    x = col,
    data = d2,
    order = d2[col].value_counts().index)
    axes[1].set_title(t2)
    axes[1].set_xlabel(xlabel)
    axes[1].set_xticklabels(d2[col].value_counts().index, rotation = rot)
    plt.tight_layout()
    plt.savefig(f"figs/{fname}.jpeg")

plot_double(
    df, 
    df_o, 
    "answers_new", 
    "All Questions", 
    "Overall Questions", 
    30, 
    "Answers",
    "answer_types")

######## what is in other ###########
n = 5
c1 = 15
c2 = 20

df_other = df[df["answers_new"] == "Other Values"]
df_o_other = df_o[df_o["answers_new"] == "Other Values"]

df_other_g = df_other.groupby("answers").size().reset_index(name="count").sort_values("count", ascending=False)
df_o_other_g = df_o_other.groupby("answers").size().reset_index(name="count").sort_values("count", ascending=False)

df_other_lst = df_other_g["answers"].head(n).values.tolist()
df_o_other_lst = df_o_other_g["answers"].head(n).values.tolist()

df_other["other_answers"] = df_other['answers'].apply(lambda x: x if x in df_other_lst else 'Other Values')
df_o_other["other_answers"] = df_o_other['answers'].apply(lambda x: x if x in df_o_other_lst else 'Other Values')

df_other_10 = df_other[df_other["other_answers"] != "Other Values"]
df_o_other_10 = df_o_other[df_o_other["other_answers"] != "Other Values"]

df_other_10["other_answers_c"] = df_other_10["other_answers"].apply(lambda x: x[0:c1] + " [...]" if len(x) > c2 else x)
df_o_other_10["other_answers_c"] = df_other_10["other_answers"].apply(lambda x: x[0:c1] + " [...]" if len(x) > c2 else x)

df__other_10 = df_other_10.fillna("NaN")
df_o_other_10 = df_o_other_10.fillna("NaN")

plot_double(
    df_other_10, 
    df_o_other_10, 
    "other_answers_c", 
    "All Questions", 
    "Overall Questions", 
    45, 
    "Answers (Other)",
    "other_types")

########## with the NANs ###########
### assign unique ID to each question
d_q_id = df.groupby('q').size().reset_index(name="count").sort_values("count", ascending = False)
d_q_id["q_id"] = d_q_id.index
d_q_id = d_q_id[["q", "q_id"]]
df_no_cut = df.merge(d_q_id, on = "q", how = "inner") # 172.070
df_no_cut = df_no_cut.sample(frac = 1.0).groupby(['q_id', 'entry_id']).head(1) # 165.136

### overall (no subsetting) ### 
# https://yizhepku.github.io/2020/12/26/dataloader.html
def get_nan(df): 
    d_q_id = df[["q_id"]].drop_duplicates()
    l_q_id = list(d_q_id["q_id"]) # n = 1672

    d_e_id = df[["entry_id"]].drop_duplicates()
    l_e_id = list(d_e_id["entry_id"]) # n = 838

    l_comb = list(itertools.product(l_q_id, l_e_id))
    d_comb = pd.DataFrame(l_comb, columns=["q_id", "entry_id"])

    df = df.merge(d_comb, on = ["q_id", "entry_id"], how = "outer") # 1.401.136
    df = df.fillna('NaN')
    answer_vals = ["No", "Yes", "Field doesn't know", "I don't know", "NaN"] 
    df["answers_new"] = df['answers'].apply(lambda x: x if x in answer_vals else 'Other Values')
    
     # keeping track
    n_samples = len(df['entry_id'].unique())
    n_nodes = len(df["q_id"].unique())

    return df, n_samples, n_nodes

# preparation
df_o_no_cut = df_no_cut[df_no_cut["related_parent_q"].isna()]

df_no_cut_nan, no_cut_nan_samples, no_cut_nan_nodes = get_nan(df_no_cut)
df_o_no_cut_nan, no_cut_o_nan_samples, no_cut_o_nan_nodes = get_nan(df_o_no_cut)

plot_double(
    df_no_cut_nan, 
    df_o_no_cut_nan, 
    "answers_new", 
    f"All Questions (s: {no_cut_nan_samples}, n: {no_cut_nan_nodes})", 
    f"Overall Questions (s: {no_cut_o_nan_samples}, n: {no_cut_o_nan_nodes})", 
    30, 
    "Answers",
    "with_nan")

### if we apply a cutoff ###
def df_cut(df, cutoff): 
    d_q_id = df.groupby('q').size().reset_index(name="count").sort_values("count", ascending = False)
    d_q_id_cut = d_q_id[d_q_id["count"] >= cutoff].reset_index(drop = True)
    d_q_id_cut["q_id"] = d_q_id_cut.index
    d_q_id_cut = d_q_id_cut[["q", "q_id"]]
    df_cut = df.merge(d_q_id_cut)
    df_cut = df_cut.sample(frac = 1.0).groupby(['q_id', 'entry_id']).head(1)
    
    # keeping track
    n_samples = len(df_cut['entry_id'].unique())
    n_nodes = len(df_cut["q_id"].unique())

    return df_cut

df_cut_50 = df_cut(df, 50) # 150.542 rows, 
df_cut_300 = df_cut(df, 300) # 54.490 rows, 

df_cut_50_nan, samples_cut_50, nodes_cut_50 = get_nan(df_cut_50)
df_cut_300_nan, samples_cut_300, nodes_cut_300 = get_nan(df_cut_300)

# NB: some religions here might still have predominantly NA
# might also want to subset based on religions (i.e. each sample needs to contain x number of answers). 
plot_double(
    df_cut_50_nan, 
    df_cut_300_nan, 
    "answers_new", 
    f"cutoff = 50 (s: {samples_cut_50}, n: {nodes_cut_50})", 
    f"cutoff = 300 (s: {samples_cut_300}, n: {nodes_cut_300})", 
    30, 
    "Answers",
    "with_nan_cutoff")

#### most common nodes (N) and Civilizations (C) ####
df_cut_300_nan["entry_id_str"] = df_cut_300_nan["entry_id"].map(str)
df_cut_300_nan["entry"] = df_cut_300_nan[["entry_id_str", "entry_name"]].agg("-".join, axis = 1)

df_cut_300_N = df_cut_300_nan.groupby('q').size().reset_index(name = "count").sort_values("count", ascending = False)
df_cut_300_nan.head(10) 
df_cut_300_x_N = df_cut_300_N[df_cut_300_N["q"] != "NaN"]
df_cut_300_x_N.tail(10)

df_cut_300_C = df_cut_300_nan.groupby('entry').size().reset_index(name = "count").sort_values("count", ascending = False)
df_cut_300_C.head(10) # lot of C with only 1 not NaN

df_cut_300_nan_x = df_cut_300_nan[df_cut_300_nan["entry_name"] != "NaN"]
df_cut_300_x_C = df_cut_300_nan_x.groupby('entry').size().reset_index(name = "count").sort_values("count", ascending = False)
df_cut_300_x_C.head(10) # the C with most questions not NaN. 

def plot_double_hist(d1, d2, col, t1, t2, n, fname): 
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    # all questions
    sns.histplot(
        ax = axes[0],
        x = col,
        data = d1,
        bins = n)
    axes[0].set_title(t1)
    # overall questions
    sns.histplot(
        ax = axes[1],
        x = col,
        data = d2,
        bins = n)
    axes[1].set_title(t2)
    plt.tight_layout()
    plt.savefig(f"figs/{fname}.jpeg")

plot_double_hist(
    df_cut_300_x_N, 
    df_cut_300_x_C, 
    "count", 
    "number of C answering each Q (max = 835)", # some error here 
    "non NaN answers by C (max = 138)",
    50,
    "C_and_N")

### answer types over time ### 


#### distribution 

### make it ready for MPF ### 
# pd.pivot(df, index = "entry_id", columns = "q_id", values = 'answer_val')

### other things ### 

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