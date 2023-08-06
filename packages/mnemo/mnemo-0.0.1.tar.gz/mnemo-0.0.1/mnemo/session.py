"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

import bottle  # type: ignore
import copy
from passlib.hash import pbkdf2_sha256  # type: ignore
import time
from tinydb import Query, TinyDB, where
from typing import Any, Dict


class Session(object):
    __db: TinyDB
    __q: Query

    def __init__(self, db: TinyDB):
        super(Session, self).__init__()
        self.__db = db
        self.__q = Query()

    @property
    def is_logged(self) -> bool:
        """Checks if a user is currently logged.
        Only one user can be logged at the same time.
        """
        query_result = self.__db.table("Users").search(self.__q.cookie_key != None)
        if 0 == len(query_result):
            return False
        else:
            return (
                bottle.request.get_cookie("mnemo-email"),
                bottle.request.get_cookie("mnemo-key"),
            ) == (
                query_result[0]["email"],
                query_result[0]["cookie_key"],
            )

    @property
    def has_users(self) -> bool:
        return 0 != len(self.__db.table("Users"))

    def create_first_user(self, request) -> str:
        assert not self.has_users
        try:
            self.__db.table("Users").insert(
                {
                    "email": request.forms.get("user_email"),
                    "password": pbkdf2_sha256.hash(request.forms.get("user_password")),
                    "cookie_key": None,
                    "last_touch": time.time(),
                }
            )
            return '{"response":"success", "success":true}'
        except Exception:
            return '{"response":"failed", "success":false}'

    def login(self, request) -> str:
        """Logs user based on user_email and user_password fields in request."""
        self.logout()
        try:
            email = request.forms.get("user_email")
            search_results = self.__db.table("Users").search(self.__q.email == email)

            if 0 == len(search_results):
                return '{"response":"not-found", "success":false}'

            if pbkdf2_sha256.verify(
                request.forms.get("user_password"), search_results[0]["password"]
            ):
                cookie_key = pbkdf2_sha256.hash(str(time.time()))
                print(cookie_key)
                self.__db.table("Users").update(
                    {"cookie_key": cookie_key, "last_touch": time.time()},
                    where("email") == email,
                )
                bottle.response.set_cookie(
                    "mnemo-email",
                    email,
                    max_age=60 * 30,
                    httponly=True,
                )
                bottle.response.set_cookie(
                    "mnemo-key",
                    cookie_key,
                    max_age=60 * 30,
                    httponly=True,
                )
                return '{"response":"logged", "success":true}'
            else:
                return '{"response":"wrong-pwd", "success":false}'
        except Exception as e:
            print(e)
            return '{"response":"failed", "success":false}'

    def logout(self) -> str:
        """Logs user out. Does not delete the session cookie."""
        try:
            self.__db.table("Users").update(
                {"cookie_key": None, "last_touch": time.time()},
                where("cookie_key") != None,
            )
            return '{"response":"logged-out", "success":true}'
        except Exception as e:
            print(e)
            return '{"response":"failed", "success":false}'

    def get_user_data(self) -> Dict[str, str]:
        search_results = self.__db.table("Users").search(self.__q.cookie_key != None)
        if 0 == len(search_results):
            return {}
        user_data = copy.copy(search_results[0])
        user_data["password"] = None
        user_data["cookie_key"] = None
        return user_data
