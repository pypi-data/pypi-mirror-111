# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepgrp', 'deepgrp._scripts']

package_data = \
{'': ['*'],
 'deepgrp': ['_mss/mss.c',
             '_mss/mss.c',
             '_mss/mss.c',
             '_mss/mss.h',
             '_mss/mss.h',
             '_mss/mss.h',
             '_mss/pymss.pyx',
             '_mss/pymss.pyx',
             '_mss/pymss.pyx']}

install_requires = \
['hyperopt>=0.2.3,<0.3.0',
 'numpy<1.20.0',
 'pandas>=1.0.1,<2.0.0',
 'tensorflow>=2.1.0,<2.6.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['deepgrp = deepgrp.__main__:main',
                     'parse_rm = deepgrp._scripts.parse_rm:main',
                     'preprocess_sequence = '
                     'deepgrp._scripts.preprocess_sequence:main']}

setup_kwargs = {
    'name': 'deepgrp',
    'version': '0.2.3',
    'description': 'DNA repeat annotations',
    'long_description': "==================================================================\nDeepGRP - Deep learning for Genomic Repetitive element Prediction\n==================================================================\n\n|PyPI version fury.io|\n\n.. |PyPI version fury.io| image:: https://badge.fury.io/py/deepgrp.svg\n   :target: https://pypi.org/project/deepgrp/\n\nDeepGRP is a python package used to predict genomic repetitive elements\nwith a deep learning model consisting of bidirectional gated recurrent units\nwith attention.\nThe idea of DeepGRP was initially based on `dna-nn`__, but was re-implemented\nand extended using `TensorFlow`__ 2.1.\nDeepGRP was tested for the prediction of HSAT2,3, alphoid, Alu\nand LINE-1 elements.\n\n.. __: https://github.com/lh3/dna-nn\n.. __: https://www.tensorflow.org\n\nGetting Started\n===============\n\nInstallation\n------------\n\nFor installation you can use the PyPI version with::\n\n    pip install deepgrp\n\nor install from this repository with::\n\n    git clone https://github.com/fhausmann/deepgrp\n    cd deepgrp\n    pip install .\n\nAdditionally you can install the developmental version with `poetry`__::\n\n    git clone https://github.com/fhausmann/deepgrp\n    cd deepgrp\n    poetry install\n\n.. __: https://python-poetry.org/\n\nData preprocessing\n------------------\nFor training and hyperparameter optimization the data have to be preprocessed.\nFor inference / prediction the FASTA sequences can directly be used and you\ncan skip this process.\nThe provided script `parse_rm` can be used to extract repeat annotations from\n`RepeatMasker`__ annotations to a TAB seperated format by::\n\n    parse_rm GENOME.fa.out > GENOME.bed\n\n.. __: http://www.repeatmasker.org/\n\nThe FASTA sequences have to be converted to a one-hot-encoded representation,\nwhich can be done with::\n\n    preprocess_sequence FASTAFILE.fa.gz\n\n`preprocess_sequence` creates a one-hot-encoded representation in numpy\ncompressed format in the same directory.\n\n\nHyperparameter optimization\n---------------------------\nFor Hyperparameter optimization the github repository provides\na jupyter `notebook`__ which can be used.\n\n.. __: https://github.com/fhausmann/deepgrp/blob/master/notebooks/DeepGRP.ipynb\n\nHyperparameter optimization is based on the `hyperopt`__ package.\n\n.. __: https://github.com/hyperopt/hyperopt\n\nTraining\n--------\n\nTraining of a model can be performed with::\n\n    deepgrp train <parameter.toml> <TRAIN>.fa.gz.npz <VALIDATION>.fa.gz.npz <annotations.bed>\n\nThe prefix of `<TRAIN>` and `<VALIDATION>` should be as row identifier in the first column of `<annotations.bed>`.\n\nFor more fine-grained control of the training process you can also use the provided jupyter `notebook`__.\n\n.. __: https://github.com/fhausmann/deepgrp/blob/master/notebooks/Training.ipynb\n\nPrediction\n----------\nThe prediction can be done with the deepgrp main function like::\n\n    deepgrp <modelfile> <fastafile> [<fastafile>, ...]\n\nwhere `<modelfile>` contains the trained model in `HDF5`__\nformat and `<fastafile>` is a (multi-)FASTA file containing DNA sequences.\nSeveral FASTA files can be given at once.\n\n.. __: https://www.tensorflow.org/tutorials/keras/save_and_load\n\nRequirements\n============\nRequirements are listed in `pyproject.toml`__.\n\n.. __: https://github.com/fhausmann/deepgrp/blob/master/pyproject.toml\n\nAdditionally for compiling C/Cython code, a C compiler should be installed.\n\nContribution:\n=============\nFirst of all any contributing are very welcome.\nIf you want to contribute, please make a Pull request with your changes.\nYour code should be formatted using `yapf`__ using the default settings,\nthey and they should pass all tests without issues.\nFor testing currently `mypy`__ and `pylint`__ static tests are used, while\n`pytest`__ is used for functional tests.\n\n.. __: https://github.com/google/yapf\n.. __: https://mypy.readthedocs.io/en/latest/\n.. __: https://pylint.pycqa.org/en/latest/\n.. __: https://docs.pytest.org/en/6.2.x/\n\n\nIf you're adding new functionalities please provide corresponding tests\nin the `tests`__ directory.\n\n.. __: ./tests/\n\nFeel free to ask in case of any questions.\n\nFurther information\n===================\nYou can find material to reproduce\nthe results in the repository `deepgrp_reproducibility`__.\n\n.. __: https://github.com/fhausmann/deepgrp_reproducibility\n",
    'author': 'Fabian Hausmann',
    'author_email': 'fabian.hausmann@zmnh.uni-hamburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fhausmann/deepgrp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.9.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
