from typing import List, Any, Callable
from collections import namedtuple


class ConfigColumn:
    """Data konfigurasi column"""

    def __init__(self, nameColumn, typeColumn, aliasColumn=None, dataColumn=None, funcConvert: Callable = None,
                 paramArgs: List = None):
        """

        :param nameColumn: nama column yang akan digunakan untuk mengakses data
        :param typeColumn: type variable column
        :param dataColumn: jika typeColumn "list", maka value dari dataColumn harus ada.
        :type dataColumn: list[ConfigColumn]
        :param funcConvert: fungsi untuk manipulasi value data.
        :type funcConvert: Callable
        :param paramArgs: parameter yang akan di gunakan pada funcConvert
        """
        self.__nameColumn = nameColumn
        self.__aliasColumn = aliasColumn
        self.__typeColumn = typeColumn
        self.__dataColumn: List[ConfigColumn] = [] if dataColumn is None else dataColumn
        self.__funcConvert = funcConvert
        self.__paramArgs = [] if paramArgs is None else paramArgs

    @property
    def nameColumn(self):
        return self.__nameColumn

    @property
    def typeColumn(self):
        return self.__typeColumn

    @property
    def aliasColumn(self):
        return self.__aliasColumn

    @property
    def dataColumn(self):
        return self.__dataColumn

    @property
    def funcConvert(self):
        return self.__funcConvert

    @property
    def paramArgs(self):
        return self.__paramArgs


class ConverterResultIterator:
    """
    class iterator untuk convert format data sesuai dengan config

    """

    def __init__(self, dataIterator, config: List[ConfigColumn]):
        """
        Example 1:
            dataIterator = [
                ["name1", 18, "email1@gmail.com],

                ["name2", 20, "email2@gmail.com],
            ]

            config = [
                ConfigColumn(nameColumn="name", typeColumn=str),

                ConfigColumn(nameColumn="age", typeColumn=int),

                ConfigColumn(nameColumn="email", typeColumn=str),
            ]


        :param dataIterator: data yang dapat di iterasi
        :param config: konfigurasi dari data
        """
        self.__dataIterator = dataIterator
        self.__config = config

    def __iter__(self):
        """
        method yang akan convert data menjadi sesuai dengan config
        """
        for row in self.__dataIterator:
            tRow = row
            if type(row) is dict:
                tRow = namedtuple("TRow", row.keys())(*row.values())
            elif type(row) is list:
                tDict = {}
                i = 0
                for bqc in self.__config:
                    val = None
                    if len(row) > i:
                        val = row[i]
                    tDict[bqc.nameColumn] = val
                    i += 1
                tRow = namedtuple("TRow", tDict.keys())(*tDict.values())
            temp = type("BigQueryResult", (object,), {})()
            for bqColumn in self.__config:
                tName = bqColumn.nameColumn if bqColumn.aliasColumn is None else bqColumn.aliasColumn
                if bqColumn.typeColumn is list:
                    value = ConverterResultIterator(getattr(tRow, tName), bqColumn.dataColumn)
                else:
                    if bqColumn.funcConvert is not None:
                        tArgs = []
                        for nameArgs in bqColumn.paramArgs:
                            if nameArgs[0] == "%":
                                tArgs.append(getattr(tRow, nameArgs[1:]))
                            else:
                                tArgs.append(nameArgs)
                        tValue = bqColumn.funcConvert(*tArgs)
                    else:
                        tValue = getattr(tRow, tName)
                    value = tValue
                    if bqColumn.typeColumn is not Any:
                        value = bqColumn.typeColumn(tValue)
                setattr(temp, bqColumn.nameColumn, value)
            yield temp
