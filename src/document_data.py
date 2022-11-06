import pandas as pd 
from tqdm import tqdm
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt
import itertools
from itertools import permutations

# read data & select overall questions for now
df = pd.read_csv("../data/df_raw.csv")

# 
def single_size(df, c1, ascending = False): 
    return df.groupby(c1).size().reset_index(name = "count").sort_values("count", ascending = ascending)

def groupby_size(df, c1, c2, ascending = False): 
    df_grouped = df.groupby([c1, c2]).size().reset_index(name = 'count').sort_values('count', ascending = ascending)
    return df_grouped 

def distinct_size(df, c1, c2, ascending = False): 
    df = df[[c1, c2]].drop_duplicates()
    d_c1 = df.groupby(c1).size().reset_index(name = 'count').sort_values("count", ascending = ascending)
    d_c2 = df.groupby(c2).size().reset_index(name = 'count').sort_values("count", ascending = ascending)
    return d_c1, d_c2 

# mapping between entry_id and entry_name is not unique: 
## the pattern is that the same entry name can be entered multiple times
## each entry then has a unique entry_id. 
## these are not actually independent, so we need to decide what to do here. 
## typically same expert but different periods. 
## see e.g. (https://religiondatabase.org/browse/search?q=West%20Bengal,%20India)
e_id, e_name = distinct_size(df, 'entry_id', 'entry_name')
e_id.head(5) # entry_id: is unique 
e_name.head(5) # entry_name: not unique

# mapping not unique between question and question_id: 
## the pattern (generally) is that the same question can be answered multiple times
## for instance "Specify" might be a possible question to answer in multiple locations 
## and each of these instances will have a unique question_id.
## this actually means that I have been doing it wrong.  
q_id, q = distinct_size(df, "q_id", "q")
q_id.head(5) # almost unique
q.head(5) # not unique

## an exception is q_id = 4786 which maps to two questions
## however, these questions do appear to *actually* be the same 
## this appears to be a mistake in the question (or that the question has changed)
## for more on question quality see below
df[df["q_id"] == 4786][["q_id", "q", "entry_id"]].head(5)

## The question "Other" appears multiple times within the same
## entry_id, but with different q_id. 
df[df["q"] == "Other"][["q_id", "q", "entry_id"]].head(5)

df[df["q"] == "Other"].groupby(["q_id", "q", "entry_id"]).size().reset_index(name = "count").sort_values("count", ascending=False)

# mistakes in questions
## we notice lots of issues: 
## spelling mistakes (e.g. "Is this palce a tomb/burial:")
## questions that start with asterisks (e.g. *...)
## these are actual mistakes in the data. 
pd.set_option('display.max_colwidth', None)
q_quality = single_size(df, "q")

## questions with asterisks 
q_quality = q_quality.assign(asterisk = lambda x: x["q"].str.contains("\*"))
q_asterisk = q_quality[q_quality["asterisk"] == True]
q_asterisk = df.merge(q_asterisk, on = "q", how = "inner")[["q", "entry_id", "entry_name", "expert"]]
q_asterisk # entry_id 1025

### do these same questions appear WITHOUT spelling mistakes 
### in other places? Yes, they are! 
q_asterisk_c = pd.DataFrame([re.sub("\*", "", x) for x in q_asterisk["q"]], columns = ["q"])
df_asterisk = df.merge(q_asterisk_c, on = "q", how = "inner")[["q", "entry_id", "entry_name"]]
df_asterisk.head(5)

## questions with spelling 
### harder to detect automatically, so here we
### will just show the problem for one particular case
q_spelling = df[df["q"] == "Is this palce a tomb/burial:"][["q", "q_id", "entry_id", "entry_name", "expert"]]
q_spelling.head(5)
### let's check whether this question exists with correct spelling for other CIVs.
df_spelling = df[df["q"] == "Is this place a tomb/burial:"][["q", "q_id", "entry_id", "entry_name"]]
df_spelling.head(5) # again, yes. 
### the saving grace is question_id. 
df_spelling2 = df[df["q_id"] == 5832][["q", "q_id", "entry_id"]]

## DOUBLE CHECK THAT THE ABOVE SAVES US 
## DOUBLE CHECK "PARENT" QUESTION- FEELS LIKE THERE ARE TOO MANY QUESTIONS.

df.groupby('related_parent_q')


## is this saved by question id? 
import re
re.sub("\*", "", "*this is great")

## questions with spelling mistakes 

q_spelling = df[df["q"] == "*Is education gendered with respect to this text and larger textual tradition?"]
q_spelling["entry_id"]
test = df[df["entry_id"] == 1025]["q"].reset_index()
test.head(10)

q_spelling
# Q unique per entry?
q_e_id = groupby_size(df, 'q', 'entry_id')
q_e_id


# end year not consistent

# only the overall questions 
df1 = df_sub[df_sub["related_parent_q"].isna()] 
len(df1) # 56.012 (around 30% retained)

# only No, Yes, Field doesn't know, I don't know: 
answer_vals = ["No", "Yes", "Field doesn't know", "I don't know"]
df2 = df1.loc[df1['answers'].isin(answer_vals)] 
len(df2) # 51.063 (more than 90% retained)

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