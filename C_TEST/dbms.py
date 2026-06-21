import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set page config for a cleaner look
st.set_page_config(page_title="SmartCal", page_icon="🍱", layout="centered")

@st.cache_data
def load_and_clean_data():
    data = pd.read_csv(
        'fastfood.csv',  # <-- Use your filename here
        usecols=['item', 'calories'],
        encoding='utf-8'
    )
    data.rename(columns={'item': 'food_name'}, inplace=True)
    data.dropna(inplace=True)
    data.drop_duplicates(subset=['food_name'], inplace=True)
    data['food_name_cleaned'] = data['food_name'].str.lower().apply(
        lambda x: re.sub(r'[^a-z ]', '', x).strip())
    return data

@st.cache_resource
def train_models(data):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(data['food_name_cleaned'])
    y = data['calories']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    # Random Forest
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_r2 = r2_score(y_test, rf_pred)
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    lr_r2 = r2_score(y_test, lr_pred)
    return (vectorizer, rf, (rf_mae, rf_rmse, rf_r2)), (lr, (lr_pred, y_test, lr_mae, lr_rmse, lr_r2))

st.title("🍱 SmartCal: Food Calorie Estimator")
st.caption(
    "Type a fast food item name. Suggestions will appear as you type. "
    "Pick from the list or type any name (we'll predict if it's recognized)."
)
try:
    data = load_and_clean_data()
    (vectorizer, model, rf_metrics), (lr, (lr_pred, y_test, lr_mae, lr_rmse, lr_r2)) = train_models(data)
    all_foods = data['food_name'].tolist()
    rf_mae, rf_rmse, rf_r2 = rf_metrics

    # --- Unified "Google-like" search & predict bar ---
    search = st.text_input(
        "Enter or pick a food name (auto-suggest):",
        "",
        help="Type a name to see suggestions. Select or type your own and hit Enter or click Estimate."
    )
    filtered = [f for f in all_foods if search.lower() in f.lower()] if search else []
    suggestion = st.selectbox(
        "Suggestions:",
        filtered if filtered else ["(No matches, use your input)"],
        index=0 if filtered else 0,
        key='suggestions',
        help="Pick from these, or type your own food name above."
    ) if search else None
    if search:
        if suggestion and suggestion != "(No matches, use your input)":
            final_choice = suggestion
        else:
            final_choice = search
    else:
        final_choice = ""

    if final_choice:
        action = st.button("Estimate Calories")
        if action:
            cleaned = final_choice.lower().strip()
            cleaned = re.sub(r'[^a-z ]', '', cleaned)
            food_vec = vectorizer.transform([cleaned])
            if food_vec.sum() == 0:
                st.error("Sorry, I don't recognize that food. Try retyping or select a suggestion.")
            else:
                calories = model.predict(food_vec)[0]
                st.success(f"Estimated Calories: {calories:.2f} kcal")
                st.caption(f"Based on: {final_choice}")

    st.divider()
    with st.expander("Show Model Performance (on test data)"):
        st.write("Random Forest performance on test data:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean Absolute Error", f"{rf_mae:.2f} kcal")
        col2.metric("Root Mean Squared Error", f"{rf_rmse:.2f} kcal")
        col3.metric("R² Score", f"{rf_r2:.2f}")
        st.write("Linear Regression performance on test data:")
        st.markdown(f"""
            - MAE: **{lr_mae:.2f} kcal**
            - RMSE: **{lr_rmse:.2f} kcal**
            - R² Score: **{lr_r2:.2f}**
        """)
        # Show scatterplot of predictions vs. actual for Linear Regression
        fig, ax = plt.subplots()
        ax.scatter(y_test, lr_pred, color='dodgerblue', alpha=0.7, label="Predictions")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, label="Ideal Line")
        ax.set_xlabel("Actual Calories")
        ax.set_ylabel("Predicted Calories")
        ax.set_title("Linear Regression: Predicted vs Actual Calories")
        ax.legend()
        st.pyplot(fig)

    with st.expander("Show Sample Training Data"):
        st.write(f"A sample of the {len(data)} training data items:")
        st.dataframe(data[['food_name', 'calories']], use_container_width=True)

except FileNotFoundError:
    st.error("Dataset file 'fastfood.csv' not found. Please add it to the app directory.")
except Exception as e:
    st.error(f"An error occurred: {e}")
