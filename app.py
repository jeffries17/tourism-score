import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from googletrans import Translator

# Set up the Streamlit app
st.set_page_config(layout="wide", page_title="Tourism Perception Questionnaire")

# Initialize translator
translator = Translator()

# Translations
translations = {
    "en": {
        "title": "Tourism Perception Questionnaire",
        "nav_questionnaire": "Questionnaire",
        "nav_results": "Results",
        "q1": "How satisfied are you with the current level of tourism in your area?",
        "q2": "How often do you interact with tourists?",
        "q3": "What do you think are the main benefits of tourism in your area?",
        "q4": "What are your main concerns about tourism in your area?",
        "submit": "Submit",
        "thank_you": "Thank you for your response!",
        "no_data": "No data available yet. Please submit some responses first.",
        "select_analysis": "Select analysis to view:",
        "all_responses": "All Responses",
        "satisfaction_dist": "Satisfaction Distribution",
        "interaction_freq": "Interaction Frequency",
        "wordcloud_benefits": "Word Cloud - Benefits",
        "wordcloud_concerns": "Word Cloud - Concerns",
        "satisfaction_by_interaction": "Satisfaction by Interaction",
        "satisfaction_summary": "Satisfaction Summary",
        "avg_satisfaction": "Average satisfaction level: {:.2f}/5",
        "developed_with": "Developed with Streamlit for iRest",
        "daily": "Daily",
        "weekly": "Weekly",
        "monthly": "Monthly",
        "rarely": "Rarely",
        "never": "Never",
        "frequency": "Frequency"
    },
    "es": {
        "title": "Cuestionario de Percepción del Turismo",
        "nav_questionnaire": "Cuestionario",
        "nav_results": "Resultados",
        "q1": "¿Qué tan satisfecho está con el nivel actual de turismo en su área?",
        "q2": "¿Con qué frecuencia interactúa con turistas?",
        "q3": "¿Cuáles cree que son los principales beneficios del turismo en su área?",
        "q4": "¿Cuáles son sus principales preocupaciones sobre el turismo en su área?",
        "submit": "Enviar",
        "thank_you": "¡Gracias por su respuesta!",
        "no_data": "No hay datos disponibles aún. Por favor, envíe algunas respuestas primero.",
        "select_analysis": "Seleccione el análisis para ver:",
        "all_responses": "Todas las Respuestas",
        "satisfaction_dist": "Distribución de Satisfacción",
        "interaction_freq": "Frecuencia de Interacción",
        "wordcloud_benefits": "Nube de Palabras - Beneficios",
        "wordcloud_concerns": "Nube de Palabras - Preocupaciones",
        "satisfaction_by_interaction": "Satisfacción por Interacción",
        "satisfaction_summary": "Resumen de Satisfacción",
        "avg_satisfaction": "Nivel de satisfacción promedio: {:.2f}/5",
        "developed_with": "Desarrollado con Streamlit para iRest",
        "daily": "Diariamente",
        "weekly": "Semanalmente",
        "monthly": "Mensualmente",
        "rarely": "Raramente",
        "never": "Nunca",
        "frequency": "Frecuencia"
    }
}

# Path for the CSV file
csv_file = "responses.csv"

# Load existing responses from CSV if it exists
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Language", "Satisfaction", "Interaction", "Benefits", "Concerns", "Benefits_en", "Concerns_en"])

# Language selector
languages = ["en", "es"]
selected_lang = st.sidebar.selectbox("Select Language / Seleccione Idioma", languages)

# Translate function
def t(key):
    return translations[selected_lang].get(key, translations["en"][key])

# Sidebar for navigation
st.sidebar.title(t("title"))
page = st.sidebar.radio(t("nav_questionnaire"), [t("nav_questionnaire"), t("nav_results")])

