import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class bot:

    def __init__(self):
        f=open('chatbot.txt','r',errors = 'ignore')
        self.raw=f.read()
        self.raw=self.raw.lower()# converts to lowercase
        nltk.download('punkt') # first-time use only
        nltk.download('wordnet') # first-time use only
        self.sent_tokens = nltk.sent_tokenize(self.raw)# converts to list of sentences
        self.word_tokens = nltk.word_tokenize(self.raw)# converts to list of words
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
        self.GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    #WordNet is a semantically-oriented dictionary of English included in NLTK.
    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def greeting(self, sentence):

        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)
    def response(self, user_response):
        robo_response=''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            robo_response=robo_response+"I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response+self.sent_tokens[idx]
            return robo_response

    def chat(self):
        flag=True
        print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
        while(flag==True):
            user_response = input()
            user_response=user_response.lower()
            if(user_response!='bye'):
                if(user_response=='thanks' or user_response=='thank you' ):
                    flag=False
                    print("ROBO: You are welcome..")
                else:
                    if(self.greeting(user_response)!=None):
                        print("ROBO: "+self.greeting(user_response))
                    else:
                        print("ROBO: ",end="")
                        print(self.response(user_response))
                        self.sent_tokens.remove(user_response)
        else:
            flag=False
            print("ROBO: Bye! take care..")

chatty = bot()
chatty.chat()
