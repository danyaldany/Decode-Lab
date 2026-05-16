# 🌸 Professional Iris AI Vision — Streamlit App

# =========================================================
# IRIS AI VISION — PROFESSIONAL AI DASHBOARD
# Modern UI/UX Streamlit App
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="IrisAI Vision",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg,#F8FAFC,#EEF2FF,#FFFFFF);
    color: #0F172A;
    overflow-x: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.96);
    border-right: 1px solid rgba(15,23,42,0.08);
}

/* Main Title */
.main-title {
    font-size: 64px;
    font-weight: 800;
    background: linear-gradient(90deg,#7C3AED,#2563EB,#06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}

/* Subtitle */
.subtitle {
    color: #475569;
    font-size: 22px;
    margin-top: 10px;
}

/* Glass Cards */
.glass-card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(16px);
    border-radius: 24px;
    padding: 24px;
    border: 1px solid rgba(15,23,42,0.08);
    box-shadow: 0 8px 32px rgba(15,23,42,0.08);
    transition: 0.3s ease-in-out;
}

.glass-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 36px rgba(124,58,237,0.15);
}

/* Prediction Result */
.result-box {
    background: linear-gradient(135deg,#7C3AED,#2563EB);
    border-radius: 26px;
    padding: 30px;
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: 700;
    margin-top: 20px;
    box-shadow: 0 10px 35px rgba(59,130,246,0.25);
}

/* Upload Box */
.upload-box {
    background: rgba(255,255,255,0.95);
    border: 2px dashed rgba(15,23,42,0.12);
    border-radius: 24px;
    padding: 30px;
    text-align: center;
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#8B5CF6,#3B82F6);
    color: white;
    border: none;
    border-radius: 14px;
    height: 54px;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(139,92,246,0.35);
}

/* Metric Styling */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(15,23,42,0.08);
    padding: 18px;
    border-radius: 18px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    margin-right: 8px;
    padding: 10px 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATASET
# =========================================================

iris = load_iris()

X = iris.data
y = iris.target

feature_names = iris.feature_names
species_names = iris.target_names

# =========================================================
# TRAIN MODEL
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🌸 IrisAI Vision")
st.sidebar.markdown("Advanced AI Flower Analytics")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Prediction",
        "Visual Analytics",
        "About"
    ]
)

st.sidebar.markdown("---")

st.sidebar.metric("Model Accuracy", f"{accuracy*100:.2f}%")
st.sidebar.metric("Dataset Samples", "150")
st.sidebar.metric("Flower Classes", "3")

# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    '<div class="main-title">IrisAI Vision</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Next-Generation Flower Classification Powered by Artificial Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌼 Total Samples", "150")
    c2.metric("📊 Features", "4")
    c3.metric("🧠 Classes", "3")
    c4.metric("🎯 Accuracy", f"{accuracy*100:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.4,1])

    with left:

        df = pd.DataFrame(X, columns=feature_names)
        df['species'] = [species_names[i] for i in y]

        fig = px.scatter(
            df,
            x='sepal length (cm)',
            y='petal length (cm)',
            color='species',
            size='petal width (cm)',
            template='plotly_dark',
            title='AI Flower Distribution Analysis'
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        pie = px.pie(
            df,
            names='species',
            hole=0.6,
            template='plotly_dark',
            title='Species Distribution'
        )

        pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        st.plotly_chart(pie, use_container_width=True)

# =========================================================
# AI PREDICTION PAGE
# =========================================================

elif page == "AI Prediction":

    st.markdown("## 🌸 AI Flower Prediction System")

    tab1, tab2 = st.tabs([
        "📏 Manual Measurements",
        "🖼 Upload Flower Image"
    ])

    # =====================================================
    # TAB 1 — MANUAL INPUT
    # =====================================================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            sepal_length = st.slider(
                "Sepal Length",
                4.0,
                8.0,
                5.1,
                0.1
            )

            sepal_width = st.slider(
                "Sepal Width",
                2.0,
                5.0,
                3.5,
                0.1
            )

        with col2:
            petal_length = st.slider(
                "Petal Length",
                1.0,
                7.0,
                1.4,
                0.1
            )

            petal_width = st.slider(
                "Petal Width",
                0.1,
                3.0,
                0.2,
                0.1
            )

        input_data = np.array([[
            sepal_length,
            sepal_width,
            petal_length,
            petal_width
        ]])

        if st.button("🚀 Predict Flower Species"):

            pred = model.predict(input_data)
            probs = model.predict_proba(input_data)

            flower = species_names[pred][0]
            confidence = np.max(probs) * 100

            st.markdown(f'''
            <div class="result-box">
            🌸 {flower.upper()} <br><br>
            🎯 Confidence: {confidence:.2f}%
            </div>
            ''', unsafe_allow_html=True)

            prob_df = pd.DataFrame({
                'Species': species_names,
                'Confidence': probs[0]
            })

            fig_prob = px.bar(
                prob_df,
                x='Species',
                y='Confidence',
                color='Species',
                template='plotly_dark',
                title='AI Confidence Meter'
            )

            fig_prob.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )

            st.plotly_chart(fig_prob, use_container_width=True)

    # =====================================================
    # TAB 2 — IMAGE UPLOAD
    # =====================================================

    with tab2:

        st.markdown('''
        <div class="upload-box">
        <h2>📸 Upload Iris Flower Image</h2>
        <p>Upload an iris flower image for AI preview</p>
        </div>
        ''', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Flower Image",
            type=['png','jpg','jpeg']
        )

        if uploaded_file:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption='Uploaded Flower Image',
                use_container_width=True
            )

            st.info(
                "Image uploaded successfully. For actual image classification, train a CNN model using TensorFlow or PyTorch."
            )

# =========================================================
# VISUAL ANALYTICS
# =========================================================

elif page == "Visual Analytics":

    st.markdown("## 📊 AI Visual Analytics")

    df = pd.DataFrame(X, columns=feature_names)
    df['species'] = [species_names[i] for i in y]

    corr = df.drop('species', axis=1).corr()

    heatmap = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='purples',
        title='Feature Correlation Heatmap'
    )

    heatmap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    st.plotly_chart(heatmap, use_container_width=True)

    cm = confusion_matrix(y_test, predictions)

    fig_cm = px.imshow(
        cm,
        text_auto=True,
        color_continuous_scale='blues',
        title='Confusion Matrix'
    )

    fig_cm.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    st.plotly_chart(fig_cm, use_container_width=True)

# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "About":

    st.markdown("## 🧠 About This AI System")

    st.markdown('''

### What is Classification?

Classification is a supervised machine learning technique
used to predict categories or classes.

---

### Model Used

Random Forest Classifier

---

### Dataset

Iris Flower Dataset

---

### Features

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

---

### Technologies Used

- Streamlit
- Scikit-learn
- Plotly
- Pandas
- NumPy

---

### Project Highlights

✅ Modern Glassmorphism UI
✅ Interactive AI Dashboard
✅ Real-time Predictions
✅ Confidence Visualization
✅ Upload Image Feature
✅ Advanced Analytics

''')

# =========================================================
# FOOTER
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown('''
<hr style="border:1px solid rgba(255,255,255,0.08)">

<center>
Made with ❤️ using Artificial Intelligence & Streamlit
</center>
''', unsafe_allow_html=True)
