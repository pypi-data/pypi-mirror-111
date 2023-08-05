import string


class Monster:
    """

    Sample monster data:

    'mon': {
        'id': 1,
        'name': 'kobold',
        'plural': 'kobolds',
        'type': 187,
        'typedata': {
            'avghp': 3
        },
        'att': 0,
        'btype': 187,
        'threat': 1
    }


    """

    all_possible_g_values = string.ascii_lowercase + string.ascii_uppercase + ';'

    # current theory: each monster has a unique id, so use this class variable to track them
    ids_to_monsters = {}

    def __init__(self):
        self.name = None
        self.vals = None
        self.ascii_sym = None
        self.id = None
        self.cell = None  # if the monster is on a cell, update it here (note that this could become outdated and we wouldn't know about it)
        self.threat = 0

    @staticmethod
    def create_or_update_monster(vals, ascii_sym):
        if 'id' in vals.keys():
            # check if id already exists, if so, retrieve that Monster instance
            mon_id = vals['id']
            if mon_id in Monster.ids_to_monsters.keys():
                # if this monster already exists, update instead of creating new one
                Monster.ids_to_monsters[mon_id].update(vals, ascii_sym)
                return Monster.ids_to_monsters[mon_id]
            else:
                # create a new monster and insert into Monster.ids_to_monsters
                new_monster = Monster()
                new_monster.update(vals, ascii_sym)
                Monster.ids_to_monsters[new_monster.id] = new_monster
                return new_monster
        elif 'name' in vals.keys() and vals['name'] == 'plant':
            # a plant is not a monster
            return 'plant'
        elif 'name' in vals.keys():
            # create a new monster and don't give it an ID (IDs are reserved for the game to give us)
            new_monster = Monster()
            new_monster.update(vals, ascii_sym)
            return new_monster
        else:
            raise Exception("Monster with no id, here's the vals: {}".format(vals))

    def update(self, vals, ascii_sym):
        self.vals = vals
        self.ascii_sym = ascii_sym
        if 'id' in vals.keys():
            self.id = vals['id']

        if 'name' in vals.keys():
            self.name = vals['name']

        if 'type' in vals.keys():
            self.type = vals['type']

        if 'threat' in vals.keys():
            self.threat = vals['threat']

    def set_cell(self, cell):
        self.cell = cell

    def remove_cell(self):
        # this should happen when a monster dies or is no longer in view
        self.cell = None

    def get_pddl_strs(self, pddl_cell_str):
        strs = [
            "(monsterat {} {} {})".format(self.name, self.id, pddl_cell_str),
        ]
        return strs