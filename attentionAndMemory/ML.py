import signalTreatment as st
import splitSignal as ss
import dataSorting as ds
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Exemple de données
X = np.random.rand(100, 36, 64)  # 100 échantillons avec des dimensions (36, 64)
y = np.random.randint(0, 2, size=(100, 3))
print(y[0])  # 100 échantillons avec des labels one-hot encodés


# Aplatir les dimensions (36, 64) en une seule dimension (36*64)
X_flat = X.reshape(X.shape[0], -1)

# Convertir les étiquettes one-hot en étiquettes de classe
y_labels = np.argmax(y, axis=1) 

from sklearn.model_selection import train_test_split

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X_flat, y_labels, test_size=0.3, random_state=42)

# Initialiser le classifieur
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Entraîner le modèle
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)


# Évaluer le modèle
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Afficher un rapport de classification
print('Classification Report:')
print(classification_report(y_test, y_pred))