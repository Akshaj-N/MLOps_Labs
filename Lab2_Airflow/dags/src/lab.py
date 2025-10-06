import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pickle
import os
import matplotlib.pyplot as plt

def load_data():
    """
    Loads the Mall Customers dataset from a CSV file, serializes it, and returns the serialized data.
    """
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/Mall_Customers.csv"))
    serialized_data = pickle.dumps(df)
    return serialized_data


def data_preprocessing(data):
    """
    Deserializes data, performs preprocessing (scaling selected features), 
    and returns serialized scaled data.
    """
    df = pickle.loads(data)
    df = df.dropna()

    # Select numeric columns for clustering
    clustering_data = df[["Annual Income (k$)", "Spending Score (1-100)"]]
    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return clustering_serialized_data

def build_save_model(data, filename):
    """
    Builds a KMeans clustering model, saves it to a file, plotd elbow curve and returns SSE values.
    """
    df = pickle.loads(data)
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 50,
        "random_state": 42,
    }

    sse = []
    K_RANGE = range(1, 11)
    for k in K_RANGE:
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)

    pickle.dump(kmeans, open(filename, 'wb'))

    # Plot the Elbow Curve
    plt.figure(figsize=(8, 6))
    plt.plot(K_RANGE, sse, marker='o', linestyle='-', color='blue')
    plt.title("Elbow Curve - Mall Customers Dataset")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Sum of Squared Errors (SSE)")
    plt.grid(True)
    plt.tight_layout()

    # Save the elbow curve plot
    elbow_path = os.path.join(os.path.dirname(__file__), "../data/elbow_curve.png")
    plt.savefig(elbow_path)
    print(f"Elbow curve saved at {elbow_path}")

    return sse


def load_model_elbow(filename, sse):
    """
    Loads a saved KMeans model, determines the optimal number of clusters using the elbow method,
    and predicts the cluster for the first test observation.
    """
    loaded_model = pickle.load(open(filename, 'rb'))
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/Mall_Customers.csv"))

    # Use the same features as training
    X = df[["Annual Income (k$)", "Spending Score (1-100)"]]
    min_max_scaler = MinMaxScaler()
    X_scaled = min_max_scaler.fit_transform(X)

    kl = KneeLocator(range(1, 11), sse, curve="convex", direction="decreasing")

    cluster_pred = loaded_model.predict(X_scaled)[0]
    return f"Cluster {cluster_pred}, Optimal number of clusters: {kl.elbow}"

def visualize_clusters(filename):
    """
    Fits a KMeans model with 5 clusters to the scaled Mall Customers dataset, 
    then plots and saves the customer clusters with their centroids as a PNG image.
    """
    import matplotlib.pyplot as plt
    import os
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import MinMaxScaler

    # Load dataset
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/Mall_Customers.csv"))
    X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

    # Scale features
    min_max_scaler = MinMaxScaler()
    X_scaled = min_max_scaler.fit_transform(X)

    # 5 clusters
    kmeans = KMeans(n_clusters=5, init="random", n_init=10, max_iter=500, random_state=42)
    kmeans.fit(X_scaled)
    clusters = kmeans.predict(X_scaled)

    # Plot clusters and centroids
    plt.figure(figsize=(8, 6))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap="viridis", s=50)
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
                c='red', s=200, alpha=0.7, label="Centroids")

    plt.title("Customer Clusters (K = 5) - Mall Customers Dataset")
    plt.xlabel("Annual Income (scaled)")
    plt.ylabel("Spending Score (scaled)")
    plt.legend()
    plt.tight_layout()

    # Save the plot instead of showing
    output_path = os.path.join(os.path.dirname(__file__), "../data/cluster_plot.png")
    plt.savefig(output_path)
    print(f"Cluster plot (5 clusters) saved at {output_path}")