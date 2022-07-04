from pony.orm import *
import datetime

db = Database()
db.bind(provider='sqlite', filename='discussion.db', create_db=True)


class Timer(db.Entity):
    id = PrimaryKey(int, auto=True)
    hours = Required(int)
    minutes = Required(int)
    seconds = Required(int)
    user = Optional('User')


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    id_tg = Required(str)
    name = Required(str)
    surname = Optional(str)
    timer = Required(Timer, reverse='user')
    token=Required(int)
    discussion = Optional('Discussion')
    owner_of = Optional('Discussion')


class Discussion(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    topic = Required(str)
    max_user = Required(int)
    user_now = Required(int)
    time = Required(datetime.datetime)
    users_to_add = Set(User)
    owner = Required(User, reverse='owner_of')
    
    @db_session
    def get_all_users(self):
        return User.select(lambda u: u.discussion == self)[:]


db.generate_mapping(create_tables=True)


