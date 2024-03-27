from flask import Flask, request, jsonify
from typing import Literal
from pydantic import BaseModel, conint, confloat
from pickle import load
import streamlit as st
import numpy as np
import pandas as pd



# Let's first define the Pydantic model for the user input data validation
class InputData(BaseModel):
    age : conint(ge=20, le=80)
    sex : Literal["Male", "Female"]
    cp : Literal['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymtomatic']
    trestbps : conint(ge=90, le=200)
    chol : conint(ge=100, le=600)
    fbs : Literal["True", "False"]
    restecg : Literal['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy']
    thalach : conint(ge=50, le=200)
    exang : Literal["Yes", "No"]
    oldpeak :  confloat(ge=0.0, le=6.20)
    slope : Literal['Upsloping', 'Flat', 'Downsloping']
    ca : conint(ge=0, le=4)
    thal : Literal['Normal', 'Fixed Defect', 'Reversible Defect']



# Loading the model and scaler from disk
with open('model.bin', 'rb') as f1:
    model = load(file=f1)

with open('scaler.bin', 'rb') as f2:
    scaler = load(file=f2)


# The Flask app
app = Flask(__name__)

# Let's now define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Validating the user input data using our Pydantic predefined model
    input_data = InputData(**request.json)

    # Let's now convert the input data to a python dictionary
    input_dict : dict = input_data.model_dump()

    # Let's make the prediction
    prediction = model.predict([list(input_dict.values())])[0]


    # Let's return the predition as JSON response
    return jsonify({'Prediction' : prediction})




