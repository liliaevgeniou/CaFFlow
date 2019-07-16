# CaFFlow

CaFFlow is a Python framework for acquisition and analysis of single-,
two-photon calcium imaging and experimental animal's behavior data.
This project is intended to be used for acquisition of video data stream(s) generated
by [Miniscope](http://miniscope.org) miniature fluorescence microscope and subsequent
(offline and/or online) analysis of the acquired data.
Practically however, it can be used for processing of wider range of frame streams,
such as animal's behavior only, batch image/video editing etc.

**This repository is currently _under_  _development_. Code contributions and bug reports are welcome.**

### Repository layout

CaFFlow consist of two main parts - framework-side and user-side scripts.
The framework-side part is a self-contained set of Python classes/functions representing
building blocks common for all recordings/experiments conducted in a Lab.
The user-side part is a set of Python scripts adapted for each experiment.
The framework is extended by developer(s), and never changed by user(s);
it has a strict set of external dependencies and guarantied backward compatibility.


- __examples__ - examples of the user-side scripts. Each script demonstrate usage of particular set of features provided by the mendouscopy framework.
- __mendouscopy__ - framework-side code related to analysis of the acquired calcium imaging and behavior data.
- __mstools__ - framework-side GUI applications for video stream(s) preview and recording of video frames generated by [Miniscope](http://miniscope.org) hardware and/or common video cameras.
- __unit_test__ - scripts for testing readiness of your Python environment to be used with the CaFFlow.


### Supported OS

- Windows (primarily).
- Any OS for which Python and all required packages available (optionally).


### Installation

__FIXME: this is short description for those who already familiar with Python/Conda.__

Download and install a command line interface based `git` client, such as
[Git for Windows](https://git-scm.com/download/win) if you do not already have it installed.

Launch the `git` client and install/activate [Git Large File Storage](https://git-lfs.github.com/) extension:

`$ git lfs install`

_MacOS:_

- _if you use Homebrew, run `$ brew install git-lfs`_
- _if you use MacPorts, run `$ port install git-lfs`_

Change directory `(cd)` to the place where you plan to keep CaFFlow and clone this repository:

`$ git clone https://github.com/DenisPolygalov/CaFFlow.git`

Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you don't have it installed already.

Launch Miniconda command line prompt. Create and activate new environment:

_MacOS: `source activate` (must activate conda first)_

`(base)> conda create -n cafflow`

`(base)> activate cafflow`

_MacOS:  `(base)> source activate cafflow` or  `(base)> conda activate cafflow`_

`(cafflow)>`

Install necessary Python packages:

`(cafflow)> conda install opencv numpy pandas scipy scikit-image`

The set of packages above is sufficient to run analysis without visualization (on a headless server for example) and GUI applications.
To add visualization capability - install Matplotlib package:

`(cafflow)> conda install matplotlib`

For GUI-based applications - install PyQt package:

`(cafflow)> conda install pyqt`

For video encoding support the lossless video codec (FFV1)
must be installed and registered globally, at your OS level
(i.e. as a COM DLL in the case of Windows).
There are multiple ways of doing this. __FIXME: extend this__

Test your Python environment:

`(cafflow)> cd CaFFlow`

`(cafflow)> python -m unittest discover unit_test`

Read Python scripts located in the __examples__ directory, execute them and adjust for your purpose.
Note that all example scripts are intended to be executed from __*inside*__ of the __examples__ directory.
