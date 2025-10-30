import streamlit as st
import numpy as np
import pandas as pd


questions = pd.read_csv("career_questions.csv")
ds = pd.read_csv("prepared_dataset.csv")

careers = ds["Career"].unique()
career_counts = [0]*len(careers)



def count_careers(index):
    q_ds = ds[ds["QNo"] == index]
    answer = user_answers[index]
    answer_name = ""
    if answer == 0:
        answer_name = "Answer_A"
    elif answer == 1:
        answer_name = "Answer_B"
    elif answer == 2:
        answer_name = "Answer_C"
    else:
        answer_name = "Answer_D"            
    answer_ds = q_ds[q_ds[answer_name] == 1][["Career"]].reset_index(drop = True)
    for row in answer_ds.index:
        for j in range(0, len(careers)):
            if answer_ds.iloc[row]["Career"] == careers[j]:
                career_counts[j] = career_counts[j] + 1


st.title("Career Recommender")
# st.markdown("""
#     <style>
#    .stApp {
#         background-color: #121212;
#         color: #f1f1f1;
#         font-family: 'Segoe UI', sans-serif;
#     }
#     </style>
# """, unsafe_allow_html=True)

answers= [0]*20


for i in questions.index:
    Answer_A = questions.iloc[i]["Answer A"]
    Answer_B = questions.iloc[i]["Answer B"]
    Answer_C = questions.iloc[i]["Answer C"]
    Answer_D = questions.iloc[i]["Answer D"]

    options = ["Not Selected" , Answer_A ,Answer_B ,Answer_C,Answer_D]

    selected = st.radio(str((i+1))+ "." + questions.iloc[i]["Question"],
            options,index = 0              
            )
    
    answers[i]=options.index(selected)


if st.button("Recommend"):
    user_answers=[]
    st.write("Recommended Career is : ")
    for answer in answers:
        user_answers.append(answer)
    for i in range (0,len(user_answers)):
        count_careers(i)
    st.write("Recommended Career is  ",careers[np.argmax(career_counts)])
  
    

    



