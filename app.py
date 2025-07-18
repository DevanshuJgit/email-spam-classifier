import streamlit as st
import pickle
import string
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

ps = PorterStemmer()

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y=[]
    for i in text:
        if i.isalnum():
            y.append(i)
    
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

st.title('Email Spam Classifier')

input_sms = st.text_area('Enter The Message')

if st.button('Predict'):
    #transformation
    tr_sms = transform_text(input_sms)
    #vectorization
    vect_input = tfidf.transform([tr_sms])
    #predict
    result = model.predict(vect_input)[0]
    #Display
    if result==1:
        st.header('Spam')
    else:
        st.header('Not Spam')