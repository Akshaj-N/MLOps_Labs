import joblib

def predict_data(X):
    """
    Predict the wine class for the input data.
    Args:
        X (numpy.ndarray): Input data for which predictions are to be made.
    Returns:
        y_pred (numpy.ndarray): Predicted wine class (0, 1, or 2).
    """
    model = joblib.load("../model/wine_model.pkl")
    y_pred = model.predict(X)
    return y_pred