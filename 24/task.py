#!/usr/bin/env pipenv-run
import sys
import re
from itertools import chain, count

class Army():
    def __init__(self, name):
        self.name = name
        self.sealed_groups = None
        self.reset()

    def seal(self):
        self.sealed_groups = set(self.groups)

    def reset(self):
        if self.sealed_groups is None:
            self.groups = set()
        else:
            self.groups = set(self.sealed_groups)
        self.targetable_groups = None
        self.dead_groups = set()
        for group in self.groups:
            group.reset()

    def set_enemy_army(self, army):
        self.enemy_army = army

    def add_group(self, group):
        group.army = self
        group.number = len(self.groups) + 1
        self.groups.add(group)

    def get_groups(self):
        return self.groups

    def reset_targetable(self):
        self.targetable_groups = set(self.groups)

    def mark_untargetable(self, group):
        self.targetable_groups.remove(group)

    def mark_dead(self, group):
        self.groups.remove(group)
        self.dead_groups.add(group)

    def is_alive(self):
        return len(self.groups) > 0

    def describe_with(self, func):
        result = list()
        result.append('{}:'.format(self.name))
        if len(self.groups) == 0:
            result.append('No groups remain')
        else:
            for group in sorted(self.groups, key=ArmyGroup.get_number):
                result.append('Group {} contains {}'.format(group.number, func(group)))
        return result

    def describe(self):
        return self.describe_with(ArmyGroup.describe)

    def describe_short(self):
        return self.describe_with(ArmyGroup.describe_short)

    def __repr__(self):
        return self.name

