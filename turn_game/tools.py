class Ability:
    def __init__(self, name, description, damage=0, duration=0, max_uses=1, blocks_attack=False, heal=0):
        self.name = name
        self.description = description
        self.damage = damage
        self.duration = duration
        self.max_uses = max_uses
        self.remaining_uses = max_uses
        self.blocks_attack = blocks_attack
        self.heal = heal
        self.active_turns = 0

    def can_use(self):
        return self.remaining_uses > 0

    def activate(self):
        if self.can_use():
            self.remaining_uses -= 1
            self.active_turns = self.duration

    def tick(self):
        if self.active_turns > 0:
            self.active_turns -= 1

    def is_active(self):
        return self.active_turns > 0
