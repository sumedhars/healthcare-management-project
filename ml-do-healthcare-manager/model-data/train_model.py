# Use Case: Identify patients who might be at risk of worsened conditions in the next 2 weeks based on information

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
import joblib

# Load data
data = pd.read_csv('training_data.csv')

# Preprocess data
categorical_features = ['diagnosis', 'TreatmentPlan']
numeric_features = ['age', 'ImmunizationStatus', 'InsuranceStatus', 'VisitInLastMonth']

# Create transformers for numeric and categorical data
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Combine transformers into a preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create the logistic regression pipeline
pipeline = make_pipeline(preprocessor, LogisticRegression())

# Prepare target variable where True indicates 'at risk'
y = data['RiskLabel'].astype(bool)
X = data.drop('RiskLabel', axis=1)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the pipeline on the training data
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print('Model accuracy:', accuracy_score(y_test, y_pred))

# Save the model and the pipeline
joblib.dump(pipeline, 'patient_risk_model.pkl')
