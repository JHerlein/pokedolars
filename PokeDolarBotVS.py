import time
import datetime
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import requests
from lxml import html
import tweepy
import json
import PokemonFight
import random

df_pokemon = pd.read_excel(r"C:\Users\Julian\PokeDolarBot\dfpokemonv2.xlsx")

#Cargo el JSON con los datos de los pokemon
pokemons_file = open("C:\\Users\Julian\PokeDolarBot\pokedex.json", 'r', encoding="utf8")

pokemonJson = json.load(pokemons_file)

pokemons_file.close()

# access_token = "345520234-Fb0VwXc8ERDoHvC51EdFFwLGCAO38gTThA38nD1L"        Julian Herlein
# access_token_secret = "9tX4KgnEp4EykCkeyp1H190wdUjeOQ2AUVSaQyqG3VZeG"
# consumer_key = "hiwF2GMZ3gqIQywkDqEj00Jm7"
# consumer_secret = "EmgKibJje0Kj3mIAxv7h7cvzmCA8XDyjI7wHWEgUcxTPlPWF4t"

access_token = "1263554175071371266-ehGJPgYyoWtOIe8ulfjIlFmciHEPMS"
access_token_secret = "UcYh6dpJhnGYa8JN6VyinZk1tkNF8CncUFN87US8HOP24"
consumer_key = "xciTqiAYrubn54eBl8IQvlCII"
consumer_secret = "rlUfeukX3t1MjgxA7rzRBmuPTx2b3L5iN4SxxYEbRWyaf6QVZk"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

# pokename = df_pokemon.iloc[index_pokemon,2]

api = tweepy.API(auth)

subio = True
subio_intra = True

#i = 0

precio_today_anterior = 110

#dolar_mep_round = 115

