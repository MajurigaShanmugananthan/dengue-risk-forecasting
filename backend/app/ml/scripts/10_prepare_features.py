import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
train = pd.read_csv(BASE_DIR / "data/processed/train_clean.csv")
test = pd.read_csv(BASE_DIR / "data/processed/test_clean.csv")

target = "Risk_Level"

drop_cols = ["District", "MOH", "week", "Dengue_Cases"]

X_train = train.drop(columns=drop_cols + [target])
y_train = train[target]

X_test = test.drop(columns=drop_cols + [target])
y_test = test[target]

X_train.to_csv(BASE_DIR / "data/processed/X_train.csv", index=False)
y_train.to_csv(BASE_DIR / "data/processed/y_train.csv", index=False)

X_test.to_csv(BASE_DIR / "data/processed/X_test.csv", index=False)
y_test.to_csv(BASE_DIR / "data/processed/y_test.csv", index=False)

print("✅ Features and target prepared")
