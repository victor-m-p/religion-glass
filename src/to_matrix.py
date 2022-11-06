import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from helper_functions import fill_grid, assign_id, calc_nodes_samples

# read data
df = pd.read_csv("../data/df_raw.csv")
## subset relevant columns
df = df[["q", "q_id", "answers", "answer_val", "related_parent_q", "entry_name", "entry_id", "end_year"]]
## only overall questions (without parent)
df = df[df["related_parent_q"].isna()]
## assign new id (because their id is not unique)
#df = assign_id(df, "q", "q_id")
## if more than one answer to a question sample 1. 
df = df.sample(frac = 1.0).groupby(['q_id', 'entry_id']).head(1)

conditions = [
    (df['answers'] == "Yes"),
    (df["answers"] == "No"),
    (df['answers'] == "Field doesn't know") | (df["answers"] == "I don't know") | (df['answers'] == "NaN")
]
choices = ["Yes", "No", "DK-NAN"]
df['answer_types'] = np.select(conditions, choices, default="non-binary")

df.groupby('answer_types').size()

## find questions with non-binary answers and remove them
df_ = df.groupby(['q_id', 'answer_types']).size().reset_index(name="count")
df_ = df_[df_["answer_types"] == "non-binary"]
df_ = df.merge(df_, how = "outer", indicator = True)
df_b = df_[(df_._merge=="left_only")].drop("_merge", axis = 1)

## fill with nan 
df_nan = fill_grid(df_b, "q_id", "entry_id", "DK-NAN")
df_nan.groupby('answer_types').size()

## recode values
answer_map = {
    "DK-NAN": 0,
    "Yes": 1,
    "No": -1
}
df_nan = df_nan.assign(answers = df_nan["answer_types"].map(answer_map))
df_nan = df_nan[["entry_id", "q_id", "answers"]]

## to matrix 
df_pivot = df_nan.pivot(
    index = "entry_id",
    columns = "q_id",
    values = "answers")

## to numpy
np_mat = np.array(df_pivot)
np_mat.shape # 835 x 548

## save 
with open(f"matrix/mat_835x548.txt", "w") as txt_file:
    for line in np_mat: 
        txt_file.write(str(line) + "\n")