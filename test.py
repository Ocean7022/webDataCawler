from sentence_transformers import util
import requests, asyncio


def getEmbedding():
    sentences = {'sentences': ['Anti-Financial Investment Fraud Zone',
                            '防制金融投資詐騙專區']}
    embeddings = requests.post('http://192.168.4.101:8000/embedding', json=sentences).json()

    cosine_scores = util.cos_sim(embeddings['embeddings'][0], embeddings['embeddings'][1])
    return "{:.4f}".format(cosine_scores[0][0])

#print(getEmbedding())

#192.168.4.101:8000/embedding

#testText = '    aa  aa   '
#print(testText.strip())

def get_embeddings(sentences):
    response = requests.post('http://192.168.4.101:8000/embedding', json=sentences)
    return response.json()

def test():
    sentences1 = {
            'sentences': [
                "西瓜",
                "蘋果",
                "香蕉",
                "槍",
                "橙",
                "草莓",
                "葡萄",
                "梨",
                "櫻桃",
                "柚",
                "桃"
            ]
        }
        
    sentences2 = {
            'sentences': [
                "strawberry",
                "pomelo",
                "pear",
                "orange",
                "watermelon",
                "peach"
                "grape",
                "apple",
                "cherry",
                "gun",
                "banana",
            ]
        }

    embeddings1 = get_embeddings(sentences1)
    embeddings2 = get_embeddings(sentences2)

    cosine_scores = util.cos_sim(embeddings1['embeddings'], embeddings2['embeddings'])

    

    for cosIndex, cosine_score in enumerate(cosine_scores):
        max_score = 0
        max_score_index = 0
        for index, cosine in enumerate(cosine_score):
            if cosine > max_score:
                max_score = cosine
                max_score_index = index
            
        sentences1['sentences'][cosIndex] += sentences2['sentences'][max_score_index]

        max_score = 0
        max_score_index = 0

    print(cosine_scores)
    print(sentences1['sentences'])

    #return "{:.4f}".format(cosine_scores[0][0])


test()


