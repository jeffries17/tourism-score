import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Set up the Streamlit app
st.title("Tourism Perception Questionnaire")

# Path for the CSV file
csv_file = "responses.csv"

# Load existing responses from CSV if it exists
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Satisfaction", "Interaction", "Benefits", "Concerns"])

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
    # Create a DataFrame with the new response
    new_data = pd.DataFrame({
        "Satisfaction": [q1],
        "Interaction": [q2],
        "Benefits": [q3],
        "Concerns": [q4]
    })
    
    # Append new data to the existing DataFrame
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save the updated DataFrame back to the CSV
    df.to_csv(csv_file, index=False)
    
    # Display the updated data
    st.subheader("All Responses")
    st.write(df)

# Data Analysis Section
if not df.empty:
    st.subheader("Data Analysis & Visualizations")
    
    # 1. Satisfaction Distribution - Histogram
    st.subheader("Satisfaction Distribution")
    fig, ax = plt.subplots()
    ax.hist(df['Satisfaction'], bins=5, range=(1, 5), color='skyblue', edgecolor='black')
    ax.set_title('Distribution of Satisfaction Scores')
    ax.set_xlabel('Satisfaction Score')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    
    # 2. Interaction Frequency - Pie Chart
    st.subheader("Interaction Frequency Breakdown")
    interaction_counts = df['Interaction'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(interaction_counts, labels=interaction_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title('Frequency of Interaction with Tourists')
    st.pyplot(fig)
    
    # 3. Word Cloud for Benefits
    st.subheader("Word Cloud for Benefits")
    if df['Benefits'].notnull().sum() > 0:
        benefits_text = " ".join(df['Benefits'].dropna().tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(benefits_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("No benefits data available for word cloud.")
    
    # 4. Word Cloud for Concerns
    st.subheader("Word Cloud for Concerns")
    if df['Concerns'].notnull().sum() > 0:
        concerns_text = " ".join(df['Concerns'].dropna().tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(concerns_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("No concerns data available for word cloud.")
    
    # 5. Correlation Between Satisfaction and Interaction - Bar Chart
    st.subheader("Satisfaction by Interaction Frequency")
    interaction_means = df.groupby('Interaction')['Satisfaction'].mean()
    fig, ax = plt.subplots()
    ax.bar(interaction_means.index, interaction_means, color='lightgreen')
    ax.set_xlabel("Interaction Frequency")
    ax.set_ylabel("Average Satisfaction Score")
    ax.set_title("Average Satisfaction Score by Interaction Frequency")
    st.pyplot(fig)
    
    # 6. Average Satisfaction
    st.subheader("Satisfaction Summary")
    avg_satisfaction = df['Satisfaction'].mean()
    st.write(f"Average satisfaction level: {avg_satisfaction:.2f}/5")
