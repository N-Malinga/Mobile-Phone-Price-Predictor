import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
from ExplainableAI import run_explainable_ai
import pickle

# 1. Load your preprocessed data
df = pd.read_csv('preprocessed_iphones_final.csv')

# 2. Split Features (X) and Target (y)
X = df.drop('Price', axis=1)
y = df['Price']

# 3. Train/Test Split (80/20 split as per guidelines)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and Train XGBoost Regressor
# We use 'reg:squarederror' because we are predicting a continuous price
model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# 5. Evaluation
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

# Give the model and data to your new function:
run_explainable_ai(model, X, X_train, X_test)

print(f"Mean Absolute Error: Rs. {mae:,.2f}")
print(f"Root Mean Squared Error: Rs. {rmse:,.2f}")
print(f"R-squared Score: {r2:.4f}")

# Save the model
with open('iphone_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save the list of columns so the backend knows the order
with open('model_columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

# 6. Visualization: Actual vs Predicted Prices
plt.figure(figsize=(10, 6))
plt.scatter(y_test, predictions, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Price (Rs.)')
plt.ylabel('Predicted Price (Rs.)')
plt.title('iPhone Price Prediction: Actual vs Predicted')
plt.show()