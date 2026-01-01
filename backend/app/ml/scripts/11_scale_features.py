import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import joblib

BASE_DIR = Path(__file__).resolve().parents[4]
X_train = pd.read_csv(BASE_DIR / "data/processed/X_train.csv")
X_test = pd.read_csv(BASE_DIR / "data/processed/X_test.csv")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pd.DataFrame(X_train_scaled, columns=X_train.columns)\
  .to_csv(BASE_DIR / "data/processed/X_train_scaled.csv", index=False)

pd.DataFrame(X_test_scaled, columns=X_test.columns)\
  .to_csv(BASE_DIR / "data/processed/X_test_scaled.csv", index=False)

joblib.dump(scaler, BASE_DIR / "data/processed/scaler.pkl")

print("✅ Feature scaling completed")
