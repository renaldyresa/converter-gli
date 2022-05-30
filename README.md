# Dokumentasi Penggunaan Library ConverterDataGLI


## Installation

```sh
pip install git+https://github.com/renaldyresa/logging-gli@main
```


## ConverterResultIterator


#### Example 1

Contoh Data:

|name|age|date_of_birth|
|----|---|-------------|
|user1|22|2000-01-01|
|user2|22|2000-01-02|

Data Python:
```python
data = [
    ["user1", 22, "2000-01-01"],
    ["user2", 22, "2000-01-02"]
]
```


Contoh konfiguration:

```python
import ConverterDataGLI as cdg

config = [
    cdg.ConfigColumn(nameColumn="name", typeColumn=str),
    cdg.ConfigColumn(nameColumn="age", typeColumn=int),
    cdg.ConfigColumn(nameColumn="date_of_birth", typeColumn=str),
]
```

Cara penggunaan:

```sh
for row in cdg.ConverterResultIterator(data, config):
    print(row.name, row.age, row.date_of_birth)
```