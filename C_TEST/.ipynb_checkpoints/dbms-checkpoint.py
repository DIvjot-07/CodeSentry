import streamlit as st
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set page config for a cleaner look
st.set_page_config(page_title="SmartCal", page_icon="🍱", layout="centered")

# --- Step 1 & 2: Data Loading & Cleaning ---

@st.cache_data
def load_and_clean_data():
    """
    Loads fast food nutrition dataset CSV and cleans it.
    Assumes CSV has 'item' and 'calories' columns.
    """
    data = pd.read_csv(
        'fastfood.csv',  # <-- Use your filename here
        usecols=['item', 'calories'],
        encoding='utf-8'
    )
    data.rename(columns={'item': 'food_name'}, inplace=True)
    data.dropna(inplace=True)
    data.drop_duplicates(subset=['food_name'], inplace=True)
    data['food_name_cleaned'] = data['food_name'].str.lower().apply(lambda x: re.sub(r'[^a-z ]', '', x).strip())
    return data

@st.cache_resource
def train_model(data):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(data['food_name_cleaned'])
    y = data['calories']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if X_train.shape[0] == 0:
        X_train, y_train = X, y
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    if X_test.shape[0] > 0:
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
    else:
        mae, rmse, r2 = 0, 0, 1
    return vectorizer, model, (mae, rmse, r2)

st.title("🍱 SmartCal: Food Calorie Estimator")
st.caption(
    "Type a fast food item name. Suggestions will appear as you type. "
    "Pick from the list or type any name (we'll predict if it's recognized)."
)
try:
    data = load_and_clean_data()
    vectorizer, model, metrics = train_model(data)
    mae, rmse, r2 = metrics
    all_foods = data['food_name'].tolist()

    # --- Unified "Google-like" search & predict bar ---
    search = st.text_input(
        "Enter or pick a food name (auto-suggest):",
        "",
        help="Type a name to see suggestions. Select or type your own and hit Enter or click Estimate."
    )

    # Find matching items for dropdown suggestions
    filtered = [f for f in all_foods if search.lower() in f.lower()] if search else []
    # Only show suggestions if any match and input is non-empty
    suggestion = st.selectbox(
        "Suggestions:",
        filtered if filtered else ["(No matches, use your input)"],
        index=0 if filtered else 0,
        key='suggestions',
        help="Pick from these, or type your own food name above."
    ) if search else None

    # Use suggestion if picked (and not the default no-match msg), else use what was typed
    if search:
        if suggestion and suggestion != "(No matches, use your input)":
            final_choice = suggestion
        else:
            final_choice = search
    else:
        final_choice = ""

    # Only predict if there is text
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
        st.write("Model evaluation metrics on test data:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean Absolute Error", f"{mae:.2f} kcal")
        col2.metric("Root Mean Squared Error", f"{rmse:.2f} kcal")
        col3.metric("R² Score", f"{r2:.2f}")

    with st.expander("Show Sample Training Data"):
        st.write(f"A sample of the {len(data)} training data items:")
        st.dataframe(data[['food_name', 'calories']], use_container_width=True)

except FileNotFoundError:
    st.error("Dataset file 'fastfood.csv' not found. Please add it to the app directory.")
except Exception as e:
    st.error(f"An error occurred: {e}")
