import shap
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay

def run_explainable_ai(model, X, X_train, X_test):
    # 1. Feature Importance
    plt.figure(figsize=(10, 6))
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    feat_importances.nlargest(10).plot(kind='barh')
    plt.title("Top 10 Most Influential Features (Local Market)")
    plt.show()

    # 2. SHAP Values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # SHAP Summary Plot
    shap.summary_plot(shap_values, X_test, feature_names=X.columns)

    # 3. Partial Dependence Plot (PDP)
    # Focus on Memory_GB to see how storage affects price
    fig, ax = plt.subplots(figsize=(8, 4))
    PartialDependenceDisplay.from_estimator(model, X_train, ['Memory_GB'], ax=ax)
    plt.title("How Storage (Memory) Influences Price")
    plt.show()
