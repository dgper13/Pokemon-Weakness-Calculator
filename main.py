import sys
import requests

API_URL = "https://pokeapi.co/api/v2/pokemon/"


class Pokemon:
    def __init__(self, name, damageRelations):
        self.name = name
        self.damageRelations = damageRelations
        self.weaknesses = set()
    
    def getWeaknesses(self):
        lessDamageFrom = set()

        for i in range(len(self.damageRelations)):
            
            typeWeaknesses = self.damageRelations[i]["double_damage_from"]
            for types in typeWeaknesses:
                self.weaknesses.update([types["name"]])
            
            typeImmunities = self.damageRelations[i]["no_damage_from"]
            for types in typeImmunities:
                lessDamageFrom.update([types["name"]])
            
            typeHalfDamage = self.damageRelations[i]["half_damage_from"]
            for types in typeHalfDamage:
                lessDamageFrom.update([types["name"]])

        for type in lessDamageFrom:
            self.weaknesses.discard(type)

        return self.weaknesses
    

class Team:
    def __init__(self):
        self.team = []
    
    def addMember(self, newMember):
        self.team.append(newMember)

    def getTeamSize(self):
        return len(self.team)
    
    def showResults(self):
        print("--------------------------------------")

        for member in self.team:
            print(f'{member.name} <- ', end="")
            weaknesses = list(member.getWeaknesses())
            for j in range(len(weaknesses)-1):
                print(f'{weaknesses[j]},', end=" ")
            print(weaknesses[-1])


def createTeam():
    team = Team()

    args = sys.argv[1:]
    for pokemon in args:
        damageRelations = []

        try:
            r = requests.get(API_URL + pokemon)
            r.raise_for_status()
            r = r.json()["types"]

            for i in range(len(r)):
                url = r[i]["type"]["url"]
                try:
                    r2 = requests.get(url)
                    r2.raise_for_status()
                    damageRelations.append(r2.json()["damage_relations"])
                except requests.exceptions.HTTPError as err:
                    print("Error.")
                    exit()
            
            newMember = Pokemon(pokemon, damageRelations)
            team.addMember(newMember)

        except requests.exceptions.HTTPError as err:
            print (f"'{pokemon}' is not a valid Pokemon.")

    return team


if __name__ == '__main__':
    team = createTeam()
    team.showResults()