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
            self.__names__ = list(map(
                lambda x: f'{self.__directory__}{"/"*(bool(self.__directory__) if self.__directory__ and self.__directory__[-1] != "/" else 0)}{x}', re.split(r', | |;|\\|\/|\,', names)))
        elif isinstance(names, (list, tuple)):
            self.__names__ = list(map(
                lambda x: f'{self.__directory__}{"/"*(bool(self.__directory__) if self.__directory__ and self.__directory__[-1] != "/" else 0)}{x}', names))
        else:
            raise ValueError('Names can only be list, tuple')
        return self.__names__

    def fromdir(self, dir: str = None) -> np.ndarray:
        if dir is None:
            dir = self.__directory__
        result = []
        self.__names__ = self.setnames(os.listdir(dir))
        for name in self.__names__:
            with open(name, 'rb') as file:
                data = file.readlines()
                result.append(np.fromiter(map(bytes.decode, data), float))
        return np.array(result)
    # def fromzip(self, pwd=None) -> np.ndarray:
    #     for name in self.__names__:
    #         if name.split('/')[-1] in os.listdir(self.__directory__) and zf.is_zipfile(name):
    #             self.result.append([])
    #             with zf.ZipFile(name) as zip:
    #                 for file in zip.infolist():
    #                     if not file.is_dir():

    #     return self.result


test = Decoder('norm.zip', '../datasets/unpack norm')
print(test.fromdir())

# directory = input('Enter archives directory:\t').strip()
# archives = list(map(lambda x: f'{directory}{"/"*(bool(directory) if directory[-1] != "/" else 0)}{x}', map(lambda x: x + '.zip' if '.' not in x else x,
#                                                                                                            re.split(r' |;|\\|\/|\,', input('Enter archives name:\t')))))

# data = []
# for arc in archives:
#     with zf.ZipFile(arc, 'r') as zip:
#         for name in zip.filelist:
#             with zip.open(name.filename, mode='r') as file:
#                 vector = file.readlines()
#                 data.append(np.fromiter(map(bytes.decode, vector), float))

# # with open('022w1.eea', 'rb') as file:
# #     data = file.readlines()
# #     # print(*map(bytes.decode, data))
# #     array = np.fromiter(map(bytes.decode, data), float)

# # print(array)
# print(np.array(data))
