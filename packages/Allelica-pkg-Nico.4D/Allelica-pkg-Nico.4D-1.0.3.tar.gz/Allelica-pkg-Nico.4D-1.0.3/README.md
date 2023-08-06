# allelica-lib Documentation.

The Source Code of The Library. [Source-Code](https://github.com/4DIngenieria/allelica-lib).

For The Example Using The Class. [Source-Code](https://github.com/4DIngenieria/Allelica).

```diff
For The Installation of This Library: "pip install Allelica-pkg-Nico.4D"
```

```python

#Example Without Dask

from allelica_lib import parse

parse.process("source.xlsx", "out.tsv")

```

```python

#Example Using The Library Dask

from allelica_lib import parse

parse.process_dask("source.xlsx", "out.tsv", 4) 

#'4' Is The Number of Partitions That The Dask Library Will Use When Running The Process. 

```

```diff
Other Requirements (Auto-Install With The Library):
```
- pip install dask 
- pip install pandas 
- pip install openpyxl