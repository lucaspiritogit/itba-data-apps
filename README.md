# WOWTPC | World of Warcraft Token Price Check

WOWTPC es un DAG que utiliza una API gratuita la comunidad de [Blizzard/BattleNet](https://us.shop.battle.net/es-es) sobre el juego MMORPG [World of Warcraft](https://worldofwarcraft.blizzard.com/es-es/). El DAG busca diariamente el endpoint de `data/wow/token` para saber el precio de cada dia del WoW Token.

## ¿Que es un WoW Token?

Dado que el World of Warcraft es un juego que se paga mensualmente, se creo el "wow token" para permitir a los jugadores intercambiar oro (moneda principal del juego) por una **wow token**. Estos tokens pueden ser utilizados para conseguir 1 mes adicional de juego.

# Pre-requisitos

- Tener docker instalado

# Componentes principales del DAG

## dag.py

Modulo donde se almacenan las instrucciones y configuraciones de cada Task y el orden de ejecucion

## api.py

Modulo donde se interactua con la API de Battle Net para buscar el precio de los wow tokens actual.

## database_functions.py

Modulo que tiene una interaccion con la base de datos, es como el repository de la aplicacion.
Adicionalmente se encarga de procesar la informacion y generar un .csv en `/output` en la raiz del proyecto con los datos mediante el uso de dataframes con pandas.

# Como probar la aplicacion

1. Clonar el repositorio: `git clone https://github.com/lucaspiritogit/dag-wow-token-price-check`
2. Entrar a la carpeta del repositorio clonado
3. Crear un archivo `.env` (_no es necesario poner ninguna credencial_)
4. En la terminal de preferencia, ejecutar: `docker compose up`
5. Abrir un navegador en modo incognito y dirigirse a http://localhost:8080
6. Ingresar al airflow con las siguientes credenciales:
   1. user: airflow
   2. pass airflow
