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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.model_selection import train_test_split


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
fullCorpus.columns = ['label','body_text']
fullCorpus.head()
#data=fullCorpus[0:15]
data=fullCorpus
data['body_text'].head(20)
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

def clean_text(text):
    text="".join([char for char in text if char not in string.punctuation])
    tokenized_list =re.split('\W+',text)
    text = [word for word in tokenized_list if word not in stopword]
    return text

def count_punct(text):
    count = sum([1 for char in text if char in string.punctuation])
    return round(count/(len(text) - text.count(" ")),3) * 100



data['body_text_clean'] = data['body_text'].apply(lambda x:remove_punct(x))
data['body_text_tokenized'] = data['body_text_clean'].apply(lambda x:tokenize(x))
data['body_text_nostop']=data['body_text_tokenized'].apply(lambda x : remove_stopwords(x))

data.head()

###############################################################################
##
##Vectorizing
##Feature vector
##
###############################################################################

#new_data = data.head(15)
new_data = data
len(new_data)
new_data['body_text']
new_data.head()
stopword = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()

new_data['body_text_cleaned']=new_data['body_text'].apply(lambda x : clean_text(x))

new_data1=new_data['body_text'].apply(lambda x : clean_text(x))
new_data1

count_vect = CountVectorizer(analyzer=clean_text)
X_counts = count_vect.fit_transform(new_data['body_text'])

print(X_counts.shape)
print(count_vect.get_feature_names())

X_count_df = pd.DataFrame(X_counts.toarray())
X_count_df.columns = count_vect.get_feature_names()
X_count_df

tfidf_vect = TfidfVectorizer(analyzer=clean_text)
X_tfidf= tfidf_vect.fit_transform(new_data['body_text'])
print(X_tfidf.shape)
print(tfidf_vect.get_feature_names())
X_tfidf_df = pd.DataFrame(X_tfidf.toarray())
X_tfidf_df.columns =tfidf_vect.get_feature_names()

X_tfidf_df

#Feature creation

new_data['body_len'] = new_data['body_text'].apply(lambda x : len(x) -x.count(" "))
new_data['punct%'] = new_data['body_text'].apply(lambda x : count_punct(x))

new_data.head()
bins = np.linspace(0,200,40)
pyplot.hist(new_data[new_data['label']=='spam']['body_len'],bins , alpha=0.5 , normed=True, label='spam')
pyplot.hist(new_data[new_data['label']=='ham']['body_len'],bins , alpha=0.5 , normed=True, label='ham')
pyplot.legend(loc='upper left')
pyplot.show()

bins = np.linspace(0,200,40)
pyplot.hist(new_data[new_data['label']=='spam']['punct%'],bins , alpha=0.5 , normed=True, label='spam')
pyplot.hist(new_data[new_data['label']=='ham']['punct%'],bins , alpha=0.5 , normed=True, label='ham')
pyplot.legend(loc='upper left')
pyplot.show()


###############################################################################
###############################################################################
##Ensemble
len(new_data)
new_data.head()
X_features = pd.concat([new_data['body_len'],new_data['punct%'],pd.DataFrame(X_tfidf.toarray())],axis=1  )
X_features.head()

print(dir(RandomForestClassifier))
print(RandomForestClassifier())

rf = RandomForestClassifier(n_jobs=-1)
k_fold = KFold(n_splits=5)
cross_val_score(rf,X_features,new_data['label'],cv=k_fold,scoring='accuracy',n_jobs=-1)

X_train , X_test , y_train , y_test = train_test_split(X_features,new_data['label'],test_size=0.2)


X_train.head()
X_test.head()
y_train.head()
new_data.head()
new_data[156:157]
len(new_data)

rf = RandomForestClassifier(n_estimators=50,max_depth=20,n_jobs=-1)
rf_model = rf.fit(X_train,y_train)
y_pred=rf_model.predict(X_test)
len(y_pred)
precision , recall , fscore , support = score(y_test,y_pred,pos_label='spam' , average='binary')

score(y_test[100:101],rf_model.predict(X_test[100:101]),pos_label='spam' , average='binary')

###############################################################################
###############################################################################

measurements = [
    {'city': 'Dubai', 'temperature': 33.},
    {'city': 'London', 'temperature': 12.},
    {'city': 'San Francisco', 'temperature': 18.},
]

from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()

vec.fit_transform(measurements).toarray()
vec.get_feature_names()

np.linspace( 0, 9, 3 )

###############################################################################
