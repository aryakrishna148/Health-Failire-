import pandas as pd
import pickle
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


# Load dataset
df = pd.read_csv("heart (1).csv")

print("Dataset shape:", df.shape)


# ======================
# GRAPH 1 : Target Distribution
# ======================
plt.figure()
df["HeartDisease"].value_counts().plot(kind="bar")
plt.title("Heart Disease Distribution")
plt.xlabel("Heart Disease (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.show()


# Encode categorical columns
categorical_cols = df.select_dtypes(include="object").columns

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])


# Features and target
X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# Models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "Decision Tree": DecisionTreeClassifier()
}

accuracies = {}
best_model = None
best_accuracy = 0


for name, model in models.items():

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)
    accuracies[name] = accuracy

    print("\n", name, "Accuracy:", accuracy)

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model


# Save best model
pickle.dump(best_model, open("heart_model.pkl", "wb"))

print("\nBest model saved!")
print("Best accuracy:", best_accuracy)


# ======================
# GRAPH 2 : Model Accuracy Comparison
# ======================
plt.figure()
plt.bar(accuracies.keys(), accuracies.values())
plt.title("Model Accuracy Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy")
plt.show()


# ======================
# GRAPH 3 : Confusion Matrix
# ======================
preds = best_model.predict(X_test)
cm = confusion_matrix(y_test, preds)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()

for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, cm[i][j], ha="center", va="center")

plt.show()


# ======================
# GRAPH 4 : Feature Importance
# ======================
if isinstance(best_model, RandomForestClassifier):

    importances = best_model.feature_importances_
    features = X.columns

    plt.figure()
    plt.barh(features, importances)
    plt.title("Feature Importance")
    plt.xlabel("Importance Score")
    plt.ylabel("Features")
    plt.show()