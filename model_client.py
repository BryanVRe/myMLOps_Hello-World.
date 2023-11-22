import streamlit as st
import requests
import json

SERVER_URL = 'https://linear-model-service-bryanvre.cloud.okteto.net/v1/models/linear-model:predict'

def make_prediction(hours_worked):
    # Hacer una solicitud al servidor externo para predecir la métrica
    payload = {'instances': [hours_worked]}
    
    try:
        response = requests.post(SERVER_URL, json=payload)
        response.raise_for_status()
        prediction = response.json()
        return prediction['predictions'][0][0]
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error de conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Tiempo de espera agotado: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error en la solicitud: {err}")

def calculate_deficiency(hours_worked):
    # Usar la fórmula Y=3X+2 para calcular una métrica relacionada con la deficiencia del programador
    target_hours = 40  # Establecer las horas de trabajo establecidas
    deficiency_metric = max(0, hours_worked - target_hours)
    return deficiency_metric

def main():
    st.title('Calculadora de Deficiencia del Programador')

    hours_worked = st.number_input('Ingrese el número de horas trabajadas:', min_value=0.0, step=1.0)

    if st.button('Calcular'):
        # Hacer la llamada al servidor externo para predecir la métrica
        predicted_efficiency = make_prediction(hours_worked)
        
        if predicted_efficiency is not None:
            # Calcular la métrica relacionada con la deficiencia del programador
            deficiency_result = calculate_deficiency(hours_worked)
            
            st.write(f'Deficiencia del programador por exceder las horas establecidas ({hours_worked} horas trabajadas): {deficiency_result}')
            st.write(f'Métrica predicha por el servidor externo: {predicted_efficiency}')
            
            # Mostrar la fórmula y=3x+2
            st.write('Fórmula: y = 3x + 2')

if __name__ == '__main__':
    main()

