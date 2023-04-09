# pruebaNW

Documentación de la API para predicción del atraso de vuelos comerciales
Descripción general

La API se encarga de realizar predicciones sobre el atraso de los vuelos comerciales, utilizando dos modelos de inteligencia artificial. Los modelos disponibles son Random Forest y Red Neuronal.

#Endpoints

##/rf

Método: POST

Este endpoint se encarga de realizar la predicción del atraso utilizando el modelo de Random Forest.
Input

El input que espera el endpoint es un JSON con un arreglo de valores numéricos. El arreglo debe tener 8 elementos, que corresponden a las siguientes características:

    Hora de salida (en formato decimal)
    Día de la semana (1=Lunes, 2=Martes, ..., 7=Domingo)
    Mes (1=Enero, 2=Febrero, ..., 12=Diciembre)
    Aeropuerto de origen (1=ATL, 2=CLT, ..., 6=SFO)
    Aeropuerto de destino (1=ATL, 2=CLT, ..., 6=SFO)
    Línea aérea (1=AA, 2=AS, ..., 14=WN)
    Tiempo de vuelo (en minutos)
    Distancia de vuelo (en millas)

Ejemplo:

json

{
  "values": [10.5, 3, 4, 2, 4, 7, 120, 750]
}

Output

El output que devuelve el endpoint es un JSON con la predicción del modelo de Random Forest en formato numérico. El valor predicho representa el atraso en minutos del vuelo.

Ejemplo:

json

{
  "value": 10
}

##/torch

Método: POST

Este endpoint se encarga de realizar la predicción del atraso utilizando el modelo de Red Neuronal.
Input

El input que espera el endpoint es un JSON con un arreglo de valores numéricos. El arreglo debe tener 8 elementos, que corresponden a las mismas características que en el modelo de Random Forest.

Ejemplo:

json

{
  "values": [10.5, 3, 4, 2, 4, 7, 120, 750]
}

Output

El output que devuelve el endpoint es un JSON con la predicción del modelo de Red Neuronal en formato numérico. El valor predicho representa la probabilidad de que el vuelo tenga un atraso mayor a 15 minutos.

Ejemplo:

json

{
  "value": 0.2
}

Red Neuronal

La red neuronal implementada en este proyecto está basada en un autoencoder, que es una arquitectura de red neuronal utilizada en el aprendizaje no supervisado de datos. Esta red está diseñada para aprender una representación de los datos de entrada, en este caso, las características de los vuelos, y posteriormente utilizar esta representación para realizar una clasificación binaria (retraso o no retraso).

La red neuronal consta de dos partes principales: el codificador (encoder) y el decodificador (decoder). El codificador recibe los datos de entrada y los reduce a una representación más pequeña, mientras que el decodificador toma la representación y trata de reconstruir los datos originales.

La arquitectura de la red neuronal utilizada en este proyecto está formada por capas lineales (o completamente conectadas) con funciones de activación ReLU (Rectified Linear Unit) y una capa de salida con una función de activación sigmoide, lo que permite realizar una clasificación binaria.

Además, se ha implementado una técnica llamada dropout, que consiste en "apagar" aleatoriamente algunas neuronas durante el entrenamiento para evitar el sobreajuste (overfitting) de la red.
Combinación de modelos

La red neuronal se utiliza junto con un modelo de clasificación basado en Random Forest para realizar la clasificación de los vuelos. El modelo de Random Forest se utiliza como modelo de backup en caso de que la red neuronal no pueda realizar la clasificación.

Para combinar los modelos, se utiliza un modelo híbrido llamado AutoencoderClassifier, que combina el autoencoder y el modelo de clasificación en una sola red neuronal. En primer lugar, los datos de entrada se procesan mediante el autoencoder para obtener una representación más pequeña, y luego se utiliza la salida del autoencoder como entrada para el modelo de clasificación. La salida final de la red neuronal es la salida del modelo de clasificación.
Uso de la API

La API proporciona dos endpoints para realizar la predicción del retraso de los vuelos:

    /torch: Utiliza el modelo de la red neuronal implementado en PyTorch para realizar la predicción.
    /rf: Utiliza el modelo de Random Forest para realizar la predicción.

Ambos endpoints reciben los datos de entrada en formato JSON, los procesan y devuelven la predicción en formato JSON.
