import streamlit as st
import pandas as pd
import numpy as np


questions = pd.read_csv("career_questions.csv")
ds = pd.read_csv("prepared_dataset.csv")

careers = ds["Career"].unique()
career_index = {c: i for i, c in enumerate(careers)}

answers = [None] * len(questions)

st.title("Career Recommender System")
st.write("Answer the questions below to get career recommendations.")

for i, row in questions.iterrows():
    options = [
        row["Answer A"],
        row["Answer B"],
        row["Answer C"],
        row["Answer D"],
    ]
    selected = st.radio(
        f"{i+1}. {row['Question']}",
        options,
        index=0,
        key=f"q_{i}"
    )
    answers[i] = options.index(selected) 


if st.button("Recommend"):
   
    career_counts = [0] * len(careers)

    for i, ans in enumerate(answers):
        if ans is None:
            continue

        qno = i + 1
        q_ds = ds[ds["QNo"] == qno]

        answer_col = ["Answer_A", "Answer_B", "Answer_C", "Answer_D"][ans]
        matched_careers = q_ds[q_ds[answer_col] == 1]["Career"].unique()

        for c in matched_careers:
            career_counts[career_index[c]] += 1

    results_df = pd.DataFrame({
        "Career": careers,
        "Score": career_counts
    }).sort_values(by="Score", ascending=False)

    # Show Top 3 careers
    st.subheader("Top Career Recommendations")
    for idx, row in results_df.head(3).iterrows():
        st.write(f"**{row['Career']}** — Score: {row['Score']}")

    if results_df["Score"].max() == 0:
        st.warning("No clear recommendation — please answer more questions.")
