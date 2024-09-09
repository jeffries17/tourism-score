import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Streamlit app
st.title("Tourism Perception Questionnaire")

# Create a form for the questionnaire
with st.form("tourism_survey"):
    st.write("Please answer the following questions about tourism in your area:")
    
    # Sample questions
    q1 = st.slider("How satisfied are you with the current level of tourism in your area?", 1, 5, 3)
    q2 = st.selectbox("How often do you interact with tourists?", ["Daily", "Weekly", "Monthly", "Rarely", "Never"])
    q3 = st.text_area("What do you think are the main benefits of tourism in your area?")
    q4 = st.text_area("What are your main concerns about tourism in your area?")
    
    # Submit button
    submitted = st.form_submit_button("Submit")

# Process the form data
if submitted:
    # Create a DataFrame with the responses
    data = pd.DataFrame({
        "Satisfaction": [q1],
        "Interaction": [q2],
        "Benefits": [q3],
        "Concerns": [q4]
    })
    
    # Display the raw data
    st.subheader("Raw Data")
    st.write(data)
    
    # Perform some simple analysis
    st.subheader("Analysis")
    
    # Satisfaction level
    st.write(f"Satisfaction level: {q1}/5")
    
    # Interaction frequency
    st.write(f"Interaction frequency: {q2}")
    
    # Word clouds for benefits and concerns
    st.write("Most common words in benefits:")
    st.write(", ".join(w for w in q3.lower().split() if len(w) > 3))
    
    st.write("Most common words in concerns:")
    st.write(", ".join(w for w in q4.lower().split() if len(w) > 3))
    
    # Visualization
    st.subheader("Visualization")
    fig, ax = plt.subplots()
    ax.bar(["Satisfaction"], [q1])
    ax.set_ylim(0, 5)
    ax.set_ylabel("Score")
    ax.set_title("Tourism Satisfaction Score")
    st.pyplot(fig)