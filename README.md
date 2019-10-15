# flarestack
[![Documentation Status](https://readthedocs.org/projects/flarestack/badge/?version=latest)](https://flarestack.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/IceCubeOpenSource/flarestack.svg?branch=master)](https://travis-ci.org/IceCubeOpenSource/flarestack) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IceCubeOpenSource/flarestack/master)

Code for unbinned likelihood analysis of astroparticle physics data, created by [@robertdstein](https://github.com/robertdstein).

Both time-dependent and time-independent analyses can be performed, as well as a "flare-search" algorithm to find event clustering in time as well as space.

Performs single point source analyses, as well as the stacking of sources according to predefined weighting. 
Also performs stacking analyses where the signal strength of each source is fit individually.

# Getting started

The easiest way to start using Flarestack is to play with the introductory ipython notebooks, which can be opened with the following link:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IceCubeOpenSource/flarestack/master)

The notebooks themselves are found under *examples/ipython_notebooks/*.

The "Binder" provides a pre-built Docker image containing all necessary dependencies, so you can simply click and play. It avoids the need for local installation, and should provide understanding of how the code works. 

# Installation instructions

## How do I actually install Flarestack?

The answer to this question depends on how lazy you're feeling, and how much of the backend you want to deal with.

### OPTION A: I only want to do an analysis, and trust the under-the-hood code

In that case:
```bash
pip install flarestack
```
 
The entire package can simply be pip installed, and this will automatically install all dependencies.

 ### OPTION B: Actually, I want to see the backend code myself. Maybe I want to contribute to it!
 
 Now you will need a couple of extra code lines:

```bash
git clone git@github.com:IceCubeOpenSource/flarestack.git
export PYTHONPATH=/path/to/flarestack
```
 
This will give you the very latest copy of the code, update the installed version if you git pull or modify scripts yourself, and still enable you to import flarestack.

### What actually are the dependencies, by the way?

Flarestack uses python 3.7, and requires the following packages:

* numpy
* scipy
* astropy
* healpy=1.10.1
* matplotlib
* numexpr

All required dependencies can be found using the IceCube py3-v4 environment. They can collectively be installed with ```pip install -r requirements.txt```, if you don't want to install flarestack via pip.
 
### Right, anyway, I've now downloaded Flarestack. Can I use it right away?
 
You can get started with flarestack immediatly using public IceCube datasets provided as part of the code. You can simply run scripts such as those under /flarestack/analyses/, and do your science!

You can optionally set custom directorioes for datasets, and for storing data calculated with the code.

### Setting up the dataset directory

If you are running on WIPAC or DESY, you do not need to specify a dataset directory, as IceCube data will be found automatically. Otherwise, you can add:

```bash
export FLARESTACK_DATASET_DIR=/path/to/datasets
```

to point the code to local copies of Icecube datasets.

### Setting up directory for storing data

Flarestack will produce many files that do not need to be version-controlled. The principle is that everything within this directory can be reproduced by the code, so does not need to be backed up. By default, these files will be saved in a separate within the user home directory, but it might be preferrable to save them elsewhere, such as a scratch directory. You can specify the parent directory:

```bash
export FLARESTACK_SCRATCH_DIR=/path/to/scratch
```

A folder `flarestack__data` will be created in that directory. This is where you will find plots, pickle files and other files produced by the code.

# Testing Flarestack

Is flarestack actually working? If you've already run the precomputation, you can check the functionality of flarestack with *unit tests*. There are a suite of unit tests to cover flarestack functionality, which can be run from the base flarestack directory with:

 ```bash
 python -m unittest discover tests/
```

If you want to contribute to flarestack, please remember to add new tests!

Flarestack runs with Travic CI, a Continuous Integration Service. After each commit, the suite of tests is run, to ensure that the commit did not break anything. You can see the results of these tests at:

[![Build Status](https://travis-ci.org/IceCubeOpenSource/flarestack.svg?branch=master)](https://travis-ci.org/IceCubeOpenSource/flarestack)
