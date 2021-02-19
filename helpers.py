from collections import deque, defaultdict
from itertools import product
import re

import enum
import os


############################################################################
#
# Reading from files.

def read_lines(file_name):
    return list(filter(None, open(file_name).read().split('\n')))

def read_paragraphs(file_name):
    return list(filter(None, open(file_name).read().split('\n\n')))

def parse_items(items, parser):
    return list(map(parser, items))


############################################################################
#
# Grids: 2D square and hex grids.

class grid:
    """
    2D grid. Supports life- algorithm by producing a new grid
    based on a is_alive function taking as parameter if the old grid
    position was alive and the number of immediate neighbours.
    """
    def __init__(self, dir_to_moves):
        self._grid = set()
        self._dir_to_moves = dir_to_moves

    @staticmethod
    def hex_grid():
        return grid(( (-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), ))

    @staticmethod
    def square_grid():
        return grid(( (1, 0), (0, -1), (-1, 0), (0, 1), ))

    def clone(self):
        other = grid(self._dir_to_moves)
        other._grid = set(self._grid)
        return other

    def add(self, pos):
        self._grid.add(pos)

    @staticmethod
    def move_pos(pos: tuple, dir: tuple):
        return (pos[0] + dir[0], pos[1] + dir[1])
    
    def count_around(self, pos: tuple):
        count = 0
        for dir in self._dir_to_moves:
            if grid.move_pos(pos, dir) in self._grid:
                count += 1
        return count

    def evolve(self, is_alive):
        new_grid = grid(self._dir_to_moves)
        for pos in self._grid:
            count = self.count_around(pos)
            if is_alive(True, count):
                new_grid.add(pos)
            for dir in self._dir_to_moves:
                new_pos = grid.move_pos(pos, dir)
                if new_pos not in self._grid:
                    count = self.count_around(new_pos)
                    if is_alive(False, count):
                        new_grid.add(new_pos)
        return new_grid


############################################################################
#
# URL stuff.

import requests
import json

_requests_session = None
def get_session() -> requests.Session:
    global _requests_session
    if not _requests_session:
        _requests_session = requests.Session()
    return _requests_session


class Method(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


_base_url = None

def set_base_url(url: str):
    global _base_url
    _base_url = url

def build_full_url(url: str) -> str:
    global _base_url
    if not _base_url:
        return url
    return _base_url + url


def get_url(
    url: str = '',
    method: Method = Method.GET,
    params: dict = None,
    in_headers: dict = None,
    in_json: dict = None) -> dict:
    """
    Call a rest API.
    The url will be combined with the global base URL, if set.
    Return a tuple of (JSON, headers, status code).
    """
    full_url = build_full_url(url)

    session = get_session()

    methods = {
        Method.GET: session.get,
        Method.POST: session.post,
        Method.PUT: session.put,
        Method.DELETE: session.delete,
    }
    meth = methods[method]
    
    with meth(full_url, params=params, headers=in_headers, json=in_json, stream=False) as response:
        try:
            received_json = response.json()
        except:
            received_json = {}
        received_content = response.content
        received_headers = response.headers
        received_code = response.status_code

    return (received_json, received_headers, received_content, received_code)

def get_url_json(url: str = '', **kwargs):
    return get_url(url, **kwargs)[0]

def get_url_headers(url: str = '', **kwargs):
    return get_url(url, **kwargs)[1]

def get_url_content(url: str = '', **kwargs):
    return get_url(url, **kwargs)[2]

def get_url_status(url: str = '', **kwargs):
    return get_url(url, **kwargs)[3]

