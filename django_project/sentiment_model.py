import pickle 

# Predicts avrage sentiment based on list of texts
class SentimentModel:

    # Load both the support vector classifer aswell as the tfid vectorizer
    def __init__(self):
        self.model = pickle.load(open('model.sav', 'rb'))
        self.vec = pickle.load(open('vectorizer.pk', 'wb'))

    # Takes a list of texts and returns sentiment from 0 to 1
    def get_sentiment(self, data):
        features = self.vec.transform(data)
        res = self.model.predict(features)
        return sum(res) / len(res)