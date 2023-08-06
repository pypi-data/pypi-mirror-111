'''
MIT License

Copyright (c) 2021 Qualichat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pathlib
from typing import Union, List, Any, DefaultDict
from collections import defaultdict

import tkinter
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from .chat import Chat
from .utils import parse_domain


__all__ = ('Qualichat', 'load_chats')


class Qualichat:
    """Represents a set of chats for linguistic analysis.
    
    Attributes
    ----------
    chats: List[:class:`.Chat`]
        All chats uploaded and parsed by Qualichat.
    """

    __slots__ = ('chats',)

    def __init__(self, chats: List[Chat]) -> None:
        self.chats = chats

    def news(self) -> None:
        chat = self.chats[0]
        data: DefaultDict[str, int] = defaultdict(int)

        for message in chat.messages:
            for url in message['Qty_char_links']: # type: ignore
                # Avoid PyLance complainings.
                url: str = url
                data[parse_domain(url)] += 1

        labels = list(data.keys())
        sizes = list(data.values())

        _, ax = plt.subplots()

        ax.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
        print('plot.show()')
        plt.show()


def load_chats( # type: ignore
    *paths: Union[str, pathlib.Path],
    **kwargs: Any
) -> Qualichat:
    """Loads the given chats from a plain text files.

    Parameters
    ----------
    *paths: Union[:class:`str`, :class:`pathlib.Path`]
        The paths to the chat files.
        The files must be in plain text format.
    **kwargs: Any
        Keyword arguments that will be passed to :class:`.Chat`.

    Returns
    -------
    :class:`.Qualichat`
        The object that will be used for analysis of the chat.

    Raises
    ------
    :class:`FileNotFoundError`
        If one of the chat files could not been found.
    """
    return Qualichat([Chat(path, **kwargs) for path in paths])
