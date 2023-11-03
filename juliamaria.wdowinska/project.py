import pandas as pd
from UDFs import expand_contractions, extract_words, remove_stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, ConfusionMatrixDisplay

# Load the data
dfjokes = pd.read_csv('jokes.csv')
print(dfjokes.head())

print(dfjokes.isnull().any()) # Check for missing values
print(dfjokes.dtypes) # Check the data type
print(dfjokes.shape[0]) # Check the number of observations

# Expand contractions
text1 = []
for element in dfjokes.text.values:
    text1.append(expand_contractions(element))

# Extract words from text
words1 = [extract_words(element) for element in text1]

# Remove 'stopwords'
text2 = []
for element in words1:
    text2.append(remove_stopwords(element))

# Concatenate words back to text
text3 = []
for i in range(0, len(text2)):
    text3.append(" ".join(text2[i]))

# Update the dataframe
dfjokes.text = text3
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

# Data transformation and split into the training and test sets
dfjokes.humor.replace(True, 1, inplace = True)
dfjokes.humor.replace(False, 0, inplace = True)

X = dfjokes.text.values
y = dfjokes.humor.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

print("Size of the training set:", len(X_train))
print("Size of the test set:", len(X_test))

print(X_train)

# Vectorize text data
vectorizer = CountVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

# Logistic regression (LR) with Stochastic Gradient Descent (SGD) training
lr_classifier = SGDClassifier(loss = 'log_loss', max_iter = 1000)
lr_classifier.fit(X_train, y_train)

# Multinomial Naive Bayes (MNB)
mnb_classifier = MultinomialNB()
mnb_classifier.fit(X_train, y_train)

# LR evaluation (training set)
y_train_pred_lr = lr_classifier.predict(X_train)

f1_train_lr = f1_score(y_train, y_train_pred_lr).round(decimals = 4)
acc_train_lr = accuracy_score(y_train, y_train_pred_lr).round(decimals = 4)
prec_train_lr = precision_score(y_train, y_train_pred_lr).round(decimals = 4)
rec_train_lr = recall_score(y_train, y_train_pred_lr).round(decimals = 4)
print('LR - training set:', '\nF1:', f1_train_lr, '\nAccuracy:', acc_train_lr,
      '\nPrecision:', prec_train_lr, '\nRecall:', rec_train_lr)

# MNB evaluation (training set)
y_train_pred_mnb = mnb_classifier.predict(X_train)

f1_train_mnb = f1_score(y_train, y_train_pred_mnb).round(decimals = 4)
acc_train_mnb = accuracy_score(y_train, y_train_pred_mnb).round(decimals = 4)
prec_train_mnb = precision_score(y_train, y_train_pred_mnb).round(decimals = 4)
rec_train_mnb = recall_score(y_train, y_train_pred_mnb).round(decimals = 4)
print('\nMNB - training set:', '\nF1:', f1_train_mnb, '\nAccuracy:', acc_train_mnb,
      '\nPrecision:', prec_train_mnb, '\nRecall:', rec_train_mnb)

# LR evaluation (test set)
y_test_pred_lr = lr_classifier.predict(X_test)

f1_test_lr = f1_score(y_test, y_test_pred_lr).round(decimals = 4)
acc_test_lr = accuracy_score(y_test, y_test_pred_lr).round(decimals = 4)
prec_test_lr = precision_score(y_test, y_test_pred_lr).round(decimals = 4)
rec_test_lr = recall_score(y_test, y_test_pred_lr).round(decimals = 4)
print('\nLR - test set:', '\nF1:', f1_test_lr, '\nAccuracy:', acc_test_lr,
      '\nPrecision:', prec_test_lr, '\nRecall:', rec_test_lr)

# MNB evaluation (test set)
y_test_pred_mnb = mnb_classifier.predict(X_test)

f1_test_mnb = f1_score(y_test, y_test_pred_mnb).round(decimals = 4)
acc_test_mnb = accuracy_score(y_test, y_test_pred_mnb).round(decimals = 4)
prec_test_mnb = precision_score(y_test, y_test_pred_mnb).round(decimals = 4)
rec_test_mnb = recall_score(y_test, y_test_pred_mnb).round(decimals = 4)
print('\nLR - test set:', '\nF1:', f1_test_mnb, '\nAccuracy:', acc_test_mnb,
      '\nPrecision:', prec_test_mnb, '\nRecall:', rec_test_mnb)

# MNB confusion matrix (test set)
ConfusionMatrixDisplay.from_estimator(mnb_classifier, X_test, y_test, display_labels = ["Unhumorous", "Humorous"])
plt.title("Confusion Matrix - MNB Classifier")
plt.show()

# Enter your text
usertext = input('Enter text:')
# Sample texts:
# (H) Why don’t Calculus majors throw house parties? Because you should never drink and derive.
# (H) A man tells his doctor, “Doc, help me. I’m addicted to Twitter!” The doctor replies, “Sorry, I don’t follow you ...”
# (H) What did the shark say when he ate the clownfish? This tastes a little funny.
# (NH) Find the latest breaking news and information on the top stories, weather, business, entertainment, politics, and more.
# (NH) Boris Johnson is still in charge. But behind closed doors, rivals are plotting his ouster.
# (NH) Seven killed in helicopter crash in Italy's Monte Cusna.

# Text pre-processing
usertext = " ".join(remove_stopwords(extract_words(expand_contractions(usertext))))

# Humor prediction using MNB classifier
user_X = vectorizer.transform([usertext])
userprediction = mnb_classifier.predict(user_X)

if userprediction[0] == 1:
    print('Your text is: humorous.')
else:
    print('Your text is: unhumorous.')