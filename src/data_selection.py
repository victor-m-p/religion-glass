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
import numpy as np

# read data
df = pd.read_csv("../data/df_raw.csv")

# select the subset of columns we will be using for now
df = df[["q", "answers", "answer_val", "related_parent_q", "entry_name", "entry_id", "end_year"]]

# select only overall questions
df = df[df["related_parent_q"].isna()] 

# create unique q_id (the original q_id is not unique, but q is) 
d_q_id = df.groupby('q').size().reset_index(name="count").sort_values("count", ascending = False)
d_q_id["q_id"] = d_q_id.index
d_q_id = d_q_id[["q", "q_id"]]
df = df.merge(d_q_id, on = "q", how = "inner") 

# if more than one answer per entry and per id then take random answer (small fraction)
df = df.sample(frac = 1.0).groupby(['q_id', 'entry_id']).head(1) 

# nan values for combinations of (q_id, entry_id) that do not have answer
def get_nan(df): 
    d_q_id = df[["q_id"]].drop_duplicates()
    l_q_id = list(d_q_id["q_id"]) 

    d_e_id = df[["entry_id"]].drop_duplicates()
    l_e_id = list(d_e_id["entry_id"]) 

    l_comb = list(itertools.product(l_q_id, l_e_id))
    d_comb = pd.DataFrame(l_comb, columns=["q_id", "entry_id"])

    df = df.merge(d_comb, on = ["q_id", "entry_id"], how = "outer") 
    df = df.fillna('NaN')

    # keeping track
    n_samples = len(df['entry_id'].unique())
    n_nodes = len(df["q_id"].unique())

    return df, n_samples, n_nodes

df_nan, n_samples, n_nodes = get_nan(df)
print(f"number of civilizations (samples): {n_samples}")
print(f"number of questions (nodes): {n_nodes}")

# create column with: (Yes/No), (Don't know), (NaN) and (Other) 
conditions = [
    (df_nan['answers'] == "Yes") | (df_nan["answers"] == "No"),
    (df_nan['answers'] == "Field doesn't know") | (df_nan["answers"] == "I don't know"),
    (df_nan['answers'] == "NaN")
]

choices = ["Yes/No", "Don't know", "NaN"]
df_nan['answers_1'] = np.select(conditions, choices, default="Other Answers")

# create column with: (Other) vs. all known types (yes, no, don't know, nan)
df_nan['answers_2'] = [x if x == "Other Answers" else "Known Answers" for x in df_nan["answers_1"]]

# number of binary questions
df_binary_g = df_nan.groupby(['q_id', 'answers_2']).size().reset_index(name="count").sort_values("count", ascending=False)
df_binary_t = df_binary_g[df_binary_g["count"] == n_samples].drop_duplicates()
n_binary_t = len(df_binary_t)
frac_binary_q = round(n_binary_t/n_nodes, 2)
print(f"N binary questions: {n_binary_t} ({frac_binary_q}%)")

# only use these binary questions going forward
binary_q_id = df_binary_t[["q_id"]]
df_nan_b = df_nan.merge(binary_q_id, on = "q_id", how = "inner")
df_nan_sub = df_nan_b.groupby(['q_id', 'answers_1']).size().reset_index(name = "count")
df_nan_wide = pd.pivot(df_nan_sub, index = "q_id", columns = "answers_1", values = "count").fillna(0)

## number of NA
df_nan_number = df_nan_wide.sort_values('NaN', ascending=True).reset_index()

fig, axes = plt.subplots(1, 2, figsize = (10, 5))
sns.countplot(
    ax = axes[0],
    data = df_nan_b,
    x = "answers_1",
    order = df_nan_b["answers_1"].value_counts().index
)
axes[0].set_title('Dist. of answer types for binary questions')
axes[0].set_xlabel('Answer types')

sns.histplot(
    ax = axes[1],
    x = df_nan_number.index, 
    weights = df_nan_number["NaN"], 
    discrete=True)
axes[1].set_title('N of CIVs not answering Q')
axes[1].set_xlabel('Questions (nodes)')
axes[1].set_ylabel('N CIVs with NaN')

## trying to do the wild thing
### ask Simon
# .... do simple for now .... # 

## over time across questions 
df_entry_answers = df_nan_b.groupby(["entry_id", "answers_1"]).size().reset_index(name = "count")
df_time_wide = pd.pivot(df_entry_answers, index = "entry_id", columns = "answers_1", values = "count").fillna(0)
df_entry_year = df_nan_b[df_nan_b["end_year"] != "NaN"][["end_year", "entry_id"]].drop_duplicates()
df_entry_year = df_entry_year.sample(frac = 1.0).groupby(["entry_id"]).head(1) # not unique year per entry...?!
df_time_wide_x = df_time_wide.merge(df_entry_year, on = "entry_id", how = "inner")

## N cultures over time ## 
sns.histplot(
    x = "end_year",
    data = df_time_wide_x,
    bins = 100
)

## completeness of data over time (grouped by cardinality)
df_time_wide_x["q_cut"] = pd.qcut(df_time_wide_x["end_year"], q = 10)
df_time_wide_x = df_time_wide_x.sort_values('q_cut', ascending=True)

# fractions (not the most pretty)
df_time_wide_x["frac_nan"] = df_time_wide_x["NaN"] / n_binary_t
df_time_wide_x["frac_yn"] = df_time_wide_x["Yes/No"] / n_binary_t 
df_time_wide_x["frac_dk"] = df_time_wide_x["Don't know"] / n_binary_t

# we need new index (not the most pretty)
df_index = df_time_wide_x[["q_cut"]].drop_duplicates()
df_index["index"] = range(10)
df_time_wide_x = df_time_wide_x.merge(df_index, on = "q_cut", how = "inner")

# only factions and long 
df_time_frac = df_time_wide_x[["q_cut", "index", "entry_id", "frac_nan", "frac_yn", "frac_dk"]]

df_time_frac_long = pd.wide_to_long(
    df_time_frac,
    stubnames = "frac",
    i = "entry_id",
    j = "answer",
    sep = "_",
    suffix = r"\w+"
).reset_index()

# prepare plot 
len_id = len(df_time_frac_long[["q_cut"]].drop_duplicates())
x = df_time_frac_long["q_cut"].unique().to_list()
df_time_frac_long["answer"] = df_time_frac_long["answer"].replace(["nan", "dk", "yn"], ["NaN", "Don't know", "Yes/No"])

# plot it 
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data = df_time_frac_long,
    x = "index",
    y = "frac",
    hue = "answer"
)
ax.set_xticks(range(len_id), x)
ax.set_xticklabels(x, rotation = 30)
ax.set_xlabel('Year (equal N of CIVs in each)')
ax.set_ylabel('Fraction of answers')
plt.suptitle("Bias over time")