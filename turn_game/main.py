import random
from character  import Character
from tools import Ability

characters_list = {
    "rogue": Character(100, 10, 0.1, 0.4, [
        Ability("Golpe mortal", "Gran golpe con mucho danio", damage=25, max_uses=2),
        Ability("Evasion perfecta", "Evita todo danio por 2 turnos", duration=2, max_uses=1)
    ]),
    "tank": Character(500, 8, 0.3, 0.1, [
        Ability("Golpe aplastante", "Ataque poderoso", damage=20, max_uses=3),
        Ability("Escudo total", "Bloquea ataques por 3 turnos", duration=3, max_uses=1)
    ]),
    "wizard": Character(100, 12, 0.1, 0.4, [
        Ability("Bola de fuego", "Danio magico a un enemigo", damage=30, max_uses=3),
        Ability("Curacion", "Recupera 20 HP", heal=20, max_uses=2, blocks_attack=True)
    ]),
    "paladin": Character(200, 9, 0.2, 0.2, [
        Ability("Luz Milagrosa", "Cura 30 HP", heal=30, max_uses=1, blocks_attack=True),
        Ability("Martillo Mortal", "Gran golpe fisico", damage=22, max_uses=2)
    ])
}

num_players = 0
while num_players < 2 or num_players > 4:
    num_players = int(input("Ingrese un numero de jugadores entre 2 y 4: "))

players = []
for i in range(num_players):
    print("\nPersonajes disponibles: rogue, tank, wizard, paladin")
    choice = input(f"Jugador {i+1}, elija su personaje: ").lower()
    while choice not in characters_list:
        choice = input("Opcion no valida, elija nuevamente: ").lower()

    template = characters_list[choice]
    player_char = Character(template.hp, template.base_damage, template.parry_prob, template.crit_prob,
                            [Ability(a.name, a.description, a.damage, a.duration, a.max_uses, a.blocks_attack, a.heal) for a in template.abilities])
    name = input(f"Jugador {i+1}, ingrese el nombre de su personaje: ")
    player_char.set_name(name)
    players.append(player_char)

n_turns = int(input("\nIngrese numero de turnos: "))

for turn in range(1, n_turns+1):
    print(f"\n___Turno {turn}___")
    random.shuffle(players)

    for attacker in players:
        if attacker.hp <= 0:
            continue
        attacker.tick_abilities()

        if any(ab.is_active() and ab.blocks_attack for ab in attacker.abilities):
            print(f"{attacker.name} sigue usando una habilidad y no puede atacar este turno.")
            continue

        alive_targets = [p for p in players if p != attacker and p.hp > 0]
        if not alive_targets:
            break

        print(f"\nTurno de {attacker.name}")
        print("1. Ataque normal")
        for idx, ab in enumerate(attacker.abilities, start=2):
            status = f"(usos restantes: {ab.remaining_uses})"
            print(f"{idx}. {ab.name} - {ab.description} {status}")

        choice = int(input("Elige una accion: "))

        if choice == 1:
            for idx, target in enumerate(alive_targets):
                print(f"{idx+1}. {target.name} (HP: {target.hp})")
            target_choice = int(input("Elige a quien atacar: ")) - 1
            attacker.attack(alive_targets[target_choice])
        else:
            ability = attacker.abilities[choice-2]
            if not ability.can_use():
                print("No puedes usar esta habilidad, sin usos restantes.")
                continue
            for idx, target in enumerate(alive_targets):
                print(f"{idx+1}. {target.name} (HP: {target.hp})")
            target_choice = int(input("Elige a quien atacar: ")) - 1
            attacker.use_ability(ability, alive_targets[target_choice])

    vivos = [p for p in players if p.hp > 0]
    if len(vivos) <= 1:
        break

print("\n___Fin del combate___")
players.sort(key=lambda p: p.hp, reverse=True)
for p in players:
    print(f"{p.name}: {p.hp} HP")

ganadores = [p for p in players if p.hp > 0]
if len(ganadores) == 1:
    print(f"\n¡El ganador es {ganadores[0].name}!")
elif len(ganadores) > 1:
    print("\n¡Empate entre: " + ", ".join(p.name for p in ganadores) + "!")
else:
    print("\nTodos perdieron, no hay ganador.")