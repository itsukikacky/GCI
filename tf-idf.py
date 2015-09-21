#coding:utf-8
from __future__ import division
import MeCab
import collections
from math import log10 as log

rank = 30
companies = ['tabelog', 'Retty']
N = 2  # 会社の数
sentences = ['' for i in range(N)]  # 文書を入れていくリスト

# それぞれの会社のサービス概要を sentences に読み込む
for i in range(N):
    filename = companies[i] + '.txt'
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        sentences[i] += line.strip()
    f.close()

#textを形態素解析して、名詞のみのリストを返す
def extractKeyword(text):
    tagger = MeCab.Tagger('-Ochasen')
    #parseToNode()は先頭のノード（形態素情報）を返す
    node = tagger.parseToNode(text)
    keywords = []
    while node:
    	#もし形態素の最初が名詞なら
        if node.feature.split(",")[0] == "名詞":
        	#surfaceで表層形だけkeywordに足していく
            keywords.append(node.surface.decode("utf-8"))
        node = node.next
    return keywords
#それぞれ単語のみをリストに抽出
selected_keywords = [extractKeyword(sentences[i]) for i in range(N)]
print(len(selected_keywords))
wordSets = map(set, selected_keywords)
wordCounts = map(collections.Counter, selected_keywords)


# tf 値を計算
def tf(word, doc):
    n = wordCounts[doc][word]
    nlist = [wordCounts[doc][w] for w in wordSets[doc]]
    return n / sum(nlist)


# idf 値を計算
def idf(word):
    df = 0
    for i in range(N):
        if word in wordSets[i]:
            df += 1
    return log(N / df) + 1

# tf-idf 値の入れ物を用意
tfidfs = [{} for i in range(N)]

# 各単語の tf-idf 値を計算
for i in range(N):
    for word in wordSets[i]:
        tfidfs[i][word] = tf(word, i) * idf(word)

# 単語を tf-idf 値の高い順にソートする
sorted_tfidfs = [[] for i in range(N)]
sorted_words = [[] for i in range(N)]
for i in range(N):
    sorted_tfidfs[i] = sorted(
        tfidfs[i].items(), key=lambda x: x[1], reverse=True
    )
    sorted_words[i] = [x[0] for x in sorted_tfidfs[i]]
    print '%s:' % companies[i], ", ".join(sorted_words[i][:rank])


# 単語のベクトルの類似度を計算
# どれくらいの割合の単語が共通しているか
def similarity(list1, list2):
    count = 0
    for x in list1:
        if x in list2:
            count += 1
    return count / len(list1)

# 結果を表示

print '%s と %s の類似度:' % (companies[0], companies[1])
print similarity(sorted_words[0][:rank], sorted_words[(1)][:rank])
