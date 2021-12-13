import pandas as pd
import math
import json
import matplotlib.pyplot as plt
import numpy as np


punc = '()[],-.?!:;#&\n'
topics = ["vaccine-outlook-related", "pfizer-related", "booster-related", "political-related", "vaccine-general-knowledge",
            "side-effect-related", "work-related", "vaccine-proof", "retweet", "other"]

def get_stop():
    stop = []
    with open('stopwords.txt', 'r') as sw:
        for line in sw.readlines():
            if line[0] == '#':
                continue
            else:
                stop.append(line[:-1])
    return stop

def get_df():
    df = pd.read_csv("joseph_800_1100.csv",usecols=['text','topic','emotion'])
    af = pd.read_csv('san_1100_1300.csv', usecols=['text','topic','emotion'])
    bf = pd.read_csv('marwan_0_800.csv', usecols=['text','topic','emotion'])
    df = pd.concat([df,af,bf])
    df = df[(df['topic'] != 'retweet') & (df['topic'] != 'other')]
    df['text'] = df['text'].str.lower()
    return df

def to_list(words):
    new_word = ''
    
    for char in words:
        if char not in punc:
            new_word += char
        else:
            new_word += ' '
    return new_word.split()

def get_word_count(df,stop):
    topic_dict = {"vaccine-outlook-related":{}, "pfizer-related":{}, "booster-related":{}, "political-related":{}, "vaccine-general-knowledge":{},
            "side-effect-related":{}, "work-related":{}, "vaccine-proof":{}}
    total_dict = {}
    for index, row in df.iterrows():
        topic = row['topic']
        for word in to_list(row['text']):
            if word in stop or not word.isalpha():
                continue
            if word not in total_dict:
                total_dict[word] = 1
            else:
                total_dict[word] += 1
            if word not in topic_dict[topic]:
                topic_dict[topic][word] = 1
            else:
                topic_dict[topic][word] += 1
    for word in total_dict:
        if total_dict[word] < 5:
            for topic in topic_dict:
                if word in topic_dict[topic]:
                    topic_dict[topic].pop(word)
    return topic_dict

def num_topics(topic_dict, word):
    count = 0
    for topic in topic_dict:
        if word in topic_dict[topic]:
            count += 1
    return count

def tfidf(topic_dict):
    tfidf_dict = {"vaccine-outlook-related":{}, "pfizer-related":{}, "booster-related":{}, "political-related":{}, "vaccine-general-knowledge":{},
            "side-effect-related":{}, "work-related":{}, "vaccine-proof":{}}
    for topic in topic_dict:
        for word in topic_dict[topic]:
            tf = topic_dict[topic][word]
            idf = math.log((len(topic_dict)) / num_topics(topic_dict, word))
            tfidf_dict[topic][word] = tf * idf
    return tfidf_dict

def output(n, tfidf_dict):
    output_dict = {"vaccine-outlook-related":[], "pfizer-related":[], "booster-related":[], "political-related":[], "vaccine-general-knowledge":[],
            "side-effect-related":[], "work-related":[], "vaccine-proof":[]}
    for i in range(n):
        for topic in tfidf_dict:
            if len(tfidf_dict[topic]) <= i:
                continue
            high = max(tfidf_dict[topic], key=tfidf_dict[topic].get)
            output_dict[topic].append(high)
            tfidf_dict[topic].pop(high)
    return output_dict

def calculate_tfidf(df):
    stop_words = get_stop()
    word_counts = get_word_count(df,stop_words)
    tfidf_dict = tfidf(word_counts)
    output_dict = output(10, tfidf_dict)
    with open("tfidfs.json", 'w') as fp:
        json.dump(output_dict,fp, indent=2)

def make_plots(df):
    emotion_dict = {"vaccine-outlook-related":{}, "pfizer-related":{}, "booster-related":{}, "political-related":{}, "vaccine-general-knowledge":{},
            "side-effect-related":{}, "work-related":{}, "vaccine-proof":{}}
    af = df.drop(labels=['text'],axis=1)
    x = af.value_counts()
    items = list(x.items())
    emotion = ['positive','neutral','negative']
    y = np.zeros((len(emotion_dict),3))
    x = list(emotion_dict.keys())
    x_seq = []
    for topic in x:
        new_word = ""
        for word in topic.split('-'):
            new_word += word[0].upper()
            new_word += word[1:]
            new_word += '\n'
        x_seq.append(new_word)
         
    for item in items:
        index = x.index(item[0][0])
        eIndex = emotion.index(item[0][1])
        y[index][eIndex] = item[1]
  
    y_pos = list(y[:,0])
    y_neut = list(y[:,1])
    y_neg = list(y[:,2])
    x_axis = np.arange(len(x))
  
    plt.bar(x_axis - 0.2, y_pos, 0.2, label = 'Positive',color=['blue'])
    plt.bar(x_axis, y_neut, 0.2, label = 'Neutral',color=['orange'])
    plt.bar(x_axis + 0.2, y_neg, 0.2, label = 'Negative',color=['red'])
  
    plt.xticks(x_axis, x_seq,fontsize=8)
    plt.xlabel("Groups")
    plt.ylabel("Number of Tweets")
    plt.title("Emotion of Tweets Based on Topic")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    df = get_df()
    calculate_tfidf(df)
    make_plots(df)

    

if __name__ == "__main__":
    main()
