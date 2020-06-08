#if __name__ == '__main__':
import json
import random

pokemons_file = open("C:\\Users\Julian\PokeDolarBot\pokedex.json", 'r', encoding="utf8")

pokemonJson = json.load(pokemons_file)

pokemons_file.close()

#Cargo los atributos del primer Pokemon
pokemonID = 7
pokemonIndex1 = pokemonID - 1
newPokemon1 = pokemonJson[pokemonIndex1]
newPokemonClass1 = newPokemon1["type"][0]
newPokemonName1 = newPokemon1["name"]["english"]
newPokemonAttack1 = newPokemon1["base"]["Attack"]
newPokemonDefense1 = newPokemon1["base"]["Defense"]

#Cargo los atributos del Segundo Pokemon
pokemonID2 = 5
pokemonIndex2 = pokemonID2 - 1
newPokemon2 = pokemonJson[pokemonIndex2]
newPokemonClass2 = newPokemon2["type"][0]
newPokemonName2 = newPokemon2["name"]["english"]
newPokemonAttack2 = newPokemon2["base"]["Attack"]
newPokemonDefense2 = newPokemon2["base"]["Defense"]



# {'id': 1,
#  'name': {'english': 'Bulbasaur',
#   'japanese': 'フシギダネ',
#   'chinese': '妙蛙种子',
#   'french': 'Bulbizarre'},
#  'type': ['Grass', 'Poison'],
#  'base': {'HP': 45,
#   'Attack': 49,
#   'Defense': 49,
#   'Sp. Attack': 65,
#   'Sp. Defense': 65,
#   'Speed': 45}}


class Pokemon:
    
    debilidad = { "debilidades" : { "Grass": ["Water","Ground","Rock"],
                                    "Rock" : ["Fire","Ice","Flying","Bug"],
                                    "Ice": ["Grass","Ground","Flying","Dragon"],
                                    "Dragon": ["Dragon"],
                                    "Dark":["Psychic", "Ghost"],
                                    "Psychic":["Fighting", "Poison"],
                                    "Bug": ["Grass", "Psychic", "Dark"],
                                    "Flying": ["Grass", "Fighting", "Bug"],
                                    "Steel": ["Ice", "Rock", "Fairy"],
                                    "Fire": ["Grass", "Ice", "Bug"],
                                    "Fighting": ["Normal", "Ice","Rock", "Dark"],
                                    "Ground": ["Fire", "Electric", "Poison", "Rock", "Steel"],
                                    "Ghost": ["Psychic", "Ghost"],
                                    "Poison": ["Grass", "Fairy"],
                                    "Water":["Fire", "Ground", "Rock"],
                                    "Fairy": ["Fire", "Ground", "Rock"],
                                    "Electric": ["Water", "Flying"],
                                    "Normal": "none"
                            
                                    }
                }
    
    
    def __init__(self, nombre,ataque,defensa,clase,id):
        self.nombre = nombre
        self.vida = 5 * defensa
        self.ataque = ataque
        self.defensa = defensa
        self.clase = clase
        self.id = id
    
    def attack(self, Pokemon2):
        global battle_log
        battle_log = ""
        
#         print(self.debilidad["debilidades"][self.clase])
#         print(self.debilidad["debilidades"][Pokemon2.clase])
        
        
        if Pokemon2.clase in self.debilidad["debilidades"][self.clase]:
            multiplicador1 = 1.5
        else:
            multiplicador1 = 1
        if self.clase in self.debilidad["debilidades"][Pokemon2.clase]:
            multiplicador2 = 1.5
        else:
            multiplicador2 = 1
        while Pokemon2.vida > 0 and self.vida > 0:
            ataque1 = round((self.ataque * (Pokemon2.defensa/100) * multiplicador1),2)
            ataque2 = round((Pokemon2.ataque * (self.defensa/100) * multiplicador2),2)
            #str1 = self.nombre + " ha infligido " + str(ataque1) + " de daño a " + Pokemon2.nombre + "\n"
            #print(str1)
            #battle_log = battle_log + str1
            rng = round(random.random()*10)
            if rng < 2:
                ataque1 = 0
            elif rng > 8:
                ataque1 = ataque1 * 1.3
            else:
                ataque1 = ataque1
            Pokemon2.vida = round((Pokemon2.vida - ataque1),2)
            str1 = self.nombre + " ha infligido " + str(ataque1) + " de daño a " + Pokemon2.nombre + "\n"
            #print(str1)
            battle_log = battle_log + str1
            if Pokemon2.vida > 0:
                rng = round(random.random()*10)
                if rng < 2:
                    ataque2 = 0
                elif rng > 8:
                    ataque2 = ataque2 * 1.3
                else:
                    ataque2 = ataque2
                self.vida = round((self.vida - ataque2),2)
                str2 = Pokemon2.nombre + " ha infligido " + str(ataque2) + " de daño a " + self.nombre + "\n"
                #print(str2)
                battle_log = battle_log + str2
            if self.vida < 0:
                self.vida = 0
                #return battle_log
            #return battle_log
            if Pokemon2.vida < 0:
                Pokemon2.vida == 0
            #return battle_log
            
                    

    def fight(self, Pokemon2):
        battle_log2 = ""
        self.attack(Pokemon2)
        if self.vida < 0:
            self.vida = 0
        if Pokemon2.vida < 0:
            Pokemon2.vida = 0
        str1 = "La vida restante de " + Pokemon2.nombre + " es " + str(Pokemon2.vida) + "\n" 
        #print(str1)
        battle_log2 = battle_log2 + str1
        str2 = "La vida restante de " + self.nombre + " es " + str(self.vida) + "\n"
        #print(str2)
        battle_log2 = battle_log2 + str2
        if self.vida == 0:
            #global pokemon_ganador               
            pokemon_ganador  = Pokemon2.nombre
            pokemon_ganador_id = Pokemon2.id
            #print(Pokemon2.nombre + " ha ganado")
            #return pokemon_ganador
        elif Pokemon2.vida == 0:
            #global pokemon_ganador
            pokemon_ganador  = self.nombre
            pokemon_ganador_id = self.id
            #print(self.nombre + " ha ganado")
            #return pokemon_ganador
        return pokemon_ganador, battle_log, battle_log2, pokemon_ganador_id
    
        

                
# Pokemon1 = Pokemon(newPokemonName1,newPokemonAttack1,newPokemonDefense1,newPokemonClass1,pokemonID)

# Pokemon2 = Pokemon(newPokemonName2,newPokemonAttack2,newPokemonDefense2,newPokemonClass2,pokemonID2)

# poke_ganador, battle_log, battle_log2, pokemon_ganador_id = Pokemon1.fight(Pokemon2)

# print(poke_ganador)
# print(battle_log)
# print(battle_log2)
# print(pokemon_ganador_id)


