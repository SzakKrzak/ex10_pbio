import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.datasets import load_breast_cancer
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import seaborn as sns

def create_heatmap(y_test,y_pred,name):
    # Macierz błędu (Confusion Matrix)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

    # Rysowanie wykresu
    class_names = [0, 1]
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)

    # Tworzenie heatmapy
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')

    plt.savefig(name)

def main():
    # Wczytanie danych
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='diagnosis')

    print(f"Liczba próbek: {len(X)}")
    print(f"Liczba cech: {X.shape[1]}")
    print(f"Rozkład klas:")
    print(f"  Benign (1): {sum(y==1)} ({sum(y==1)/len(y)*100:.1f}%)")
    print(f"  Malignant (0): {sum(y==0)} ({sum(y==0)/len(y)*100:.1f}%)")

    # Podział na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicjalizacja modelu
    logreg = LogisticRegression(random_state=16, max_iter=3000)
    logreg.fit(X_train, y_train)

    rfc = RandomForestClassifier(random_state=16,n_estimators=100)
    rfc.fit(X_train,y_train)
    # Predykcja
    y_pred_logreg = logreg.predict(X_test)
    y_pred_rfc = rfc.predict(X_test)
    #Heatmap
    create_heatmap(y_test,y_pred_logreg,"logreg.png")
    create_heatmap(y_test,y_pred_rfc,"rfc.png")

    # Wyświetlenie statystyk
    accuracy_logreg = accuracy_score(y_test, y_pred_logreg)
    precision_logreg = precision_score(y_test, y_pred_logreg)
    recall_logreg = recall_score(y_test, y_pred_logreg)
    f1_logreg = f1_score(y_test, y_pred_logreg)

    print("Wyniki modelu Logistic Regression:")
    print(f"  Accuracy (Dokładność): {accuracy_logreg:.4f}")
    print(f"  Precision (Precyzja):  {precision_logreg:.4f}")
    print(f"  Recall (Czułość):      {recall_logreg:.4f}")
    print(f"  F1-score:              {f1_logreg:.4f}")
    print("-" * 35)

    accuracy_rfc = accuracy_score(y_test, y_pred_rfc)
    precision_rfc = precision_score(y_test, y_pred_rfc)
    recall_rfc = recall_score(y_test, y_pred_rfc)
    f1_rfc = f1_score(y_test, y_pred_rfc)

    print("Wyniki modelu Random Forest Classifier:")
    print(f"  Accuracy (Dokładność): {accuracy_rfc:.4f}")
    print(f"  Precision (Precyzja):  {precision_rfc:.4f}")
    print(f"  Recall (Czułość):      {recall_rfc:.4f}")
    print(f"  F1-score:              {f1_rfc:.4f}")
    print("-" * 35)

if __name__=="__main__":
    main()