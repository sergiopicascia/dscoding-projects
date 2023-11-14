import pandas as pd
from UDFs import preprocess
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
import joblib
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

# Loading the data
dfjokes = pd.read_csv('jokes.csv')
print(dfjokes.head())

print(dfjokes.isnull().any()) # Checking for missing values
print(dfjokes.dtypes) # Checking the data types
print(dfjokes.shape[0]) # Checking the number of observations

# Preprocessing 'text' and updating the dataframe
dfjokes['text'] = dfjokes['text'].apply(preprocess)
print(dfjokes.head())

# Plot: Text length: humor vs. not humor
dfjokes['text_length'] = dfjokes['text'].apply(len)
plt.hist(dfjokes[dfjokes['humor'] == True]['text_length'], bins = 30, alpha = 0.5, label = 'Humorous')
plt.hist(dfjokes[dfjokes['humor'] == False]['text_length'], bins = 30, alpha = 0.5, label = 'Unhumorous')
plt.legend()
plt.xlabel('Text length')
plt.ylabel('Frequency')
plt.title('Text Length Distribution for Humor vs. Not Humor')
plt.show()

# Plot: Wordcloud: humor vs. not humor
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

# 'True' -> 1, 'False' -> 0
dfjokes.humor.replace(True, 1, inplace = True)
dfjokes.humor.replace(False, 0, inplace = True)
print(dfjokes.head())

# Splitting the data into the training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    dfjokes.text.values, dfjokes.humor.values, test_size = 0.3, random_state = 42)

print(X_train)
print(y_train)

print("Size of the training set:", len(X_train))
print("Size of the test set:", len(X_test))

# Vectorizing 'text'
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Saving the trained vectorizer
#joblib.dump(vectorizer, 'vectorizer.joblib')

# Logistic regression (LR) with Stochastic Gradient Descent (SGD) training
lr_classifier = SGDClassifier(loss = 'log_loss', max_iter = 1000)
lr_classifier.fit(X_train, y_train)

# Multinomial Naive Bayes (MNB)
mnb_classifier = MultinomialNB()
mnb_classifier.fit(X_train, y_train)

# Evaluating classifiers on the training and test sets
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

# Evaluating the MNB classifier on the test set using confusion matrix
ConfusionMatrixDisplay.from_estimator(mnb_classifier, X_test, y_test, display_labels = ["Unhumorous", "Humorous"])
plt.title("Confusion Matrix - MNB Classifier (Test Set)")
plt.show()

# Since MNB classifier shows higher accuracy, this one will be used

# Saving the trained MNB classifier
#joblib.dump(mnb_classifier, 'mnb_classifier.joblib')