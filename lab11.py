# Import
import pandas as pd
import streamlit as st

grading = {
    "Labs": 5,
    "In-class Exercises": 10,
    "Assignment": 15,
    "Midterm Exam": 20,
    "Final Exam": 50,
}

# 1: SETUP
# Task 1.1: Give the page a title (and optionally an icon) using st.set_page_config().
st.set_page_config(
    page_title="ISOM3400 Expected Score Calculator",
    page_icon="📊",
)

# Task 1.2: Display a title on the app using st.title().
#   You can also put more text/descriptions on the screen using st.write().
st.title("Expected Course Score Calculator")
st.write(
    "Enter your scores (0–100) for each component below to calculate your "
    "weighted total score and check whether you meet the passing threshold."
)

# 2. INPUT FORM
#   Create a form to group the input together.
with st.form("Score form"):
    # Task 2: Ask for user input by creating number inputs/sliders.
    #   Define min/max values to restrict user's input.
    #   Assign the values to the corresponding variables.
    labs_attended = st.number_input(
        "Labs Score / Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=100.0,
        step=1.0,
    )
    inclass_score = st.number_input(
        "In-class Exercises Score (0–100)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=1.0,
    )
    asm_score = st.number_input(
        "Assignment Score (0–100)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=1.0,
    )
    midterm_score = st.number_input(
        "Midterm Exam Score (0–100)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=1.0,
    )
    final_score = st.slider(
        "Expected Final Exam Score (0–100)",
        min_value=0,
        max_value=100,
        value=75,
    )

    click_submit = st.form_submit_button("Calculate my expected score!")

# 3. Calculate scores
if click_submit:
    # Task 3.1: Process the obtained values and calculate the total (weighted) score!
    raw_scores = {
        "Labs": labs_attended,
        "In-class Exercises": inclass_score,
        "Assignment": asm_score,
        "Midterm Exam": midterm_score,
        "Final Exam": final_score,
    }

    rows = []
    total_weighted_score = 0.0

    for component, weight in grading.items():
        score_pct = raw_scores[component]
        weighted_pts = (score_pct / 100.0) * weight
        total_weighted_score += weighted_pts
        rows.append({
            "Component": component,
            "Weight (%)": weight,
            "Your Score (%)": score_pct,
            "Weighted Points": round(weighted_pts, 2),
        })

    breakdown_df = pd.DataFrame(rows)

    st.subheader(f"Expected Total Score: {total_weighted_score:.2f} / 100")
    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

    # Task 3.2: Once the total score has been calculated, let the user know if they
    # are likely to pass the course or not by writing another message.
    passing_score = 60.0
    if total_weighted_score >= passing_score:
        st.success(
            f"You are likely to **PASS** the course (threshold: {passing_score:.0f})."
        )
    else:
        st.warning(
            f"You are at risk of **NOT PASSING** the course (threshold: {passing_score:.0f})."
        )
