# Tweet Analyser
Group project in **Intelligent Decision Support Systems** at **UPC** in 2021.

A Tweet analysis tool built in Python with [Django](https://www.djangoproject.com/).

## Getting started
The recommended Python version for this project is Python 3.8 or higher.
It is generally recommended to start a new Virtualenv before installing the project requirements.

#### Twitter API keys
To use the program, you need to have access to the Twitter API. This is done by following the intructions on [this link](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). When you have access to the Twitter API, create a file named `.env` in the root of the project. The file should contain the following lines:
```
TWITTER_KEY=(replace with your key)
TWITTER_SECRET=(replace with your secret)
TWITTER_BEARER_TOKEN=(replace with your bearer token)
```

#### Install and run the program
Install the project requirements and run the Django server:
```
pip install -r requirements.txt
python manage.py runserver
```

You should now be able to interact with the system at http://127.0.0.1:8000/.
