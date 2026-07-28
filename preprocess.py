import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# -------------------------------
# Column names for the NSL-KDD dataset
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
# Read Dataset
# -------------------------------

train = pd.read_csv(
    "dataset/KDDTrain+.txt",
    names=columns
)

test = pd.read_csv(
    "dataset/KDDTest+.txt",
    names=columns
)

print("Training Shape :", train.shape)
print("Testing Shape  :", test.shape)

# -------------------------------
# Convert attack labels into binary
# -------------------------------

train["label"] = train["label"].apply(
    lambda x: "normal" if x == "normal" else "attack"
)

test["label"] = test["label"].apply(
    lambda x: "normal" if x == "normal" else "attack"
)

# -------------------------------
# Encode categorical columns
# -------------------------------

encoders = {}

categorical_columns = [
    "protocol_type",
    "service",
    "flag"
]

for col in categorical_columns:

    encoder = LabelEncoder()

    train[col] = encoder.fit_transform(train[col])

    test[col] = encoder.transform(test[col])

    encoders[col] = encoder

# -------------------------------
# Encode output label
# -------------------------------

label_encoder = LabelEncoder()

train["label"] = label_encoder.fit_transform(train["label"])

test["label"] = label_encoder.transform(test["label"])

# -------------------------------
# Save encoders
# -------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(encoders, "models/encoders.pkl")

joblib.dump(label_encoder, "models/label_encoder.pkl")

print("\nPreprocessing Completed Successfully.")

print("\nTraining Data Preview")

print(train.head())