class ArmyGroup:
    pattern = re.compile('^(\d+) units each with (\d+) hit points (?:\((\w+) to ((?:\w+(?:, )?)+)(?:; )?(?:(\w+) to ((?:\w+(?:, )?)+))?\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)$')

    def __init__(self, line):
        match = ArmyGroup.pattern.match(line)
        self.units = int(match.group(1))
        self.sealed_units = self.units
        self.hp_per_unit = int(match.group(2))
        self.weaknesses = frozenset()
        self.immunities = frozenset()
        for alignment, types in ((match.group(3), match.group(4)), (match.group(5), match.group(6))):
            if alignment:
                types = frozenset(types.split(', '))
                if alignment == 'weak':
                    self.weaknesses = types
                elif alignment == 'immune':
                    self.immunities = types
                else:
                    raise 'Unknown alignment "{}"'.format(alignment)
        self.attack_damage = int(match.group(7))
        self.sealed_attack_damage = self.attack_damage
        self.attack_type = match.group(8)
        self.initiative = int(match.group(9))
        self.army = None
        self.number = None

    def reset(self):
        self.units = self.sealed_units
        self.attack_damage = self.sealed_attack_damage

    def get_number(self):
        return self.number

    def get_units(self):
        return self.units

    def effective_power(self):
        return self.units * self.attack_damage

    def damage_to_group(self, group):
        if self.attack_type in group.immunities:
            return 0
        if self.attack_type in group.weaknesses:
            return self.effective_power() * 2
        return self.effective_power()

    def damage_order(self, group):
        return (self.damage_to_group(group), group.effective_power(), group.initiative)

    def target_order(self):
        return (self.effective_power(), self.initiative)

    def target(self, army):
        if not army.groups:
            return None
        group = max(army.targetable_groups, key=self.damage_order, default=None)
        if group is None or self.damage_to_group(group) == 0:
            return None
        army.mark_untargetable(group)
        return group

    def attack_order(self):
        return self.initiative

    def attack(self, group):
        if group is None:
            return
        units_killed = group.defend(self.damage_to_group(group))
        return units_killed

    def defend(self, damage):
        units_lost = min(self.units, damage // self.hp_per_unit)
        self.units = self.units - units_lost
        if self.units == 0:
            self.army.mark_dead(self)
        return units_lost

    def describe(self):
        weaknesses = ', '.join(self.weaknesses)
        immunities = ', '.join(self.immunities)
        alignments = list()
        if weaknesses:
            weaknesses = 'weak to {}'.format(weaknesses)
            alignments.append(weaknesses)
        if immunities:
            immunities = 'immune to {}'.format(immunities)
            alignments.append(immunities)
        alignments = ' ({}) '.format('; '.join(alignments)) if alignments else ' '
        return ('{} units each with {} hit points{}with an attack that does {} {} damage at initiative {}'
                .format(self.units, self.hp_per_unit, alignments, self.attack_damage, self.attack_type, self.initiative))

    def describe_short(self):
        return '{} units'.format(self.units)

    def __repr__(self):
        return '{} group {}'.format(self.army.name, self.number)

    def __hash__(self):
        return hash((self.army.name, self.number))

immune_system = Army('Immune System')
infection = Army('Infection')
immune_system.set_enemy_army(infection)
infection.set_enemy_army(immune_system)
armies_by_name = dict()
for army in (immune_system, infection):
    armies_by_name[army.name] = army
army = None

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line.endswith(':'):
        line = line[:-1]
        army = armies_by_name[line]
    else:
        army.add_group(ArmyGroup(line))

for army in armies_by_name.values():
    army.seal()

def fight(armies_by_name, boost=0, verbose=True):
    for army in armies_by_name.values():
        army.reset()

    if boost > 0:
        for group in armies_by_name['Immune System'].groups:
            group.attack_damage = group.attack_damage + boost

    if verbose:
        for army in armies_by_name.values():
            for line in army.describe():
                print(line)
            print()

    fight_round = 0
    stalemate = False
    while sum(map(Army.is_alive, armies_by_name.values())) > 1:
        fight_round = fight_round + 1
        if verbose:
            print('========Round {}========'.format(fight_round))
            for army in armies_by_name.values():
                for line in army.describe_short():
                    print(line)
            print()

        for army in armies_by_name.values():
            army.reset_targetable()
        target_groups = list(chain(*map(Army.get_groups, armies_by_name.values())))
        target_groups.sort(key=ArmyGroup.target_order, reverse=True)
        attack_groups = list()
        for group in target_groups:
            target = group.target(group.army.enemy_army)
            if target is None:
                continue
            attack_groups.append((group, target))
            damage = group.damage_to_group(target)
            if verbose:
                print('{} would deal defending group {} {} damage'.format(group, target.number, damage))
        if verbose:
            print()

        attack_groups.sort(key=lambda gt: gt[0].attack_order(), reverse=True)
        total_units_killed = 0
        for group, target in attack_groups:
            if group.units == 0:
                continue
            units_killed = group.attack(target)
            total_units_killed = total_units_killed + units_killed
            if verbose:
                print('{} attacks defending group {}, killing {} units'.format(group, target.number, units_killed))
        if verbose:
            print()
        if total_units_killed == 0:
            stalemate = True
            break

    if verbose:
        print('========Combat end========'.format(fight_round))
        for army in armies_by_name.values():
            for line in army.describe_short():
                print(line)
        print()

    if stalemate:
        return (stalemate, (None, fight_round, None))
    winning_army = next(army for army in armies_by_name.values() if army.is_alive())
    units_left = sum(map(ArmyGroup.get_units, winning_army.groups))
    return (stalemate, (winning_army, fight_round, units_left))

task01_stalemate, task01_result = fight(armies_by_name, verbose=False)
if task01_stalemate:
    print('This should happen')
    exit()
print('Task 01: {} wins after {} rounds with {} units left'.format(*task01_result))

def fight_pow(lower_boost, last_state):
    last_lower_boost = lower_boost
    for boost_pow in count():
        boost = lower_boost + 2**boost_pow
        state = fight(armies_by_name, boost, verbose=False)
        stalemate = state[0]
        winning_army = state[1][0]
        if not stalemate and winning_army.name == 'Immune System':
            return ((last_lower_boost, last_state), (boost, state))
        last_lower_boost = boost
        last_state = state

lower_boost = 0
lower_state = (False, task01_result)
last_lower_state = None
while True:
    (lower_boost, lower_state), (upper_boost, upper_state) = fight_pow(lower_boost, lower_state)
    if lower_state == last_lower_state:
        print('Task 02: With a boost of {}, {} wins after {} rounds with {} units left'.format(upper_boost, *upper_state[1]))
        break
    last_lower_state = lower_state
