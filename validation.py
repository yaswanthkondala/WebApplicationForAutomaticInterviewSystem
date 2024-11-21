import os
import re
import spacy
import nltk
import json
import torch
import string
import numpy as np
import mysql.connector
from collections import Counter
from nltk.corpus import stopwords
from gensim.downloader import load
import google.generativeai as genai
from nltk.stem import PorterStemmer
from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import RobertaTokenizer, RobertaForSequenceClassification

genai.configure(api_key="")

##load all the modelss

word2vec=load('word2vec-google-news-300')
STS = SentenceTransformer('paraphrase-MiniLM-L6-v2')
model_dir = os.path.abspath("static/models/fine_tuned_bert_model")
model_dir1 = os.path.join('static/models/fine_tuned_bert_tokenizer')
BERTmodel = BertForSequenceClassification.from_pretrained(model_dir)
BERTtokenizer = BertTokenizer.from_pretrained(model_dir1)
BERTmodel.eval()
nlp = spacy.load('en_core_web_md')
model_dir2 = os.path.join('static/models/fine_tuned_robert_model')
model_dir3 = os.path.join('static/models/fine_tuned_robert_tokenizer')
romodel = RobertaForSequenceClassification.from_pretrained(model_dir2)
rotokenizer = RobertaTokenizer.from_pretrained(model_dir3)
romodel.eval()

model_dir5 = os.path.join('static/models/sbert-fine-tuned-model')
SBertmodel = SentenceTransformer(model_dir5)

#preprocessing
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens_stemmed = [stemmer.stem(token) for token in tokens]
    return " ".join(tokens_stemmed)


def validateBERT(correctans,userAnswer):
    inputs = BERTtokenizer(
        correctans,
        userAnswer,
        return_tensors='pt',
        padding=True,
        truncation=True,
        max_length=128,
    )
    
    
    with torch.no_grad():
        outputs = BERTmodel(**inputs)
    
    
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    
    return predicted_class
def validateroBERT(correctans,userAnswer):
    inputs = rotokenizer(correctans, userAnswer, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = romodel(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

def validateSEBert(correctans,userAnswer):
    embedding1 = SBertmodel.encode(correctans, convert_to_tensor=True)
    embedding2 = SBertmodel.encode(userAnswer, convert_to_tensor=True)
    if embedding1.dim() == 1:
        embedding1 = embedding1.unsqueeze(0) 
    if embedding2.dim() == 1:
        embedding2 = embedding2.unsqueeze(0)      
    cosine_score = torch.cosine_similarity(embedding1, embedding2)
    return 1 if cosine_score.item() > 0.5 else 0
    
def validateAnswer(qid,userAnswer):
    conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="interviewbase")
    cur=conn.cursor()
    cur.execute("select answer from questionbank where questionId=%s",[qid])
    correctans=cur.fetchall()
    correctans=correctans[0][0]
    conn.close()
    userans=preprocess_text(userAnswer)
    correct=preprocess_text(correctans)
    sentence1_tokens = correct.lower().split()
    sentence2_tokens = userans.lower().split()

    # Calculate average word vectors for each sentence
    def get_sentence_vector(tokens, model):
        vector = np.zeros(300)  # Word2Vec Google model has 300 dimensions
        valid_words = 0
        for word in tokens:
            if word in model:
                vector += model[word]
                valid_words += 1
        if valid_words > 0:
            vector /= valid_words
        return vector
    
    vec1 = get_sentence_vector(sentence1_tokens, word2vec)
    vec2 = get_sentence_vector(sentence2_tokens, word2vec)
    similarity1 = cosine_similarity([vec1], [vec2])
    sentence1 = nlp(correct)
    sentence2 = nlp(userans)
    similarity2 = sentence1.similarity(sentence2)
    embedding1 = STS.encode(correct, convert_to_tensor=True)
    embedding2 = STS.encode(userans,convert_to_tensor=True)
    # Step 2: Compute the cosine similarity between the embeddings
    similarity3 = util.pytorch_cos_sim(embedding1, embedding2)
    if((similarity1<0.80 and similarity2<0.80 and similarity3<0.80)or(similarity1>0.80 and similarity2<0.80 and similarity3<0.80))or(similarity1<0.80 and similarity2>0.80 and similarity3<0.80)or(similarity1<0.80 and similarity2<0.80 and similarity3>0.80):
        return 0
    else:
        bert=validateBERT(correctans,userAnswer)
        robert=validateroBERT(correctans,userAnswer)
        SeBert=validateSEBert(correctans,userAnswer)
        predictions=[bert,robert,SeBert]
        vote_counts = Counter(predictions)
        max_voted = vote_counts.most_common(1)[0][0]
        return max_voted
n=0   
#validate with gemini pro pretrained model
def validate_gemini(id,ans):
    try:
        conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="interviewbase")
        cur=conn.cursor()
        print(id)
        cur.execute("select question from questionbank where questionId=%s",[id])
        correctans=cur.fetchone()
        conn.close()
        print(correctans)
    except Exception as e:
        print("Error",e)
    try:
        prompt = """you are a question validator. i will give you the both question and answer you have to check wheather the answer was correct or not with respect to the question. you have to tell wheather the question was  correct or  wrong or partially correct select one from the above  and another was how much percent it was correct give the value 0-100 / i want two values as output seperated with comma. if iam not provide any one of  return wrong. the question was:  """
         
        question=correctans[0]
        answer=""" \n the answer is: """+ans
        prompt=prompt+question+answer
        model = genai.GenerativeModel('gemini-pro')
        responses = model.generate_content(
            prompt,
        )
        return responses.text
    except Exception as e:
        n=1
        print(e)

def score(questions):
    n=len(questions)
    correct,wrong,partial,not_attempt=0,0,0,0
    score = 0
    for i in range(len(questions)):
        if questions[i][1]=="":
            not_attempt += 1
        else:
            try:
                response=validate_gemini(questions[i][0],questions[i][1])
                response=list(response.split(","))
                score+=int(response[1].strip())
                if response[0].lower()=='correct':
                    correct+=1
                elif response[0].lower()=='wrong':
                    wrong+=1
                else:
                    partial+=1
            except Exception as e:
                pass
    return [correct,wrong,partial,not_attempt,score/len(questions)]
