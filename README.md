# YouTubeCommentAnalysis

## Installation
``pip install YouTubeCommentAnalysis``

## Example usage
```
raw_comment_csv = "sample_1k_1.csv"
# Read file
file_processor = FileExIm()
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

# Emotion Analysis
ea = EmotionAnalysis()
df = ea.emo_score(df, 'tokens', 'emo_tokens')
agg_dict = {
        'channelId': 'first',
        'commentId': list,
        'cleanText': list,
        'tokens': list,
        'bigrams': list,
        'bow': list,
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
groupby_video = ea.process_file_byvideo(channel_vid, 'videoId', agg_dict)
groupby_video.to_pickle(f'result_dir/emotion_analysis{raw_comment_csv}')

# Word Association
token = 'hello'
wa = WordAssociation(dictionary, df.bow)
pmi_dict = wa.token_pmi(token, threshold=10)
top_kw = wa.get_top_kw(token, 0.1) # Get top keywords
# Save top keywords
file_processor.save_to_txt([str(dictionary[k[0]]) for k in top_kw], f'result/{token}_top_words.txt')

# Save current df with muitple pickles,
# Each pickle represent unique channelId
file_processor.save_byColumn(df, 'channelId', 'result_dir')
df.to_csv(cleanText_file)
```

## Changelog
### ``Version 0.0.1 ``

First version includes Comment Text Processing, Emotion Analysis, and Word Association.
This version is tested and okay to use.
