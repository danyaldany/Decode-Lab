# =========================================================
# PROJECT 2 — DATA CLASSIFICATION USING AI
# DecodeLabs Internship Project
# =========================================================

# =========================
# IMPORT LIBRARIES
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# =========================================================
# STEP 1 — LOAD DATASET
# =========================================================

print("\nLoading Iris Dataset...\n")

iris = load_iris()

# Create DataFrame
df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

# Add target labels
df["target"] = iris.target

# =========================================================
# STEP 2 — UNDERSTAND DATASET
# =========================================================

print("First 5 Rows:\n")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:\n")
print(df.info())

print("\nStatistical Summary:\n")
print(df.describe())

print("\nFlower Classes:")
print(iris.target_names)

# =========================================================
# STEP 3 — DATA VISUALIZATION
# =========================================================

print("\nGenerating Visualization...\n")

sns.pairplot(df, hue="target")
plt.suptitle("Iris Dataset Visualization", y=1.02)

plt.show()

# =========================================================
# STEP 4 — SPLIT FEATURES AND TARGET
# =========================================================

X = df.drop("target", axis=1)
y = df["target"]

# =========================================================
# STEP 5 — TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

# =========================================================
# STEP 6 — CREATE MODEL
# =========================================================

print("\nCreating Logistic Regression Model...\n")

model = LogisticRegression(max_iter=200)

# =========================================================
# STEP 7 — TRAIN MODEL
# =========================================================

print("Training Model...\n")

model.fit(X_train, y_train)

print("Model Training Completed Successfully!")

# =========================================================
# STEP 8 — MAKE PREDICTIONS
# =========================================================

y_pred = model.predict(X_test)

print("\nPredictions:\n")
print(y_pred)

# =========================================================
# STEP 9 — MODEL EVALUATION
# =========================================================

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================================================
# STEP 10 — CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:\n")
print(cm)

plt.figure(figsize=(6,4))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.show()

# =========================================================
# STEP 11 — TEST CUSTOM INPUT
# =========================================================

sample = [[5.1, 3.5, 1.4, 0.2]]

prediction = model.predict(sample)

print("\nCustom Flower Prediction:")

print(
    "Predicted Flower:",
    iris.target_names[prediction][0]
)

# =========================================================
# END OF PROJECT
# =========================================================