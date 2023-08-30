import numpy as np
import zipfile as zf
import re
import os
import sys


class Decoder(object):
    def __init__(self, names: list[str] | type[str] | str = None, directory: str = '.') -> None:
        self.__directory__ = self.setdir(directory)
        if names:
            self.__names__ = self.setnames(names)
        else:
            self.__names__ = None

    def setdir(self, directory: list[str] | type[str] | str = '.') -> str:
        self.__directory__ = directory + '/' * \
            (bool(directory) and directory[-1] != '/')
        return self.__directory__

    def setnames(self, names: list[str] | type[str] | str) -> list:
        if isinstance(names, str):
            ret = list(map(
                lambda x: f'{self.__directory__}{"/"*(bool(self.__directory__) if self.__directory__ and self.__directory__[-1] != "/" else 0)}{x}', re.split(r', | |;|\\|\/|\,', names)))
        elif isinstance(names, (list, tuple)):
            ret = list(map(
                lambda x: f'{self.__directory__}{"/"*(bool(self.__directory__) if self.__directory__ and self.__directory__[-1] != "/" else 0)}{x}', names))
        else:
            raise ValueError('Names can only be list, tuple or string')
        return ret

    def fromdir(self, dir: str = None) -> np.ndarray:
        if dir is None:
            dir = self.__directory__
        result = []
        names = self.setnames(os.listdir(dir))
        for name in names:
            with open(name, 'rb') as file:
                data = file.readlines()
                result.append(np.fromiter(map(bytes.decode, data), float))
        return np.array(result)

    def fromzip(self, pwd=None, dir=None, names=None) -> np.ndarray:
        if dir is None:
            dir = self.__directory__
        if names is None:
            names = self.__names__
        else:
            names = self.setnames(names)
        result = []
        for name in names:
            if name.split('/')[-1] in os.listdir(dir) and zf.is_zipfile(name):
                with zf.ZipFile(name) as zip:
                    for file in zip.infolist():
                        if not file.is_dir():
                            with zip.open(file, pwd=pwd) as vector:
                                result.append(np.fromiter(vector, float))

        return np.array(result)
