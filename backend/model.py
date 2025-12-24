import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv("Housing.csv")

X = data[['area', 'bedrooms', 'bathrooms', 'parking']]
y = data['price']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("house_model.pkl", "wb"))

print("Model trained and saved!")
