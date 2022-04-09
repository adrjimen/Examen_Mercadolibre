# Exámen_Mercadolibre

# Instrucciones de cómo ejecutar el programa
El objetivo del ejercicio es detectar en una matriz NxN con las letras (A, T, C, G) si el ADN corresponde a un humano o a un mutante. El ADN es de un mutante si posee más de una secuencia de 4 letras iguales sea de forma horizontal, vertical u oblicua.

A continuación, se describe la lógica de programación para realizar la evaluación mencionada anteriormente:

Búsqueda de secuencias Horizontales: Se recorre cada fila de la matriz con una ventana móvil de tamaño 4. Cada vez que encuentra una ventana con todas las letras iguales aumenta en 1 el contador de número de secuencias iguales.
Búsqueda de secuencias Verticales: Se hace una transpuesta de la matriz original para convertir las columnas en filas y se realiza el mismo proceso de evaluación de secuencias horizontales descrito arriba.
Búsqueda de secuencias Oblicuas (de izquierda a derecha): Se extraen las diagonales de la matriz y se realiza la evaluación a través de la ventana móvil de tamaño 4 en búsqueda de secuencias de una misma letra aumentando el contador cuando esto ocurre.
Búsqueda de secuencias Oblicuas (de derecha a izquierda): Se invierten de izquierda a derecha el orden de las filas de la matriz original (espejo) y se realiza el mismo procedimiento de evaluación que en el caso anterior.

Finalmente, cuando el contador de secuencias alcanza el valor de 2 retorna TRUE (Mutante) si no alcanza es límite retorna FALSE (Humano)

El lenguaje de desarrollo en el cual se realizó la programación es PYTHON y se utilizó AWS para alojar la API REST.

Dentro de AWS se utilizó la funcionalidad de LAMBDA para construir en python toda la lógica que no solo evalúa las matrices para concluir si son o no mutantes, sino también toda la interacción con los web services (/mutant y /stats) a través de la API REST. Toda esta integración la posibilita la funcionalidad API GATEWAY de AWS.

Para almacenar los ADNs a evaluar y sus respectivos veredictos alrededor de si son mutantes o humanos se usó DYNAMOBD que es una funcionalidad de bases de datos dentro de AWS que posibilita una fácil integración con las otras funciones LAMBDA y API GATEWAY mencionadas arriba.

Para Interactuar con la API y utilizar sus funcionalidades se puede utilizar POSTMAN para hacer los POST a traves del servicio "/mutant" de los ADNs a evaluar en formato JSON, así:

{
    "DNA": ["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]
}

De este modo este registro queda guardado en la base de datos DYNAMODB. De igual manera, POSTMAN permite ver la respuesta del servidor, si el ADN es de un mutante devuelve TRUE y el código 200 (ok); si por el contrario es de un humano retorna FALSE y el código 403 (forbidden).

Para ver la estadística de los diferentes ADNs evaluados y alojados en la base de datos se utiliza el servicio "/stats" a través de un GET y se obtiene una respuesta en formato JSON como se puede ver a continuación:

{
    "count_mutant_dna": 2,
    "count_human_dna": 3,
    "ratio": 0.67
}

# URL de la API
https://jcab6ai39i.execute-api.us-east-1.amazonaws.com/prod
