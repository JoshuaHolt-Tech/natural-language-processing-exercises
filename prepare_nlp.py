import re
from nltk.corpus import stopwords
from nltk.tokenize.toktok import ToktokTokenizer
import pandas as pd
import numpy as np
import requests
import os
import json
import unicodedata
import nltk


def remove_stopwords(input_string, extra_words=None, exclude_words=None):
    """
    This function takes an input and removes stopwords. You can add or remove words witht the extra_words or exclude_words args.
    """
    
    stopword_list = stopwords.words('english')
    if extra_words != None:
        stopword_list.extend(extra_words)
    if exclude_words != None:
        if type(extra_words) == str:
            stopword_list.remove(exclude_words)
        if type(extra_words) == list:
            for word in exclude_words:
                stopword_list.remove(word)
    words = input_string.split()
    filtered_words = [w for w in words if w not in stopword_list]
    string_without_stopwords = ' '.join(filtered_words)

    return string_without_stopwords


def pandas_stopwords(df, extra_words=None, exclude_words=None):
    """
    This function takes an DataFrame input and removes stopwords from each column.
    You can add or remove words witht the extra_words or exclude_words args.
    """
    for col in df:
        df[col] = df[col].apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words)
    return df

def lemm_pandas(df):
    """
    Lemmatize a panda's DataFrame
    Please do not stem and lemmatize the same string.
    """
    
    #Applies the lemmatize() function to each column
    for col in df:
        df[col] = df[col].apply(lemmatize)
    return df

def lemmatized(input_string):
    """
    Takes an input string and lemmatizes it.
    Please do not stem and lemmatize the same string.
    """
    #Creates the lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    
    #Makes lemmatade
    lemmas = [wnl.lemmatize(word) for word in input_string.split()]
    lemmatized_string = ' '.join(lemmas)
    
    return lemmatized_string

def stemming_pandas(df):
    """
    Does stemming on a panda's DataFrame
    Please do not stem and lemmatize the same string.
    """
    
    #Applies the stemming() function to each column
    for col in df:
        df[col] = df[col].apply(stem)
    return df

def stems(input_string):
    """
    Takes a string and reverts each word to its base stem.
    Please do not stem and lemmatize the same string.
    """
    #Create stemming object
    ps = nltk.porter.PorterStemmer()

    #List comprehension that splits every word to find the stem of it.
    stems = [ps.stem(word) for word in input_string.split()]

    #Joins words back together to form a shadow of the origional
    stemmed_string = ' '.join(stems)
    
    return stemmed_string

def panda_tokens(df):
    for col in df:
        df[col] = df[col].apply(tokenized)
    return df

def tokenized(input_string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(input_string, return_str=True)

def basic_clean(input_string):
    """
    This function takes in a string and applies basic cleaning to it.
    """
    #Changes all characters to their lower case.
    input_string = input_string.lower()
    
    input_string = unicodedata.normalize('NFKD', input_string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    #Removes special characters
    input_string = re.sub(r"[^a-z0-9'\s]", '', input_string)

    return input_string

def cleaning_panda_strings(df):
    """ 
    This function does the cleaning operatins on every column in a dataframe.
    BUG!!! It doesn't allow me to pass in select columns from a df.
    """
    
    for col in df:
        df[col] = df[col].apply(basic_clean)
    return df

def ngrams_creator(input_list, n_grams = 2):
    """
    This function takes in a list and returns a list of grams.
    """
    ngrams = nltk.ngrams(input_list, n_grams)
    return list(ngrams)

