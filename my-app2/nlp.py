# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import nltk
from nltk.corpus import stopwords
import pandas as pd
import re
import string

print ("hello world1")

print ("hello world2")

rawData = open("/home/rajiv/Downloads/MyTechVideos/code/SMSSpamCollection.tsv").read()

rawData[0:500]

parsedData = rawData.replace("\t","\n").split("\n")

parsedData[0:10]
labelList=parsedData[0::2]
textList=parsedData[1::2]
sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""

nltk.download('punkt')
nltk.download()
tokens = nltk.word_tokenize(sentence)


stopwords.words("english")[0:500:51]

dir(nltk)

myList=[1,2,3,4,5,6]

myList[0:5:4]
myList[0::2]


rawData[0:500]
labelList[0:10]
textList[0:10]

print(len(labelList))
print(len(textList))

print(labelList[-5:])
print(textList[-5:])

fullCorpus = pd.DataFrame({"label" : labelList[:-1] , "body_list" : textList})
fullCorpus.head(11)
dataset = pd.read_csv("/home/rajiv/Downloads/MyTechVideos/code/SMSSpamCollection.tsv",sep="\t",header=None)
dataset.head()

fullCorpus= pd.read_csv("/home/rajiv/Downloads/MyTechVideos/code/SMSSpamCollection.tsv",sep="\t",header=None)
fullCorpus.columns = ['label','body_text']
fullCorpus.head()
len(fullCorpus[fullCorpus['label']=='spam'])
len(fullCorpus[fullCorpus['label']=='ham'])
fullCorpus['label'].isnull().sum()
fullCorpus['body_text'].isnull().sum()

fullCorpus['body_text'][0:2]
re_test = fullCorpus['body_text'][0]
re.findall("\S+",re_test)

dir(pd)
pd.set_option('display.max_colwidth',100)

fullCorpus= pd.read_csv("/home/rajiv/Downloads/MyTechVideos/code/SMSSpamCollection.tsv",sep="\t",header=None)
fullCorpus.head()
data=fullCorpus
data['body_text'].head()
stopword = nltk.corpus.stopwords.words('english')

def remove_punct(text):
    text_nopunct="".join([char for char in text if char not in string.punctuation])
    return text_nopunct

def tokenize(text):
    tokens=re.split('\W+',text)
    return tokens

def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopword]
    return text


data['body_text_clean'] = data['body_text'].apply(lambda x:remove_punct(x))
data['body_text_tokenized'] = data['body_text_clean'].apply(lambda x:tokenize(x))
data['body_text_nostop']=data['body_text_tokenized'].apply(lambda x : remove_stopwords(x))

data.head()