# The main function (The Streamlit app)
def main():
    # Setting the titile and favicon
    #st.set_page_config(page_title='Heart Attack Prediction App', page_icon=':heart:')

    # Loading ECE logo image
    st.image('static/ece-ecole-ingenieurs.png')

    # Adding some space 
    st.write('\n\n\n\n')

    # Setting the titile and description
    #st.subheader('Projet hackathon : Application de prédiction des crises cardiaques', divider='rainbow')
    st.subheader('Projet hackathon : Prédiction des crises cardiaques', divider='rainbow')


    #st.title('Hackathon Project: Heart Attack prediction App')


    #st.write('Cette application prédit la probabilité d’une crise cardiaque en fonction des données d’analyse des patients')
    st.markdown('###### Cette application prédit la probabilité d’une crise cardiaque en fonction des données d’analyse des patients')


    # Adding the user input fields
    st.sidebar.header('***User Input***')
    age = st.sidebar.slider('_`Age`_', min_value=20, max_value=80, value=40)
    sex = st.sidebar.selectbox('_`Sex`_', ['Male', 'Female'])
    cp = st.sidebar.selectbox('_`Chest Pain Type`_', ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymtomatic'])
    trestbps = st.sidebar.slider('_`Resting Blood Pressure (mm Hg)`_', min_value=90, max_value=200, value=120)
    chol = st.sidebar.slider('_`Serum Cholesterol (mg/dl)`_', min_value=100, max_value=600, value=200)
    fbs = st.sidebar.selectbox('_`Fasting Blood Sugar > 120 mg/dl`_', ['True', 'False'])
    restecg = st.sidebar.selectbox('_`Resting Electrocardiographic Results`_', ['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'])
    thalach = st.sidebar.slider('_`Maximum Heart Rate Achieved (bpm)`_', min_value=50, max_value=200, value=150)
    exang = st.sidebar.selectbox('_`Exercise Induced Angina`_', ['Yes', 'No'])
    oldpeak = st.sidebar.slider('_`ST Depression Induced by Exercise`_', min_value=0.0, max_value=6.2, value=0.0)
    slope = st.sidebar.selectbox('_`Slope of Peak Exercise ST Segment`_', ['Upsloping', 'Flat', 'Downsloping'])
    ca = st.sidebar.slider('_`Number of Major Vessels Colored by Fluoroscopy`_', min_value=0, max_value=3, value=0)
    thal = st.sidebar.selectbox('_`Thalassemia`_', ['Normal', 'Fixed Defect', 'Reversible Defect'])









    # Adding some space 
    st.write('\n\n\n')

    # Adding "predict" button
    st.markdown(
    """
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    if st.button(':rainbow[_Predire_]'):

        # Let's validate the user input data by using our predefined Pydantic model
        input_data = InputData(
            age=age,
            sex=sex,
            cp=cp,
            trestbps=trestbps,
            chol=chol,
            fbs=fbs,
            restecg=restecg,
            thalach=thalach,
            exang=exang,
            oldpeak=oldpeak,
            slope=slope,
            ca=ca,
            thal=thal
        )


        # Let's now convert the input data to a python dictionary
        input_dict : dict = input_data.model_dump()

        # Let's make the prediction
        #prediction = model.predict([list(input_dict.values())])[0]





        # Processing the user input
        sex = 0 if sex == 'Male' else 1
        fbs = 1 if fbs == 'True' else 0
        exang = 1 if exang == 'Yes' else 0

        def cp_encode(cp:str) -> int:
            if cp == 'Typical Angina':
                return 0
            elif cp == 'Atypical Angina':
                return 1
            elif cp == 'Non-anginal Pain':
                return 2
            else:
                return 3
       
        cp = cp_encode(cp=cp)
      
        #'Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'
        def cp_restecg(restecg:str) -> int:
            if restecg == 'Normal':
                return 0
            elif restecg == 'ST-T Wave Abnormality':
                return 1
            else:
                return 2
       
        restecg = cp_restecg(restecg=restecg)


        def cp_slope(slope:str) -> int:
            if slope == 'Upsloping':
                return 0
            elif slope == 'Flat':
                return 1
            else:
                return 2
       
        slope = cp_slope(slope=slope)

        def cp_thal(thal:str) -> int:
            if thal == 'Normal':
                return 0
            elif thal == 'Fixed Defect':
                return 1
            else:
                return 2
       
        thal = cp_thal(thal=thal)
    

        # Scaling the incoming request data
        data = {
            'age': age, 
            'sex':sex, 
            'cp':cp, 
            'trestbps':trestbps, 
            'chol':chol, 
            'fbs':fbs, 
            'restecg':restecg, 
            'thalach':thalach, 
            'exang':exang, 
            'oldpeak':oldpeak, 
            'slope':slope,
            'ca' : ca, 
            'thal':thal
        }
        df = pd.DataFrame(data, index=[0])

        # Check if feature names match those used during fit
        if set(df.columns) != set(scaler.get_feature_names_out()):
            # If not, rename the columns to match
            df.columns = scaler.get_feature_names_out()

        input_data_scaled = scaler.transform(df)


        # Making prediction
        #input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        try:
            #prediction = model.predict(input_data)[0]
            prediction = model.predict(input_data_scaled)[0]
        except Exception as e:
            # Handle any exceptions related to model prediction
            st.error(f"Error during prediction: {str(e)}")
            prediction = None

        #prediction = model.predict([list(input_dict.values())])[0]


        # Displaying prediction
        #prediction = 1
        #import emoji
        thumbs_up = "👍"
        sad_face = "😢"
            
        st.subheader('_Prédiction_')
        if prediction == 1:
            st.write(f"D’après vos données d’analyse, la probabilité d’une crise cardiaque est très élevée {sad_face}.")
        else:
            st.write(f"D’après vos données d’analyse, la probabilité d’une crise cardiaque est très faible {thumbs_up}.")

        # Displaying the model accuracy
            #accuracy : float = 0.9878
            #st.write(f'Model Accuracy: {accuracy:.2f}')


if __name__ == '__main__':
    #import threading
    # Starting the Flask app in a seperate thread(in case we want to access the model through API endpoint)
    #flask_thread = threading.Thread(target=app.run, kwargs={'debug' : False})
    #flask_thread.start()

    # Running the Stramlit app
    main()