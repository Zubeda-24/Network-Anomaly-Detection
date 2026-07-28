import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# -------------------------------
# Column names
# -------------------------------

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted",
    "num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "label",
    "difficulty"
]

# -------------------------------
# Load datasets
# -------------------------------

train = pd.read_csv(
    "dataset/KDDTrain+.txt",
    names=columns
)

test = pd.read_csv(
    "dataset/KDDTest+.txt",
    names=columns
)

# -------------------------------
# Convert labels
# -------------------------------

train["label"] = train["label"].apply(
    lambda x: 0 if x == "normal" else 1
)

test["label"] = test["label"].apply(
    lambda x: 0 if x == "normal" else 1
)

# -------------------------------
# Encode categorical columns
# -------------------------------

encoders = joblib.load("models/encoders.pkl")

for col in ["protocol_type", "service", "flag"]:
    train[col] = encoders[col].transform(train[col])
    test[col] = encoders[col].transform(test[col])

# -------------------------------
# Split Features and Labels
# -------------------------------

X_train = train.drop(["label"], axis=1)
y_train = train["label"]

X_test = test.drop(["label"], axis=1)
y_test = test["label"]

# -------------------------------
# Train Model
# -------------------------------

print("Training Random Forest Model...\n")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -------------------------------
# Prediction
# -------------------------------

predictions = model.predict(X_test)

# -------------------------------
# Evaluation
# -------------------------------

accuracy = accuracy_score(y_test, predictions)

print("Accuracy : {:.2f}%".format(accuracy * 100))

print("\nClassification Report\n")

print(classification_report(y_test, predictions))

print("\nConfusion Matrix\n")

print(confusion_matrix(y_test, predictions))

# -------------------------------
# Save Model
# -------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/random_forest.pkl")

print("\nModel Saved Successfully.")