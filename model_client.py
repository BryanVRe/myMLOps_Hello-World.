import streamlit as st
import requests

SERVER_URL = 'https://linear-model-service-bryanvre.cloud.okteto.net/v1/models/linear-model:predict'

def make_prediction(hours_worked):
    # Hacer una solicitud al servidor externo para predecir la métrica
    payload = {'instances': [hours_worked]}
    response = requests.post(SERVER_URL, json=payload)
    response.raise_for_status()
    prediction = response.json()
    return prediction['predictions'][0][0]

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
        
        # Calcular la métrica relacionada con la deficiencia del programador
        deficiency_result = calculate_deficiency(hours_worked)
        
        st.write(f'Deficiencia del programador por exceder las horas establecidas ({hours_worked} horas trabajadas): {deficiency_result}')
        st.write(f'Métrica predicha por el servidor externo: {predicted_efficiency}')

if __name__ == '__main__':
    main()