if page == t("nav_questionnaire"):
    st.title(t("title"))
    
    # Create a form for the questionnaire in the main body
    with st.form("tourism_survey"):
        st.write(t("title"))
        
        # Sample questions
        q1 = st.slider(t("q1"), 1, 5, 3)
        q2 = st.selectbox(t("q2"), [t("daily"), t("weekly"), t("monthly"), t("rarely"), t("never")])
        q3 = st.text_area(t("q3"))
        q4 = st.text_area(t("q4"))
        
        # Submit button
        submitted = st.form_submit_button(t("submit"))

    # Process the form data
    if submitted:
        # Translate text responses to English for consistency in analysis
        benefits_en = translator.translate(q3, dest='en').text if q3 else ""
        concerns_en = translator.translate(q4, dest='en').text if q4 else ""

        # Create a DataFrame with the new response
        new_data = pd.DataFrame({
            "Language": [selected_lang],
            "Satisfaction": [q1],
            "Interaction": [q2],
            "Benefits": [q3],
            "Concerns": [q4],
            "Benefits_en": [benefits_en],
            "Concerns_en": [concerns_en]
        })
        
        # Append new data to the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Save the updated DataFrame back to the CSV
        df.to_csv(csv_file, index=False)
        
        st.success(t("thank_you"))

elif page == t("nav_results"):
    st.title(t("nav_results"))

    if df.empty:
        st.write(t("no_data"))
    else:
        # Analysis options
        analysis_options = {
            t("all_responses"): "view_responses",
            t("satisfaction_dist"): "satisfaction_dist",
            t("interaction_freq"): "interaction_freq",
            t("wordcloud_benefits"): "wordcloud_benefits",
            t("wordcloud_concerns"): "wordcloud_concerns",
            t("satisfaction_by_interaction"): "satisfaction_by_interaction",
            t("satisfaction_summary"): "satisfaction_summary"
        }

        selected_analysis = st.selectbox(t("select_analysis"), list(analysis_options.keys()))

        if analysis_options[selected_analysis] == "view_responses":
            st.subheader(t("all_responses"))
            st.write(df)

        elif analysis_options[selected_analysis] == "satisfaction_dist":
            st.subheader(t("satisfaction_dist"))
            fig, ax = plt.subplots()
            ax.hist(df['Satisfaction'], bins=5, range=(1, 5), color='skyblue', edgecolor='black')
            ax.set_title(t("satisfaction_dist"))
            ax.set_xlabel(t("q1"))
            ax.set_ylabel(t("frequency"))
            st.pyplot(fig)

        elif analysis_options[selected_analysis] == "interaction_freq":
            st.subheader(t("interaction_freq"))
            interaction_counts = df['Interaction'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(interaction_counts, labels=interaction_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            ax.set_title(t("interaction_freq"))
            st.pyplot(fig)

        elif analysis_options[selected_analysis] == "wordcloud_benefits":
            st.subheader(t("wordcloud_benefits"))
            if df['Benefits_en'].notnull().sum() > 0:
                benefits_text = " ".join(df['Benefits_en'].dropna().tolist())
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(benefits_text)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.write(t("no_data"))

        elif analysis_options[selected_analysis] == "wordcloud_concerns":
            st.subheader(t("wordcloud_concerns"))
            if df['Concerns_en'].notnull().sum() > 0:
                concerns_text = " ".join(df['Concerns_en'].dropna().tolist())
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(concerns_text)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.write(t("no_data"))

        elif analysis_options[selected_analysis] == "satisfaction_by_interaction":
            st.subheader(t("satisfaction_by_interaction"))
            interaction_means = df.groupby('Interaction')['Satisfaction'].mean()
            fig, ax = plt.subplots()
            ax.bar(interaction_means.index, interaction_means, color='lightgreen')
            ax.set_xlabel(t("q2"))
            ax.set_ylabel(t("q1"))
            ax.set_title(t("satisfaction_by_interaction"))
            st.pyplot(fig)

        elif analysis_options[selected_analysis] == "satisfaction_summary":
            st.subheader(t("satisfaction_summary"))
            avg_satisfaction = df['Satisfaction'].mean()
            st.write(t("avg_satisfaction").format(avg_satisfaction))

# Add a footer
st.sidebar.markdown("---")
st.sidebar.info(t("developed_with"))