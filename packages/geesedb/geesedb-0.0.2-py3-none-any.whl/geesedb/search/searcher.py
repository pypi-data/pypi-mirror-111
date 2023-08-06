#! /usr/bin/env python3

import argparse
from typing import Any, Callable, Union

import numpy as np
import pandas as pd

from ..connection import get_connection
from ..search import RobertsonBM25


class Searcher:

    def __init__(self, **kwargs: Any) -> None:
        self.arguments = self.get_arguments(kwargs)
        self.db_connection = get_connection(self.arguments['database'])
        self.ranking_method = None
        self.fetch = self.set_return_type()
        if self.arguments['retrieval_method'] == 'BM25_robertson':
            self.ranking_method = RobertsonBM25(self.arguments['k1'], self.arguments['b'], self.arguments['n'])

    @staticmethod
    def get_arguments(kwargs: Any) -> dict:
        arguments = {
            'database': None,
            'retrieval_method': 'BM25_robertson',
            'k1': 0.9,
            'b': 0.4,
            'n': 1000,
            'return_type': 'tuple'
        }
        for key, item in arguments.items():
            if kwargs.get(key) is not None:
                arguments[key] = kwargs.get(key)
        if arguments['database'] is None:
            raise IOError('database path needs to be provided')
        return arguments

    def set_return_type(self) -> Callable[[], Union[list, pd.DataFrame, np.array]]:
        if self.arguments['return_type'] == 'list':
            fetch = self.db_connection.cursor.fetchall
        elif self.arguments['return_type'] == 'numpy':
            fetch = self.db_connection.cursor.fetchnumpy
        else:
            fetch = self.db_connection.cursor.fetchdf
        return fetch

    def set_k1(self, k1: float):
        self.arguments['k1'] = k1

    def set_b(self, b: float):
        self.arguments['b'] = b

    def set_n(self, k1: float):
        self.arguments['n'] = k1

    def search_topic(self, topic: str) -> Union[list, pd.DataFrame, np.array]:
        query = self.ranking_method.construct_query(topic)
        self.db_connection.cursor.execute(query)
        return self.fetch()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--database',
                        required=True,
                        help='Name of the database / index')
    parser.add_argument('-r',
                        '--retrieval_method',
                        choices=['BM25_robertson'],
                        help="Use the Robertson's BM25 ranking function")
    parser.add_argument('-k1')
    parser.add_argument('-b')
    parser.add_argument('-n')
    parser.add_argument('-t',
                        '--return_type',
                        choices=['numpy', 'data_frame', 'list']
                        )
    Searcher(**vars(parser.parse_args()))
