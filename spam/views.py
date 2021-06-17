from django.shortcuts import render
import pickle
import nltk
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from sklearn.naive_bayes import MultinomialNB
import os

# Create your views here.
def home(request):
    return render(request,"index.html")

def prepare(mail):
    cv = pickle.load(open(r"C:\Users\amalr\projects\spamfilter\cv.sav","rb"))
    mails = [mail]
    ps = PorterStemmer()
    corpus1 = []
    for i in mails:
        sent = re.sub("[^a-zA-Z]"," ",i)
        sent = sent.lower()
        words = sent.split()
        words = [ps.stem(word) for word in words if word not in set(stopwords.words("english"))]
        sent = " ".join(words)
        corpus1.append(sent)
    x = cv.transform(corpus1).toarray()
    return x

def check(request):
    model = pickle.load(open(r"C:\Users\amalr\projects\spamfilter\final.sav","rb"))
    cat = {1:"spam",0:"ham"}
    out = model.predict(prepare(request.POST["mail"]))

    return render(request,"result.html",{"result":cat[int(out)]})
