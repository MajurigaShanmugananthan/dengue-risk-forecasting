import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

df = pd.read_csv('../../data/processed/weekly_features.csv')
# features and target (predict next-week cases)
df['target'] = df.groupby('moh_id')['cases'].shift(-1)  # next week
df = df.dropna()
features = ['cases','rainfall','temperature']
X = df[features]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBRegressor(n_estimators=100, max_depth=4)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, preds))
joblib.dump(model, '../../backend/app/ml/xgb_model.pkl')
print("Model saved.")
