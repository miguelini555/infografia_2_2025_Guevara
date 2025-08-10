import random
from tools import Ability

class Character:
    def __init__(self, hp: int, base_damage: int, parry_prob: float, crit_prob: float, abilities=None):
        self.hp= hp
        self.base_damage = base_damage
        self.parry_prob = parry_prob
        self.crit_prob = crit_prob
        self.name = "default"
        self.abilities = abilities if abilities else []

    def attack(self, other):
        damage = self.base_damage * 2 if random.random()<=self.crit_prob else self.base_damage
        print(f"{self.name} atacando a {other} con {damage} danio")
        other.hurt(damage)

    def use_ability(self, ability, target):
        ability.activate()
        if ability.damage > 0:
            print(f"{self.name} usa {ability.name} contra {target.name} causando {ability.damage} de danio")
            target.hurt(ability.damage)
        if ability.heal > 0:
            self.hp += ability.heal
            print(f"{self.name} se cura {ability.heal} puntos de vida. HP actual: {self.hp}")


    def hurt(self, damage: int):
        damage_taken = 0 if random.random()<=self.parry_prob else damage
        self.hp -= damage_taken
        print(f"{self.name} exclama ouch! recibido danio  de {damage_taken}, hp restante: {self.hp}")

    def set_name(self, name):
        self.name = name

    def tick_abilities(self):
        for ab in self.abilities:
            ab.tick()