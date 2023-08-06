# gsbatch

[![CI](https://github.com/tdegeus/gsbatch/workflows/CI/badge.svg)](https://github.com/tdegeus/gsbatch/actions)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/gsbatch.svg)](https://anaconda.org/conda-forge/gsbatch)
[![PyPi release](https://img.shields.io/pypi/v/gsbatch.svg)](https://pypi.org/project/gsbatch/)

# Overview

*gsbatch* allows you to run batch jobs (with some default options) using *GhostScript*.

## Convert images to PNG

```bash
gsbatch_topng *.pdf
``` 

Convert a bunch of `*.pdf` images to PNG images. 
`gsbatch_topng` uses as default output the same filename, but with the `.pdf` extension replaced
by `.png`.

# Getting gsbatch

## Using conda

```bash
conda install -c conda-forge gsbatch
```

This will also download and install all necessary dependencies.

## Using PyPi

```bash
pip install gsbatch
```

This will also download and install the necessary Python modules.

## From source

```bash
# Download gsbatch
git checkout https://github.com/tdegeus/gsbatch.git
cd gsbatch

# Install
python -m pip install .
```

This will also download and install the necessary Python modules.
