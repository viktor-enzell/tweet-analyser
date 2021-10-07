import pickle
import matplotlib.pyplot as plt
import statistics

# Predicts average sentiment based on list of texts
class SentimentModel:
    directory = 'django_project/models/'

    # Load both the support vector classifer aswell as the tfid vectorizer
    def __init__(self):
        self.model = pickle.load(open(f'{self.directory}model.sav', 'rb'))
        self.vec = pickle.load(open(f'{self.directory}vectorizer.pk', 'rb'))

    # Takes a list of texts and returns sentiment from 0 to 1
    def fit_predict(self, data):
        if not data:
            return 0.5
        self.data = data
        features = self.vec.transform(data)
        self.res = self.model.predict(features)
        return sum(self.res) / len(self.res)

    def get_positive_outlier(self):
        max_index = self.res.index(max(self.res))
        return self.data[max_index]

    def get_negative_outlier(self):
        min_index = self.res.index(min(self.res))
        return self.data[min_index]

    def get_boxplot(self):
        return plt.boxplot(self.res, notch=None, vert=True, patch_artist=None, widths=None)

    def get_std(self):
        return statistics.stdev(self.res)
    
