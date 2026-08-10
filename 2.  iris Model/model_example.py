import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import plotly.express as px
import os

st.set_page_config(
    page_title="Iris Flower Classification",
    page_icon="🌸",
    layout="wide"
)

st.title("Iris Flower Species Classifier")

st.write(
    "This app predicts the species of an Iris flower based on its features using a Random Forest Classifier."
)

st.sidebar.header("Model Settings")
train_new_model = st.sidebar.checkbox("Train a new model", value=True)


@st.cache_resource
def load_data():
    iris = load_iris()

    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target
    target_names = iris.target_names

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return (
        model,
        accuracy,
        X,
        y,
        target_names,
        X_train.columns.tolist()
    )


if train_new_model or not os.path.exists("iris_model.pkl"):

    model, accuracy, X, y, target_names, feature_names = load_data()

    with open("iris_model.pkl", "wb") as f:
        pickle.dump(
            (model, target_names, feature_names),
            f
        )

    st.sidebar.success(
        f"Model trained and saved.\nAccuracy: {accuracy:.2%}"
    )

else:

    with open("iris_model.pkl", "rb") as f:
        model, target_names, feature_names = pickle.load(f)

    st.sidebar.success("Loaded pre-trained model.")

    # Load dataset when using saved model
    iris = load_iris()

    X = pd.DataFrame(
        iris.data,
        columns=iris.feature_names
    )

    y = iris.target

    # Calculate accuracy again
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        y_pred
    )


# Main input

st.subheader("Input Flower Measurements")

col1, col2 = st.columns(2)

with col1:

    sepal_length = st.slider(
        "Sepal Length (cm)",
        min_value=0.0,
        max_value=10.0,
        value=5.0
    )

    sepal_width = st.slider(
        "Sepal Width (cm)",
        min_value=0.0,
        max_value=10.0,
        value=3.5
    )


with col2:

    petal_length = st.slider(
        "Petal Length (cm)",
        min_value=0.0,
        max_value=10.0,
        value=1.5
    )

    petal_width = st.slider(
        "Petal Width (cm)",
        min_value=0.0,
        max_value=10.0,
        value=0.2
    )


# Create input dataframe for prediction

input_data = pd.DataFrame({
    feature_names[0]: [sepal_length],
    feature_names[1]: [sepal_width],
    feature_names[2]: [petal_length],
    feature_names[3]: [petal_width]
})


# Prediction

if st.button(
    "Predict Species",
    type="primary",
    use_container_width=True
):

    prediction = model.predict(input_data)[0]

    prediction_proba = model.predict_proba(input_data)[0]

    predicted_species = target_names[prediction]

    st.success(
        f"The predicted species is: {predicted_species}"
    )

    # Show Probability

    st.write("Prediction Probabilities")

    prob_df = pd.DataFrame({
        "Species": target_names,
        "Probability": prediction_proba
    })

    st.bar_chart(
        prob_df.set_index("Species")
    )


# Model Performance Section

st.subheader("Model Performance")

st.metric(
    "Test Accuracy",
    f"{accuracy:.2%}"
)


# Create Iris Dataset DataFrame
# This is outside the checkbox so iris_df always exists

iris_df = pd.DataFrame(
    X,
    columns=load_iris().feature_names
)

iris_df["species"] = pd.Series(y).map({
    0: "setosa",
    1: "versicolor",
    2: "virginica"
})


# Show Dataset

if st.checkbox("show Dataset"):

    st.write("IRIS DATASET PREVIWE")

    st.dataframe(
        iris_df.head(),
        use_container_width=True
    )


# Iris Dataset Scatter Plot

st.subheader("Petal Length vs Petal Width")


fig = px.scatter(
    iris_df,
    x="petal length (cm)",
    y="petal width (cm)",
    color="species",
    size="sepal length (cm)",
    hover_data=["sepal width (cm)"],
    title="Iris Species Distribution"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

