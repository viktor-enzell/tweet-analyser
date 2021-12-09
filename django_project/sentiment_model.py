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
    def fit_predict(self, comments, tweet):
        if not comments:
            return 0.5

        feature = self.vec.transform([tweet])
        prediction = self.model.predict_proba(feature)[0][1]

        self.comments = comments
        features = self.vec.transform(comments)
        predictions = self.model.predict_proba(features)
        self.res = [prediction[1] for prediction in predictions]
        max_index = self.res.index(max(self.res))
        min_index = self.res.index(min(self.res))
        return {
            "tweet_sentiment": prediction,
            "average_comment_sentiment": sum(self.res) / len(self.res),
            "max_reply": {
                "text": self.comments[max_index],
                "sentiment": self.res[max_index]
            },
            "min_reply": {
                "text": self.comments[min_index],
                "sentiment": self.res[min_index]
            },
        }

    def get_positive_outlier(self):
        max_index = self.res.index(max(self.res))
        return self.data[max_index]

    def get_negative_outlier(self):
        min_index = self.res.index(min(self.res))
        return self.data[min_index]

    def get_boxplot(self):
        plt.boxplot(self.res, notch=None, vert=True, patch_artist=None, widths=None)
        plt.savefig('static/boxplot_tmp.png')

    def get_std(self):
        return statistics.stdev(self.res)