while True:

    print("Arranca el while \n")
    # Aca poner para que solo se active de lunes a viernes a las 18hs
    time.sleep(10)
    hora = datetime.datetime.now()
    print("La hora es " + str(hora))
    if hora.hour == 12  or hora.hour == 15 or hora.hour == 17:
        # if hora.second > 0:
        #i = i + 1
        print("Empieza el escaneo del dolar \n")

        url_mep = urllib.request.urlopen(
            "https://www.rava.com/empresas/perfil.php?e=DOLAR%20MEP").read()  # .decode()

        soup = BeautifulSoup(url_mep,features="lxml")

        # Dato del dia MEP Rava
        print("Se cargo la pagina \n")

        mep = soup.find_all("span", class_="fontsize6")
        dolar_mep = mep[0].text
        dolar_mep_round = int(dolar_mep.split("$", 1)[0].split(",", 1)[0])
        dolar_mep = int(dolar_mep.split("$", 1)[0].split(",", 1)[
                     0]) + int(dolar_mep.split("$", 1)[0].split(",", 1)[1])/100
        # Para ver si vario el dolar_mep desde la ultima medicion

        variacion_intraday = round(
            ((dolar_mep - precio_today_anterior)/precio_today_anterior)*100, 2)

        precio_today_anterior = dolar_mep

        # Dato del dia anterior MEP Rava

        prueba = soup.find_all("td", align="right", style="")
        #print(prueba)
        precio_ant = prueba[0].text
        precio_ant_round = int(precio_ant.split("$", 1)[0].split(",", 1)[0])
        precio_ant = int(precio_ant.split("$", 1)[0].split(",", 1)[
                         0]) + int(precio_ant.split("$", 1)[0].split(",", 1)[1])/100
        variacion = round(((dolar_mep - precio_ant)/precio_ant)*100, 2)
        index_pokemon = dolar_mep_round - 1

         # Dato del dia Blue Dolar Hoy
        
        url_blue = urllib.request.urlopen("https://www.dolarhoy.com/cotizaciondolarblue").read()

        soup_blue = BeautifulSoup(url_blue, features="lxml")

        dolar_blue = soup_blue.find_all("span", class_="pull-right")[1].text
        #print(soup_blue.find_all("span", class_="pull-right"))

        precio_round_blue = int(dolar_blue.split("$", 1)[1].split(",",1)[0])

        precio_blue = int(dolar_blue.split("$", 1)[1].split(",", 1)[0]) + int(dolar_blue.split("$", 1)[1].split(",", 1)[1])/100

        index_pokemon_blue = precio_round_blue - 1

        # Nombre del pokemon Mep / blue

        pokename = df_pokemon.iloc[index_pokemon, 2]

        pokename_blue = df_pokemon.iloc[index_pokemon_blue, 2]

        # URL para descargar la imagen MEP

        URL = df_pokemon.iloc[index_pokemon, 1]
        URL_blue = df_pokemon.iloc[index_pokemon_blue, 1]


        # Nombre del archivo a guardar MEP

        img_name = df_pokemon.iloc[index_pokemon, 3] + ".jpg"
        img_name_blue = df_pokemon.iloc[index_pokemon_blue, 3] + ".jpg"


        #print(img_name)
        #print(URL)
        # Creacion de la imagen en el archivo local

        urllib.request.urlretrieve(URL, img_name)
        urllib.request.urlretrieve(URL_blue, img_name_blue)

        print("El valor del dolar es " + str(dolar_mep_round) +
              " y el pokemon es: " + img_name + "\n")
        print("El valor del dolar blue es " + str(precio_blue) +
              " y el pokemon es: " + img_name_blue + "\n")

        if variacion_intraday > 0:
            subio_intra = True
            print("El dolar subio \n " + str(variacion_intraday) + "%")
        elif variacion_intraday < 0:
            subio_intra = False
            print("El dolar bajo " + str(variacion_intraday) + "%")
        else:
            print("El dolar se mantuvo \n")

        if variacion > 0:
            subio_ = True
            print("El dolar subio \n " + str(variacion) + "%")
        else:
            subio = False
            print("El dolar bajo \n " + str(variacion) + "%")

        imagepath = "{}".format(img_name)

        tweets = api.user_timeline("PokeDolarBotAR")

        hora1 = datetime.datetime.now()

        count_tweets = 0
        for tw in tweets:
            if tw.created_at.day == hora1.day and tw.created_at.month == hora1.month:
                count_tweets = count_tweets + 1
        print(count_tweets)
        if count_tweets > 0:
            first_tweet = False
        else:
            first_tweet = True

        if first_tweet:  
            status_template = "El precio del dolar es ${}\n\n #{} - {}"
        elif subio_intra:
            status_template = "El dolar subio a ${} :(\n\n #{} - {}"
        elif not subio_intra and variacion_intraday < 0:
            status_template = "El dolar bajo a ${} :)\n\n #{} - {}"
        elif not subio_intra and variacion_intraday == 0:
            status_template = "El precio del dolar es ${}\n\n #{} - {}"

        status = status_template.format(dolar_mep, dolar_mep_round, pokename)

        print(status)

        api.update_with_media(imagepath,status)
        #dolar_mep_round = dolar_mep_round + 1

        #time.sleep(3660)
        # time.sleep(15)
        
        print("Verifica la hora para el versus")
        if hora.hour == 17:
            #Cargo los atributos del primer Pokemon
            pokemonIndex1 = index_pokemon
            pokemon_id = dolar_mep_round
            newPokemon1 = pokemonJson[pokemonIndex1]
            newPokemonClass1 = newPokemon1["type"][0]
            newPokemonName1 = newPokemon1["name"]["english"]
            newPokemonAttack1 = newPokemon1["base"]["Attack"]
            newPokemonDefense1 = newPokemon1["base"]["Defense"]

            #Cargo los atributos del Segundo Pokemon

            pokemonIndex2 = index_pokemon_blue
            pokemon_id2 = precio_round_blue
            newPokemon2 = pokemonJson[pokemonIndex2]
            newPokemonClass2 = newPokemon2["type"][0]
            newPokemonName2 = newPokemon2["name"]["english"]
            newPokemonAttack2 = newPokemon2["base"]["Attack"]
            newPokemonDefense2 = newPokemon2["base"]["Defense"]
            
            Pokemon3 = PokemonFight.Pokemon(newPokemonName1,newPokemonAttack1,newPokemonDefense1,newPokemonClass1,pokemon_id)

            Pokemon4 = PokemonFight.Pokemon(newPokemonName2,newPokemonAttack2,newPokemonDefense2,newPokemonClass2,pokemon_id2)

            poke_ganador, log, log1, pokemon_ganadorid = Pokemon3.fight(Pokemon4)

            print("")

            print(poke_ganador)

            status_template_fight = "Dolar MEP: #{} - {}\n\n vs \n\nDolar Blue #{} - {}"

            statusFight = status_template_fight.format(dolar_mep_round,pokename,precio_round_blue,pokename_blue)

            filenames = [img_name,img_name_blue]

            media_ids = []
            for filename in filenames:
                res = api.media_upload(filename)
                media_ids.append(res.media_id)

            api.update_status(status= statusFight, media_ids=media_ids)
            time.sleep(5)
            #print(log + log1 + poke_ganador + " ha ganado")
            tweets1 = api.user_timeline("PokeDolarBotAR")
            #print(tweets1[0])
            tweetid = tweets1[0].id
            index_pokemon_ganador = pokemon_ganadorid - 1
            img_name_ganador = df_pokemon.iloc[index_pokemon_ganador, 3] + ".jpg"
            status = log + log1 + poke_ganador + " ha ganado"
            if len(status) > 280:
                status = log1 + poke_ganador + " ha ganado"
            else:
                status = log + log1 + poke_ganador + " ha ganado"
            
            # print("Este es el log" + log)
            # print("Este es el log1" + log1)
            # print("Este es el poke ganador" + poke_ganador)
            

            api.update_with_media(img_name_ganador,status,in_reply_to_status_id = tweetid)
            time.sleep(3660)
        else:
            print("No twitteo el vs")
            time.sleep(3660)

    else:
        time.sleep(3660)






            


        


