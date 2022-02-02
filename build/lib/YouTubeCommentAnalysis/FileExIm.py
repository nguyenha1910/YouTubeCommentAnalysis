import ast
import pandas as pd
import os
from os import path
import pickle5 as pickle
import warnings

warnings.filterwarnings("ignore")

class FileExIm:
    def __init__(self):
        pass

    def read_file(self, filename):
        """Read file (csv, pickle, or folder of pickles)
        and return a dataframe object"""
        if filename.endswith(".pickle"):
            df = pd.read_pickle(filename)
        elif filename.endswith(".csv"):
            df = pd.read_csv(filename)
        else:
            df = self.merge(filename)
        return df

    def merge(self, directory):
        df = pd.DataFrame()
        for pickle_file in os.listdir(directory):
            try:
                sub_df = pd.read_pickle(f'{directory}/{pickle_file}')
            except ValueError:  # pickle protocol 5
                with open(f'{directory}/{pickle_file}', "rb") as p:
                    sub_df = pickle.load(p)
            df = df.append(sub_df)
        return df

    def save_byColumn(self, dataframe, column, directory):
        """Save dataframe by grouping the selected column
        each group is saved as a pickle
        All pickles are contained in the selected directory"""
        if not path.exists(directory):
            os.mkdir(directory)
        groups = dataframe.groupby(by=dataframe[column])
        for uid, gr in groups:
            gr.to_pickle(f'{directory}/{uid}.pickle')
        return 0

    def save_GroupBy(self, groupBy, directory):
        """Save groupBy object as multiple pickles file
        Each pickle file belong to a unique group
        All pickles file are contained in specified directory"""
        if not path.exists(directory):
            os.mkdir(directory)
        for uid, group in groupBy:
            filename = f"{uid}.pickle"
            group.to_pickle(f"{directory}/{filename}", compression='infer', protocol=4)
        return 0

    def eval_col(self, df, col_list):
        """Literally evaluate columns specified of the dataframe"""
        for col in col_list:
            df[col] = df[col].apply(ast.literal_eval)
        return df

    def merge_columns(self, df1, df2, id='commentId'):
        """From df1 and df2, create a new df
        with all columns from df1 and df2"""
        if len(df1) != len(df2):
            raise ValueError('2 dataframes do not have same length')
        df1 = df1.sort_values(by=[id])
        df2 = df2.sort_values(by=[id])
        if list(df1.id) != len(df2.id):
            raise ValueError(f'2 dataframes do not have same key column {id}')
        merge_df = df1.copy(deep=True)
        # Cloning columns
        for col in df2.columns:
            if col not in merge_df.columns:
                merge_df[col] = df2[col]
        return merge_df

    def save_to_txt(self, alist, filename='Untitled'):
        with open(filename, 'a+', encoding='utf-8') as file:
            for word in alist:
                file.write(word + "\n")
        file.close()
