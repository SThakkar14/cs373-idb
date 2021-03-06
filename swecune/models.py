from collections import OrderedDict

from sqlalchemy import Column, Integer, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

pokemon_move = Table('pokemon_move', Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
                     Column('move_id', Integer, ForeignKey('move.id')),
                     UniqueConstraint('pokemon_id', 'move_id', name='pokemon_move_relationship')
                     )

double_damage_to = Table('double_damage_to', Base.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('origin', Integer, ForeignKey('type.id')),
                         Column('opposing', Integer, ForeignKey('type.id')),
                         UniqueConstraint('origin', 'opposing', name='double_to_relation')
                         )

double_damage_from = Table('double_damage_from', Base.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('origin', Integer, ForeignKey('type.id')),
                           Column('opposing', Integer, ForeignKey('type.id')),
                           UniqueConstraint('origin', 'opposing', name='double_from_relation')
                           )

half_damage_to = Table('half_damage_to', Base.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('origin', Integer, ForeignKey('type.id')),
                       Column('opposing', Integer, ForeignKey('type.id')),
                       UniqueConstraint('origin', 'opposing', name='half_to_relation')
                       )

half_damage_from = Table('half_damage_from', Base.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('origin', Integer, ForeignKey('type.id')),
                         Column('opposing', Integer, ForeignKey('type.id')),
                         UniqueConstraint('origin', 'opposing', name='half_from_relation')
                         )

no_damage_to = Table('no_damage_to', Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('origin', Integer, ForeignKey('type.id')),
                     Column('opposing', Integer, ForeignKey('type.id')),
                     UniqueConstraint('origin', 'opposing', name='no_to_relation')
                     )

no_damage_from = Table('no_damage_from', Base.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('origin', Integer, ForeignKey('type.id')),
                       Column('opposing', Integer, ForeignKey('type.id')),
                       UniqueConstraint('origin', 'opposing', name='no_from_relation')
                       )


class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    average_stats = Column(Integer)

    primary_type_id = Column(Integer, ForeignKey('type.id'))
    secondary_type_id = Column(Integer, ForeignKey('type.id'))

    primary_type = relationship('Type', backref='pokemon_primary_type', foreign_keys=[primary_type_id])
    secondary_type = relationship('Type', backref='pokemon_secondary_type', foreign_keys=[secondary_type_id])

    moves = relationship('Move', secondary=pokemon_move, back_populates='pokemon')

    def __init__(self, id, name, hp, attack, defense, special_attack, special_defense, speed, average_stats):
        self.id = id
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.average_stats = average_stats

    def dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = self.name.title()
        dictified['stats'] = [
            {
                'base_stat': self.speed,
                'name': 'speed'
            }, {
                'base_stat': self.special_defense,
                'name': 'special_defense'
            }, {
                'base_stat': self.special_attack,
                'name': 'special_attack'
            }, {
                'base_stat': self.defense,
                'name': 'defense'
            }, {
                'base_stat': self.attack,
                'name': 'attack'
            }, {
                'base_stat': self.hp,
                'name': 'hp'
            }
        ]
        dictified['primary_type'] = self.primary_type.id
        dictified['secondary_type'] = None if self.secondary_type is None else self.secondary_type.id
        dictified['average_stats'] = self.average_stats
        dictified['moves'] = [move.id for move in self.moves]

        return dictified

    def min_dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = self.name.title()
        dictified['primary_type'] = self.primary_type.id
        dictified['secondary_type'] = None if self.secondary_type is None else self.secondary_type.id
        dictified['average_stats'] = self.average_stats

        return dictified


class Move(Base):
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    accuracy = Column(Integer)
    pp = Column(Integer)
    priority = Column(Integer)
    power = Column(Integer)
    damage_class = Column(String(80), nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'))
    type = relationship('Type', back_populates='move_type')

    pokemon = relationship('Pokemon', secondary=pokemon_move, back_populates='moves')

    def __init__(self, id, name, accuracy, pp, priority, power, damage_class):
        self.id = id,
        self.name = name,
        self.accuracy = accuracy,
        self.pp = pp,
        self.priority = priority,
        self.power = power,
        self.damage_class = damage_class

    def dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['accuracy'] = self.accuracy
        dictified['pp'] = self.pp
        dictified['priority'] = self.priority
        dictified['power'] = self.power
        dictified['damage_class'] = self.damage_class
        dictified['move_type'] = self.type_id
        dictified['pokemon'] = [pk.id for pk in self.pokemon]

        return dictified

    def min_dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['accuracy'] = self.accuracy
        dictified['pp'] = self.pp
        dictified['power'] = self.power
        dictified['move_type'] = self.type_id

        return dictified


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    generation = Column(Integer)

    move_type = relationship("Move", back_populates="type")

    double_damage_to = relationship('Type',
                                    secondary=double_damage_to,
                                    primaryjoin=id == double_damage_to.c.origin,
                                    secondaryjoin=id == double_damage_to.c.opposing,
                                    backref='double_damage_to_backref')

    double_damage_from = relationship('Type',
                                      secondary=double_damage_from,
                                      primaryjoin=id == double_damage_from.c.origin,
                                      secondaryjoin=id == double_damage_from.c.opposing,
                                      backref='double_damage_from_backref')

    half_damage_to = relationship('Type',
                                  secondary=half_damage_to,
                                  primaryjoin=id == half_damage_to.c.origin,
                                  secondaryjoin=id == half_damage_to.c.opposing,
                                  backref='half_damage_to_backref')

    half_damage_from = relationship('Type',
                                    secondary=half_damage_from,
                                    primaryjoin=id == half_damage_from.c.origin,
                                    secondaryjoin=id == half_damage_from.c.opposing,
                                    backref='half_damage_from_backref')

    no_damage_to = relationship('Type',
                                secondary=no_damage_to,
                                primaryjoin=id == no_damage_to.c.origin,
                                secondaryjoin=id == no_damage_to.c.opposing,
                                backref='no_damage_to_backref')

    no_damage_from = relationship('Type',
                                  secondary=no_damage_from,
                                  primaryjoin=id == no_damage_from.c.origin,
                                  secondaryjoin=id == no_damage_from.c.opposing,
                                  backref='no_damage_from_backref')

    def __init__(self, id, name, generation):
        self.id = id,
        self.name = name,
        self.generation = generation

    def dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['generation'] = self.generation

        tables = [self.double_damage_to, self.double_damage_from, self.half_damage_to, self.half_damage_from,
                  self.no_damage_to, self.no_damage_from]
        table_names = ['double_damage_to', 'double_damage_from', 'half_damage_to', 'half_damage_from', 'no_damage_to',
                       'no_damage_from']

        for table, name in zip(tables, table_names):
            dictified[name] = [t.id for t in table]

        dictified['moves'] = [move.id for move in self.move_type]
        dictified['num_primary_type'] = len(self.pokemon_primary_type)
        dictified['num_secondary_type'] = len(self.pokemon_secondary_type)

        return dictified

    def min_dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['generation'] = self.generation

        dictified['num_primary'] = len(self.pokemon_primary_type)
        dictified['num_secondary'] = len(self.pokemon_secondary_type)
        dictified['num_moves'] = len(self.move_type)

        return dictified
