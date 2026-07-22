# model_evaluator.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier # Ya jo bhi model tum use kar rahe ho
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def calculate_project_metrics(csv_path, target_column):
    """
    Yeh function dataset load karega, model train karega, 
    aur accuracy score aur matrix return karega.
    """
    try:
        # 1. Dataset load karo
        df = pd.read_csv(csv_path)
        
        # 2. Features (Inputs) aur Target (Output) alag karo
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # 3. Train-Test Split (80% Training, 20% Testing)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
        
        # 4. Model Initialize aur Train karo
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # 5. Predict karo unseen test data par
        y_pred = model.predict(X_test)
        
        # 6. Metrics Calculate karo
        accuracy = accuracy_score(y_test, y_pred) * 100
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Sab kuch ek dictionary mein pack karke return karo
        return {
            "status": "success",
            "accuracy": round(accuracy, 2),
            "confusion_matrix": cm,
            "classification_report": report,
            "total_rows": len(df),
            "train_size": len(X_train),
            "test_size": len(X_test)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }