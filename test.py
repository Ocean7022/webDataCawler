from sentence_transformers import util
import requests


def getEmbedding():
    sentences = {'sentences': ['Anti-Financial Investment Fraud Zone',
                            '防制金融投資詐騙專區']}
    embeddings = requests.post('http://192.168.4.101:8000/embedding', json=sentences).json()

    cosine_scores = util.cos_sim(embeddings['embeddings'][0], embeddings['embeddings'][1])
    return "{:.4f}".format(cosine_scores[0][0])

#print(getEmbedding())


testText = '    aa  aa   '
print(testText.strip())
