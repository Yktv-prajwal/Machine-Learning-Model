import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Advanced BMI Calculator",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main{
    background-color:#f7f9fc;
}
.title{
    text-align:center;
    color:#0E76A8;
    font-size:45px;
    font-weight:bold;
}
.card{
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0px 0px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>⚖️ Advanced BMI Calculator</div>", unsafe_allow_html=True)
st.write("### Check your Body Mass Index and receive personalized health insights.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("User Information")

name = st.sidebar.text_input("Name")
age = st.sidebar.slider("Age", 1, 100, 22)
gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female", "Other"]
)

height = st.sidebar.number_input(
    "Height (cm)",
    50.0,
    250.0,
    170.0,
    step=1.0
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    10.0,
    300.0,
    70.0,
    step=1.0
)

calculate = st.sidebar.button("Calculate BMI")

# ---------------- MAIN ----------------
if calculate:

    bmi = weight / ((height / 100) ** 2)

    # Ideal Weight
    min_weight = 18.5 * ((height / 100) ** 2)
    max_weight = 24.9 * ((height / 100) ** 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "yellow"
        advice = """
• Increase healthy calorie intake.
• Eat protein-rich foods.
• Strength training is recommended.
"""
    elif bmi < 25:
        category = "Normal"
        color = "green"
        advice = """
• Maintain a balanced diet.
• Exercise 30 minutes daily.
• Stay hydrated.
"""
    elif bmi < 30:
        category = "Overweight"
        color = "orange"
        advice = """
• Reduce sugary foods.
• Walk 8,000–10,000 steps daily.
• Include more vegetables.
"""
    else:
        category = "Obese"
        color = "red"
        advice = """
• Consult a healthcare professional.
• Follow a calorie-controlled diet.
• Exercise regularly.
"""

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("BMI", f"{bmi:.2f}")

    with col2:
        st.metric("Category", category)

    with col3:
        st.metric("Ideal Weight", f"{min_weight:.1f}-{max_weight:.1f} kg")

    st.divider()

    st.subheader(f"Hello {name} 👋")

    st.write(f"**Age:** {age}")
    st.write(f"**Gender:** {gender}")

    st.progress(min(bmi / 40, 1.0))

    if color == "green":
        st.success(f"Your BMI is {bmi:.2f} ({category})")
    elif color == "yellow":
        st.warning(f"Your BMI is {bmi:.2f} ({category})")
    elif color == "orange":
        st.warning(f"Your BMI is {bmi:.2f} ({category})")
    else:
        st.error(f"Your BMI is {bmi:.2f} ({category})")

    st.subheader("Health Advice")
    st.info(advice)

    st.subheader("BMI Reference")

    bmi_table = pd.DataFrame({
        "BMI Range": [
            "<18.5",
            "18.5 - 24.9",
            "25 - 29.9",
            "30+"
        ],
        "Category": [
            "Underweight",
            "Normal",
            "Overweight",
            "Obese"
        ]
    })

    st.table(bmi_table)

    report = pd.DataFrame({
        "Field": [
            "Name",
            "Age",
            "Gender",
            "Height (cm)",
            "Weight (kg)",
            "BMI",
            "Category",
            "Ideal Weight"
        ],
        "Value": [
            name,
            age,
            gender,
            height,
            weight,
            round(bmi, 2),
            category,
            f"{min_weight:.1f}-{max_weight:.1f} kg"
        ]
    })

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download BMI Report",
        data=csv,
        file_name="BMI_Report.csv",
        mime="text/csv"
    )

else:
    st.info("Enter your information from the sidebar and click **Calculate BMI**.")

st.divider()

st.caption("Developed using Python • Streamlit")