import importlib_resources
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


class EmotionAnalysis:
    def __init__(self):
        self.emo_df = self.load_emotable()
        self.emo_list = set(self.emo_df.index)

    def load_emotable(self):
        """Return a dataframe containing the following fields:
            en: English words: String
            Positive, Negative, Anger, Anticipation, Disgust, Fear, Joy, Sadness, Surprise, Trust
            Emotion score attribute: integer
        """
        # # DATA_PATH = resources.resource_filename('CommentAnalysis', 'data/NRC-Emotion-Lexicon.xlsx')
        # source = files('CommentAnalysis').joinpath('CommentAnalysis')
        # with as_file('data/NRC-Emotion-Lexicon.csv') as DATA_PATH:
        #     emo_df = pd.read_csv(DATA_PATH)

        with importlib_resources.path('YouTubeCommentAnalysis', "NRC-Emotion-Lexicon.csv") as DATA_PATH:
            emo_df = pd.read_csv(DATA_PATH)
        # emo_df = pd.read_csv(DATA_PATH)
        emo_df = emo_df.set_index('en')
        return emo_df

    def emo_score(self, df, token_col, emo_token_col):
        """Helper method to create emotion token column and
        emotion score columns"""
        # Get emo tokens
        df[emo_token_col] = df[token_col].apply(self.find_emo_tks)
        df[['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust',
            "Sentiment"]] = df[emo_token_col].apply(self.cal_emo_score)
        return df

    def find_emo_tks(self, tks):
        """Extract tokens that are in emotion table"""
        return [x for x in tks if x in self.emo_list]

    def cal_emo_score(self, emo_token_list):
        """This method does the actual calculation to find
        the emotion score of a comment"""
        result = pd.Series(data=[0] * 10,
                           index=['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
                                  'Surprise', 'Trust'])
        for tk in emo_token_list:
            if tk in self.emo_list and self.emo_df.loc[tk].sum() != 0:
                # Have emotion words with non-zero score
                tk_score = pd.Series(self.emo_df.loc[tk])
                result += tk_score  # Add score of the token to the comment
        result["Sentiment"] = self.sentiment(result)
        return result

    def sentiment(self, row, pos_col='Positive', neg_col='Negative'):
        if float(row[pos_col]) > float(row[neg_col]):
            sent = ['Positive']
        elif float(row[pos_col]) < float(row[neg_col]):
            sent = ['Negative']
        else:
            if row[pos_col] + row[neg_col] == 0:
                sent = ['No emo words']
            else:
                sent = ['Neutral']
        return sent

    def normalize(self, row):
        if row.comment_count == 0:
            result = row['Positive':'Trust']
        else:
            result = row['Positive':'Trust'].div(row['comment_count'], axis=0)
        return result

    def process_file_byvideo(self, df, col, aggregate_dict):
        groupby_video = df.groupby(by=col).aggregate(aggregate_dict).sort_values(by='videoId')
        groupby_video['comment_count'] = groupby_video.commentId.apply(len)
        groupby_video[
            ['Positive_score', 'Negative_score', 'Anger_score', 'Anticipation_score', 'Disgust_score', 'Fear_score',
             'Joy_score', 'Sadness_score', 'Surprise_score', 'Trust_score']] = groupby_video.apply(
            self.normalize, axis=1)
        groupby_video['Sentiment'] = self.sentiment(groupby_video, 'Positive_score', 'Negative_score')
        return groupby_video
