# Examen_Mercadolibre

# Instrucciones de cómo ejecutar el programa
El objetivo del ejercicio es detectar en una matiz NxN con las letras (A, T, C, G) si el ADN corresponde a un humano o a un mutante. El ADN es de un mutante si posee más de una secuencia de 4 letras iguales sea de forma horizontal, vertical u oblicua.

El lenguaje de desarrollo en el cual se realizó la programación es PYTHON y se utilizó AWS para alojar la API REST

Dentro de AWS utilizamos la funcionalidad de LAMBDA para construir en python toda la lógica que no solo evalúa las matrices para concluir si son o no mutantes, sino también toda la interacción con los web services (/mutant y /stats) a través de la API REST. Toda esta integracion la posibilita la funcionalidad API GATEWAY de AWS.

Para almacenar los ADNs a evaluar y sus respectivos veredictos alrededor de si son mutantes o humanos utilizamos DYNAMOBD que es una funcionalidad de bases de datos dentro de AWS que posibilita una fácil integración con las otras funciones LAMBDA y API GATEWAY mencionadas arriba.

Para Interactuar con la API y utilizar sus funcionalidad podemos utilizar POSTMAN para hacer los POST a traves del servicio "/mutant" de los ADNs a evaluar en formato JSON, así:

{
“DNA”: ["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]
}

De este modo este registro queda guardado en la base de datos DYNAMODB. De igual manera, POSTMAN nos permite ver la respuesta del servidor, si el ADN es de un mutante nos devuelve TRUE y el código 200 (ok); si por el contrario es de un humano nos retorna FALSE y el código 403 (forbidden)

Para ver las estadística de los diferentes ADNs evaluados y alojados en la base de datos utilizamos el servicio "/stats" a través de un GET y obtenemos una respuesta en formato JSON como podemos ver a continuación:

{
    "count_mutant_dna": 2,
    "count_human_dna": 3,
    "ratio": 0.67
}

# URL de la API
https://jcab6ai39i.execute-api.us-east-1.amazonaws.com/prod
