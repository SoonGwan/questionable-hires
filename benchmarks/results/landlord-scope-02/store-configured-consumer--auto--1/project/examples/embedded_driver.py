from backend import Backend
from store import Store

def connect():
    return Store(Backend())
