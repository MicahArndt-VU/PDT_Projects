from typing import Set, NamedTuple, List, Tuple, Dict, Iterable
import re, glob
import math
from collections import defaultdict, Counter
import random

def tokenize(text:str):
    text.lower()
    all_words = re.findall("[a-z0-9]+", text)
    return set(all_words)

#Class for messages
class Message(NamedTuple):
    text:str
    is_spam:bool

#Class for our ML
class NaiveBayesClassifier:
    def __init__(self, k: float = 0.5):
        self.k = k #smoothing factor
        self.tokens:set[str] = set()
        self.token_spam_counts: Dict[str:int] = defaultdict(int)
        self.token_ham_counts:  Dict[str:int] = defaultdict(int)
        self.spam_messages = self.ham_messages = 0
    #Training Function
    def train(self, messages:Iterable[Message]):
        for message in messages:
            if message.is_spam:
                self.spam_messages += 1
            else:
                self.ham_messages += 1
            for token in tokenize(message.text):
                self.tokens.add(token)
                if message.is_spam:
                    self.token_spam_counts[token] += 1
                else:
                    self.token_ham_counts[token] += 1

    #Now we want a function to calculate probabilities
    def _probabilities(self, token):
        spam = self.token_spam_counts[token]
        ham = self.token_ham_counts[token]
        p_token_spam = (spam + self.k) / (self.spam_messages + 2 * self.k)
        p_token_ham = (ham + self.k) / (self.ham_messages + 2 * self.k)
        return p_token_spam, p_token_ham

    #Finally, we can write our predict function
    def predict(self, text:str):
        text_tokens = tokenize(text)
        log_prob_is_spam = log_prob_is_ham = 0.0

        #Iterate through each word in our vocab
        for token in self.tokens:
            prob_if_spam, prob_if_ham = self._probabilities(token)

            if token in text_tokens:
                log_prob_is_spam += math.log(prob_if_spam)
                log_prob_is_ham += math.log(prob_if_ham)
            #Now, add prob if the token doesn't appear in our text tokens
            else:
                log_prob_is_spam += math.log(1.0 - prob_if_spam)
                log_prob_is_ham += math.log(1.0 - prob_if_ham)
        prob_if_spam = math.exp(log_prob_is_spam)
        prob_if_ham = math.exp(prob_if_ham)
        return prob_if_spam / (prob_if_spam + prob_if_ham)


#Now we will use our model
from io import BytesIO # So we can treat bytes as a file.
import requests # To download the files, which
import tarfile # are in .tar.bz format.
BASE_URL = "https://spamassassin.apache.org/old/publiccorpus"
FILES = ["20021010_easy_ham.tar.bz2",
        "20021010_hard_ham.tar.bz2",
        "20021010_spam.tar.bz2"]
# This is where the data will end up,
# in /spam, /easy_ham, and /hard_ham subdirectories.
# Change this to where you want the data.
OUTPUT_DIR = '../naiveBayesSpam'
for filename in FILES:
    # Use requests to get the file contents at each URL.
    content = requests.get(f"{BASE_URL}/{filename}").content
    # Wrap the in-memory bytes so we can use them as a "file."
    fin = BytesIO(content)
    # And extract all the files to the specified output dir.
    with tarfile.open(fileobj=fin, mode='r:bz2') as tf:
        tf.extractall(OUTPUT_DIR)

path = '../naiveBayesSpam/*/*'
data:List[Message] = []
for filename in glob.glob(path):
    is_spam = "ham" not in filename
    with open(filename, errors='ignore') as email_file:
        for line in email_file:
            if line.startswith("Subject:"):
                subject = line.lstrip("Subject: ")
                data.append(Message(subject, is_spam))
                break  # done with this file

from machineLearningFunctions import split_data
random.seed(0)
train_messages, test_messages = split_data(data, 0.75)
model = NaiveBayesClassifier()
model.train(train_messages)

predictions = [(message, model.predict(message.text)) for message in test_messages]
confusionMatrix = Counter((message.is_spam, spam_probability > 0.5) for message, spam_probability in predictions)
print(confusionMatrix)

def p_spam_given_token(token: str, model: NaiveBayesClassifier) -> float:
    # We probably shouldn't call private methods, but it's for a good cause.
    prob_if_spam, prob_if_ham = model._probabilities(token)
    return prob_if_spam / (prob_if_spam + prob_if_ham)
words = sorted(model.tokens, key=lambda t: p_spam_given_token(t, model))
print("spammiest_words", words[-10:])
print("hammiest_words", words[:10])