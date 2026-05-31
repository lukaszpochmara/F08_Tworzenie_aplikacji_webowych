import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris  # type: ignore[import-not-found]
from sklearn.linear_model import LinearRegression  # type: ignore[import-not-found]
from sklearn.cluster import KMeans  # type: ignore[import-not-found]
from sklearn.preprocessing import StandardScaler  # type: ignore[import-not-found]


# ---------- LOAD DATA ----------

@st.cache_data
def load_data():
    iris = load_iris()

    df = pd.DataFrame(
        iris.data,
        columns=iris.feature_names
    )

    df["species"] = iris.target
    df["species_name"] = df["species"].map({
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    })

    return df


# ---------- MAIN APP ----------

def main():
    st.title("Iris App: Linear")
    st.write(
        "This app uses the Iris dataset. "
        "It performs linear regression between two variables and clustering using KMeans."
    )

    df = load_data()

    st.subheader("Dataset preview")
    st.dataframe(df.head())

    feature_columns = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)"
    ]

    # ---------- LINEAR REGRESSION ----------

    st.header("1. Linear Regression for two variables")

    x_col = st.selectbox(
        "Choose independent variable X",
        feature_columns,
        index=0
    )

    y_col = st.selectbox(
        "Choose dependent variable Y",
        feature_columns,
        index=2
    )

    X = df[[x_col]]
    y = df[y_col]

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)

    st.write("Regression equation:")

    st.latex(
        f"y = {model.coef_[0]:.3f}x + {model.intercept_:.3f}"
    )

    st.write(f"R² score: **{model.score(X, y):.3f}**")

    fig, ax = plt.subplots()

    ax.scatter(df[x_col], df[y_col], label="Real data")
    ax.plot(df[x_col], y_pred, label="Linear regression")

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"Linear regression: {x_col} vs {y_col}")
    ax.legend()

    st.pyplot(fig)

    # ---------- CLUSTERING ----------

    st.header("2. KMeans clustering")

    number_of_features = st.number_input(
        "How many variables should be used for clustering?",
        min_value=2,
        max_value=4,
        value=2,
        step=1
    )

    selected_features = feature_columns[:number_of_features]

    st.write("Variables used for clustering:")
    st.write(selected_features)

    number_of_clusters = st.number_input(
        "Number of clusters",
        min_value=2,
        max_value=10,
        value=3,
        step=1
    )

    X_cluster = df[selected_features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)

    kmeans = KMeans(
        n_clusters=number_of_clusters,
        random_state=42,
        n_init=10
    )

    df["cluster"] = kmeans.fit_predict(X_scaled)

    st.subheader("Data with clusters")
    st.dataframe(df[feature_columns + ["species_name", "cluster"]].head(20))

    # ---------- SCATTERPLOT ----------

    st.subheader("Scatterplot of clusters")

    scatter_x = selected_features[0]
    scatter_y = selected_features[1]

    fig2, ax2 = plt.subplots()

    scatter = ax2.scatter(
        df[scatter_x],
        df[scatter_y],
        c=df["cluster"]
    )

    ax2.set_xlabel(scatter_x)
    ax2.set_ylabel(scatter_y)
    ax2.set_title("KMeans clustering scatterplot")

    st.pyplot(fig2)

    st.info(
        "The scatterplot always shows the first two variables selected for clustering. "
        "If you choose 3 or 4 variables, KMeans uses more variables internally, "
        "but the chart still displays only two dimensions."
    )


if __name__ == "__main__":
    main()