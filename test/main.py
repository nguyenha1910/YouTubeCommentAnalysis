from YouTubeCommentAnalysis.FileExIm import FileExIm
from YouTubeCommentAnalysis.TextProcessing import TextProcessing
from YouTubeCommentAnalysis.CommentCorpus import CommentCorpus
from YouTubeCommentAnalysis.EmotionAnalysis import EmotionAnalysis
from YouTubeCommentAnalysis.WordAssociation import WordAssociation
import os
from os import path
import pandas as pd
import gensim

process_text = True
emotion_analysis = True
word_association = True

# Raw comment csv file
raw_comment_csv = "sample_1k_1.csv"
cleanText_file = 'result/cleanText_' + raw_comment_csv
dictionary_file = "result/dictionary"

# Create a folder for all files created
result = 'result'
if not path.exists(result):
    os.mkdir(result)

file_processor = FileExIm()

# Process raw comment file
if process_text:
    # Read file
    df = file_processor.read_file(raw_comment_csv)

    # Clean Text
    tp = TextProcessing()
    df['cleanText'] = df.textDisplay.apply(tp.process_text)
    df['cleanText'] = df.cleanText.apply(tp.lemmatize_stemming)

    # Tokenization
    cc = CommentCorpus(list(df.cleanText))
    df['tokens'] = cc.tokenize()
    df['bigrams'] = cc.bigram(min_count=100)
    df['bow'] = cc.bag_of_word()
    dictionary = cc.dictionary(save=True, directory=dictionary_file)

    # Check if english
    df['en'] = df.cleanText.apply(tp.isEnglish)

    # Save current df
    cleanText_dir = 'result/cleanText'
    if not path.exists(cleanText_dir):
        os.mkdir(cleanText_dir)
    file_processor.save_byColumn(df, 'channelId', cleanText_dir)
    df.to_csv(cleanText_file)

# Emotion Analysis for videos
if emotion_analysis:
    ea = EmotionAnalysis()

    # Create directories to store intermediate files
    emotion_analysis_dir = 'result/EmotionAnalysis/'
    # directory to store dataframe with emotion scores
    emo_score_df_dir = "result/EmotionAnalysis/emo_score_df/"
    # directory to store dataframe group by video
    cmt_emo_byvideo = "result/EmotionAnalysis/comment_emotion_byvideo/"
    emo_final = 'result/EmotionAnalysis/emotion_result_' + raw_comment_csv

    if not path.exists(emotion_analysis_dir):
        os.mkdir(emotion_analysis_dir)
    if not path.exists(emo_score_df_dir):
        os.mkdir(emo_score_df_dir)
    if not path.exists(cmt_emo_byvideo):
        os.mkdir(cmt_emo_byvideo)

    # Group comments by channelId
    try:
        groups = df.groupby(by=df.channelId)
    except NameError:  # skip text processing
        df = file_processor.read_file(cleanText_file)
        df = file_processor.eval_col(df, ['cleanText', 'tokens', 'bow'])
        groups = df.groupby(by=df.channelId)

    # Create emotion tokens columns: Only contains emotion tokens
    # Create emotion score columns
    for uid, gr in groups:
        filename = f"{uid}.pickle"
        if not path.exists(f"{emo_score_df_dir}/{filename}"):
            # Get score
            gr = ea.emo_score(gr, 'tokens', 'emo_tokens')
            gr.to_pickle(f'{emo_score_df_dir}{uid}.pickle')

    # Group comments by videos and process the score by video
    # Aggregate dictionary specifies how each column is processed
    # when grouping comments by video
    agg_dict = {
        'channelId': 'first',
        'commentId': list,
        'authorChannelId': list,
        'likeCount': 'sum',
        'totalReplyCount': 'sum',
        'textDisplay': list,
        'cleanText': list,
        'tokens': list,
        'bigrams': list,
        'bow': list,
        'en': list,
        'emo_tokens': list,
        'Positive': 'sum',
        'Negative': 'sum',
        'Anger': 'sum',
        'Anticipation': 'sum',
        'Disgust': 'sum',
        'Fear': 'sum',
        'Joy': 'sum',
        'Sadness': 'sum',
        'Surprise': 'sum',
        'Trust': 'sum'
    }
    for filename in os.listdir(emo_score_df_dir):
        # Only process files that are not in cmt_emo_byvideo folder
        if not path.exists(f"{cmt_emo_byvideo}/{filename}"):
            channel_vid = pd.read_pickle(f"{emo_score_df_dir}/{filename}")
            groupby_video = ea.process_file_byvideo(channel_vid, 'videoId', agg_dict)
            groupby_video.to_pickle(f"{cmt_emo_byvideo}/{filename}")

    # Merge all intermediate video pickles into 1 file
    emo_cmt_vid = file_processor.merge(cmt_emo_byvideo)
    emo_cmt_vid.to_csv(emo_final)

# Word Association for comment corpus
if word_association:
    token = "good"
    # Get id of token in the dictionary
    try:
        dictionary
    except NameError:  # dictionary does not exist
        dictionary = gensim.corpora.Dictionary.load(dictionary_file)

    # Check if df exists
    try:
        df
    except NameError:  # skip text processing
        file_processor = FileExIm()
        df = file_processor.read_file(cleanText_file)
        df = file_processor.eval_col(df, ['tokens', 'bow'])

    # Find PMI score of token
    wa = WordAssociation(dictionary, df.bow)
    pmi_dict = wa.token_pmi(token, threshold=0)
    # Get top keywords
    top_kw = wa.get_top_kw(token, 1)
    # Save top keywords
    file_processor.save_to_txt([str(dictionary[k[0]]) for k in top_kw], f'result/{token}_top_words.txt')
