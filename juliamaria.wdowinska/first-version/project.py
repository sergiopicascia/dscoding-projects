import pandas as pd
from UDFs import preprocess
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

# Load the data
dfjokes = pd.read_csv('jokes.csv')
print(dfjokes.head())

print(dfjokes.isnull().any()) # Check for missing values
print(dfjokes.dtypes) # Check the data type
print(dfjokes.shape[0]) # Check the number of observations

# Preprocess 'text' and update the dataframe
dfjokes['text'] = dfjokes['text'].apply(preprocess)
print(dfjokes.head())

# Text length: humor vs. not humor
dfjokes['text_length'] = dfjokes['text'].apply(len)
plt.hist(dfjokes[dfjokes['humor'] == True]['text_length'], bins = 30, alpha = 0.5, label = 'Humorous')
plt.hist(dfjokes[dfjokes['humor'] == False]['text_length'], bins = 30, alpha = 0.5, label = 'Unhumorous')
plt.legend()
plt.xlabel('Text length')
plt.ylabel('Frequency')
plt.title('Text Length Distribution for Humor vs. Not Humor')
plt.show()

# Wordcloud: humor vs. not humor
plt.figure(figsize = (14, 4))
plt.subplot(1, 2, 1)
plt.imshow(WordCloud(background_color = 'white').generate(" ".join(dfjokes.text[dfjokes.humor == True])))
plt.title("Wordcloud for Humorous Texts")
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(WordCloud(background_color = 'white').generate(" ".join(dfjokes.text[dfjokes.humor == False])))
plt.title("Wordcloud for Unhumorous Texts")
plt.axis("off")
plt.show()

# Is the data well-balanced?
print("Number of humorous texts:", dfjokes.humor[dfjokes.humor == True].count())
print("Number of unhumorous texts:", dfjokes.humor[dfjokes.humor == False].count())

# Transform data and split it into the training and test sets
dfjokes.humor.replace(True, 1, inplace = True)
dfjokes.humor.replace(False, 0, inplace = True)

X = dfjokes.text.values
y = dfjokes.humor.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

print("Size of the training set:", len(X_train))
print("Size of the test set:", len(X_test))

# Vectorize text data
vectorizer = CountVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Logistic regression (LR) with Stochastic Gradient Descent (SGD) training
lr_classifier = SGDClassifier(loss = 'log_loss', max_iter = 1000)
lr_classifier.fit(X_train, y_train)

# Multinomial Naive Bayes (MNB)
mnb_classifier = MultinomialNB()
mnb_classifier.fit(X_train, y_train)

# Evaluate classifiers on the training and test sets
acc_train_lr = accuracy_score(y_train, lr_classifier.predict(X_train)).round(decimals = 4)
acc_train_mnb = accuracy_score(y_train, mnb_classifier.predict(X_train)).round(decimals = 4)
acc_test_lr = accuracy_score(y_test, lr_classifier.predict(X_test)).round(decimals = 4)
acc_test_mnb = accuracy_score(y_test, mnb_classifier.predict(X_test)).round(decimals = 4)

print('\nEvaluation on the training set:',
      '\nAccuracy of LR classifier:', acc_train_lr,
      '\nAccuracy of MNB classifier:', acc_train_mnb,
      '\nEvaluation on the test set:',
      '\nAccuracy of LR classifier:', acc_test_lr,
      '\nAccuracy of MNB classifier:', acc_test_mnb)

# MNB confusion matrix (test set)
ConfusionMatrixDisplay.from_estimator(mnb_classifier, X_test, y_test, display_labels = ["Unhumorous", "Humorous"])
plt.title("Confusion Matrix - MNB Classifier")
plt.show()

# User-defined text
user_text = input('Enter text:')
# Sample texts:
# (H) Why don’t Calculus majors throw house parties? Because you should never drink and derive.
# (H) A man tells his doctor, “Doc, help me. I’m addicted to Twitter!” The doctor replies, “Sorry, I don’t follow you ...”
# (H) What did the shark say when he ate the clownfish? This tastes a little funny.
# (NH) Find the latest breaking news and information on the top stories, weather, business, entertainment, politics, and more.
# (NH) Boris Johnson is still in charge. But behind closed doors, rivals are plotting his ouster.
# (NH) Seven killed in helicopter crash in Italy's Monte Cusna.

# Preprocess 'text', vectorize and predict humor using MNB classifier
user_text1 = vectorizer.transform([preprocess(user_text)])
user_prediction = mnb_classifier.predict(user_text1)

print('Your text is humorous.' if user_prediction[0] == 1 else 'Your text is unhumorous.')