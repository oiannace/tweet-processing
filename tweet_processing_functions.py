import nltk
import copy
import re
from nltk.corpus import wordnet

#run the following line once, then it can be commented out
#nltk.download("stopwords")
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')
nltk.download('omw-1.4')


def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def word_tokenize(all_users_tweets, users_following_ids):
    user_tweets_word_tokenize = {}
    for user_id in users_following_ids:
        user_tweets_word_tokenize[user_id] = [nltk.word_tokenize(all_users_tweets[user_id][tweet]) for tweet in range(len(all_users_tweets[user_id]))]
    return user_tweets_word_tokenize

def remove_stopwords(tweets_tokenized, users_following_ids):
    #set is faster to search
    stop_words = set(nltk.corpus.stopwords.words("english"))
    
    tweets_without_stopwords = {}
    for user_id in users_following_ids:
        tweets_without_stopwords[user_id] = copy.deepcopy(tweets_tokenized[user_id])
        for tweet_index in range(len(tweets_without_stopwords[user_id])):
            temp_tweet = tweets_without_stopwords[user_id][tweet_index]
            tweets_without_stopwords[user_id][tweet_index] = [word for word in temp_tweet if not word in stop_words]
    
    return tweets_without_stopwords

def remove_punctuation(original_tweets, users_following_ids):
    user_tweets_no_punc = {}
    
    #regex pattern for only letters and numbers
    regex_pattern = r"[^a-zA-Z0-9\n]"
    
    for user_id in users_following_ids:
        user_tweets_no_punc[user_id] = [re.sub(regex_pattern, " ", original_tweets[user_id][tweet]) for tweet in range(len(original_tweets[user_id]))]
    return user_tweets_no_punc

def word_lemmatizer(user_tweets, pos_tags, users_following_ids):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_tweets = {}
    
    for user_id in users_following_ids:
        lemmatized_tweets[user_id] = copy.deepcopy(user_tweets[user_id])
        for tweet_index in range(len(user_tweets[user_id])):
            lemmatized_tweets[user_id][tweet_index] = [lemmatizer.lemmatize(word,pos_tags[user_id][tweet_index][word]) if (pos_tags[user_id][tweet_index].get(word)) else word for word in user_tweets[user_id][tweet_index]]      
    return lemmatized_tweets

def part_of_speech_tagging(user_tweets_tokenized, users_following_ids):
    pos_tags = {}
    
    for user_id in users_following_ids:
        pos_tags[user_id] = [nltk.pos_tag(user_tweets_tokenized[user_id][tweet_index]) for tweet_index in range(len(user_tweets_tokenized[user_id]))]
    return pos_tags


#function to convert odd list of pos tags to a dictionary for easy lookup for lem

#try to fins a more efficient way to do this
def pos_tags_data_structure_conv(pos_tags, users_following_ids):
    pos_tags_updated = {}
    
    for user_id in users_following_ids:
        pos_tags_updated[user_id] = copy.deepcopy(pos_tags[user_id])
        for tweet_index in range(len(pos_tags[user_id])):
            pos_tags_updated[user_id][tweet_index] =  {}
            for word in pos_tags[user_id][tweet_index]:
                #getting acceptable pos tags for lemmatize function
                lemm_acceptable_pos = get_wordnet_pos(word[1])
                if(lemm_acceptable_pos != ''):
                    pos_tags_updated[user_id][tweet_index][word[0]] = lemm_acceptable_pos
            
    return pos_tags_updated
    
    
    
    
    