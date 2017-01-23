# bblr-hopfield-boltzmann
The goal of this project is to compare the Hopfield Neural Network model and the Restricted Boltzmann Machine model when they are used as associative memories that can store pattern data sets.

The details about this project are published in our [wiki](https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki).

## Reproducibility

The default configured random seed produces the same exact results as the ones published in this paper.

### Requirements

* Python >= 2.7.0
* NumPy >= 1.12.0
* UNIX-like system shell.

### Execution

Just execute the following command in the root of the project to generate data sets and test the models:

    $ sh generate results.sh
    
This will create several JSON files in `out/results/`. When it finishes, execute the following command:

    $ sh generate latex.sh > out/tables.tex

This will create a TeX file in `out/tables.tex` containing the result tables used in this paper.
