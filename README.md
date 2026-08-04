# ❤️ HeartSense — Heart Disease Predictor

<p align="center">
  <img src="Images/Heart.jpg" alt="HeartSense banner" width="100%">
</p>

HeartSense is a Streamlit web app that predicts the likelihood of heart disease from a patient's clinical
data using a Random Forest classifier. Alongside the predictor, it includes a guidance page with general
lifestyle and warning-sign information for heart patients.

## Features

- **Prediction** — Enter patient details (age, chest pain type, blood pressure, cholesterol, ECG results,
  max heart rate, ST depression, etc.) and get an instant prediction with a confidence score.
- **Guidance** — Educational content on diet, physical activity, medication adherence, lifestyle changes,
  and emergency warning signs.
- **Clean UI** — Custom-styled multi-page Streamlit interface with a themed sidebar and background imagery.

<p align="center">
  <img src="Images/prediction.jpg" alt="Prediction page preview" width="70%">
</p>

## Tech Stack

- Python
- [Streamlit](https://streamlit.io/) — web app framework
- [scikit-learn](https://scikit-learn.org/) — Random Forest model
- pandas, joblib

## Project Structure

```
app.py                              # Streamlit app (Home, Prediction, Guidance pages)
randomforest_model.pkl              # Trained Random Forest model
heart_disease_feature_columns.pkl   # Feature column order expected by the model
randomforest.ipynb                  # Model training / exploration notebook
train.csv / test.csv                # Training and test datasets
sample_submission.csv               # Sample submission format
submission_Randomforest.csv         # Model output submission
Images/                             # App imagery (background, screenshots)
.streamlit/config.toml              # Streamlit theme config
```

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/AnthonyFrancisSharu/HeartSense.git
   cd HeartSense
   ```
2. Install dependencies:
   ```bash
   pip install streamlit scikit-learn pandas joblib
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Model Input Features

Age, Sex, Chest pain type, Resting BP, Cholesterol, Fasting blood sugar > 120 mg/dl, Resting EKG results,
Max heart rate achieved, Exercise-induced angina, ST depression (old peak), Slope of peak exercise ST
segment, Number of major vessels, Thallium stress test result.

## Disclaimer

This app is for educational purposes only and does not constitute medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional.
