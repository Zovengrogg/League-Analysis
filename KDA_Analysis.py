import pandas as pd
import pickle
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt, style, pyplot
import numpy as np

data = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/KDA_Data')
data = data[["W/L", "Kills", "Deaths", "Assists", "Gold", "Time", "Vision Score"]]
data['Kills'] = pd.to_numeric(data['Kills'], errors='coerce')
data['Deaths'] = pd.to_numeric(data['Deaths'], errors='coerce')
data['Assists'] = pd.to_numeric(data['Assists'], errors='coerce')
data['Gold'] = pd.to_numeric(data['Gold'], errors='coerce')
data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
data['Vision Score'] = pd.to_numeric(data['Vision Score'], errors='coerce')

# our label
predict = "W/L"

# x is data (w/o W/L) y is what we want to predict
x = np.array(data.drop([predict,'Time','Vision Score'], 1))
y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

model = LogisticRegression()
model.fit(x_train, y_train)
# # Finds the best accuracy after n runs and saves it
# best = 0
# for _ in range(500):
#     # splits data into training and testing. This makes specifically 10% testing
#     x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
#
#     model = LogisticRegression()
#
#     # finds the best fit line for given data
#     model.fit(x_train, y_train)
#     # tests the accuracy of the model using the test data
#     acc = model.score(x_test, y_test)
#     if acc > best:
#         best = acc
#         # Saves model
#         with open("KDAmodel.pickle", "wb") as f:
#             pickle.dump(model, f)
# print(best)
# #Loads in our model
# pickle_in = open("KDAmodel.pickle", "rb")
# linear = pickle.load(pickle_in)
print(model.score(x_test, y_test))

y_predicted = model.predict(x_test)
model.predict_proba(x_test)
model.score(x_test,y_test)

print("Co: ", model.coef_)
print("Inter: ", model.intercept_)

predictions = model.predict(x_test)

# Shows prediction/data/actual
# for x in range(len(predictions)):
#     print(predictions[x], x_test[x], y_test[x])
#
# # This is the scatter plot. p is x-axis, final grade is y-axis.
# p = 'Deaths'
# style.use("ggplot")
# pyplot.scatter(data[p], data[predict])
# pyplot.xlabel(p)
# pyplot.ylabel("W/L")
# pyplot.show()
