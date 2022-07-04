from pony.orm import *
from discussionbot.databasemanagement.Database import User, Discussion, Timer
from threading import Thread
from time import sleep
from discussionbot.databasemanagement import LOGS

import logging
import schedule
import datetime


@db_session
def add_user(id_tg : str, name : str, surname : str, token : int) -> None:
    if get_user(id_tg) is None:
        if surname is not None:
            User(id_tg=id_tg, name=name, surname=surname, timer=Timer(minutes=0, seconds=0, hours=0), token=token)
        else:
            User(id_tg=id_tg, name=name, timer=Timer(minutes=0, seconds=0, hours=0), token=token)

    update_nickname(id_tg, name, surname)


@db_session
def get_user(id_tg : str) -> User:
    return User.get(id_tg=id_tg)


@db_session
def add_discussion(name : str, topic : str, max_user : int, id_tg : str) -> None:
    owner = get_user(id_tg)
    Discussion(name=name, topic=topic, max_user=max_user, user_now=1, users_to_add=[owner, ], owner=owner,
               time=datetime.datetime.now())

@db_session
def get_discussion(discussion_id : int) -> Discussion:
    return Discussion[discussion_id]

@db_session
def get_user_owner_of(user_id : int) -> Discussion:
    return get_user(user_id).owner_of

@db_session
def add_user_to_discussion(id_tg : str, discussion_id : int) -> bool:
    try:
        user = get_user(id_tg)
        discussion = get_discussion(discussion_id)
    except ObjectNotFound:
        return False


    if not user.discussion == discussion:
        user.discussion = discussion
        discussion.user_now += 1
        return True
    return False

@db_session
def get_attribute_user(user : str, attribute : str):
    try:
        return getattr(get_user(user), attribute)
    except Exception as e:
        print(e)

@db_session
def disband_discussion(discussion : int):
    try:
        get_discussion(discussion).delete()
    except Exception as e:
        print(e)

@db_session
def get_attribute_discussion(discussion : int, attribute : str):
    try:
        return getattr(get_discussion(discussion), attribute)
    except Exception as e:
        print(e)

@db_session
def leave_user_from_discussion(id_tg : str) -> None:

    user = get_user(id_tg)
    user.discussion.user_now -= 1

    user.discussion = None

    delete_manager()

@db_session
def delete_manager() -> None:
    Discussion.select(lambda d : d.user_now == 0).delete()


@db_session
def adding_token_to_user(id_tg : str, token_to_add : int) -> None:
    user = get_user(id_tg)
    user.token += token_to_add

@db_session
def update_nickname(id_tg : str, name : str, surname : str) -> None:

    user = get_user(id_tg)

    if user.name != name:
        user.name = name

    if user.surname != surname:
        if surname is not None:
            user.surname = surname
        else:
            user.surname = ""

@db_session
def get_token(id_tg : str) -> str:
    return str(get_user(id_tg).token)

@db_session
def get_all_discussion() -> list:

    return Discussion.select()[:]

@db_session
def adding_on_timer():
    # Adda il tempo solo se è in una discussione
    for user in User.select()[:]:
        if user.discussion is not None:
            user.timer.seconds += 1

        if user.timer.seconds == 60:
            user.timer.seconds = 0
            user.timer.minutes += 1

        if user.timer.minutes == 60:
            user.timer.minutes = 0
            user.timer.hours += 1

        if user.timer.hours % 2 == 0 and user.timer.hours != 0:
            if user.timer.minutes == 0 and user.timer.seconds == 0:
                adding_token_to_user(user.id_tg, 30)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


schedule.every(1).seconds.do(adding_on_timer)
Thread(target=schedule_checker).start()
