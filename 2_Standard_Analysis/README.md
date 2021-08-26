# How to analyze data

Usually, all data analysis is done in the
[Corryvreckan test beam data reconstruction framework](https://gitlab.cern.ch/corryvreckan/corryvreckan)

We are going to use an installation specifically tweaked to analyze data
taken with the ALPIDE sensors. It is provided by the ALICE ITS3 WP3 and can
be found on their
[gitlab page](https://gitlab.cern.ch/alice-its3-wp3/its-corryvreckan-tools)

## Prerequisites

It is reqired to have an installation of the ROOT analysis
framework installed on your system. For further information please go to
the [root installation page](https://root.cern/install/).

To compile root you might be required to install cmake aswell.
This is best done through
[their official website](https://cmake.org/install/).

The version of Corryvreckan contained in this repository is run in a Docker
container. For this, you need to make sure to have docker installed on your
system. On some systems this might be as easy as running

```Shell Session
$ sudo apt-get install docker
```

However, if this doesn't work, you might need to install it manually.
Fortunately, the docker website provides version for basically all
linux distributions: https://download.docker.com/linux/

So, for example, if you're running on Debian 10 (buster) x86_64, 
you will find the docker package for your system at
`linux/debian/dists/buster/pool/stable/amd64/`. There, install the latest
version of `docker-ce` and `docker-ce-cli`.

## Installation

Clone the ITS-Corryvreckan-Tools repository
```Shell Session
$ git clone https://gitlab.cern.ch/alice-its3-wp3/its-corryvreckan-tools.git
```

The version of Corryvreckan contained in this repository is run in a Docker
container. Take a look at the repository. There are several scripts
to obtain a version of the container. The easiest way to get it is to
pull the latest version. For this, execute

```Shell Session
$ ./pull_container.sh
```

To analyze data, you need to define the geometry of the setup in a .conf
file. For the ALPIDE telescope, the conf file will be attached to this
repository (`3REF-DUT-3REF.conf`).

Move this file into the `geometry` folder of your ITS-Corryvreckan-Tools
installation.

## Analysis

The next step is to set up a config file in order to tell Corryvreckan what
to do. There are templates for different steps of analyses already
inside of the `configs/` directory. The standard analysis chain
for testbeam data is as follows:
`creatmask` -> `prealign` -> `align` -> `analyse`

Make yourself familiar with the modules loaded in these config files.
For a list of all modules consult
[the Corryvreckan user manual](https://project-corryvreckan.web.cern.ch/project-corryvreckan/usermanual/corryvreckan-manual-v2.0.1.pdf)

## Example with testbeam data

The file ´run000380.raw´ contains data previously taken with the telescope at a testbeam in 2019. We will go through all four analysis stages:

### Masking

- Open the ´createmask.conf´.
- First load the Corryvreckan module ´[Corryvreckan]´. You can specify the level of detail of your console output with ´log_level´ and ´log_format´.
- Specify the geometry file by setting the ´detectors_file´ variable.
- The variable ´detectors_file_updated´ can be specified if there are alignment calculations which change the detector layout. It will be saved to
the specified geometry file. The variable ´histogram_file´ can be used to store the analysis into a ROOT object.
- Then, load the ´[Metronome]´ module, to slice the data stream into regular time frames with a defined length. And set the ´triggers´ variable to ´1´.
- Next, load the ´[EventLoaderEUDAQ2]´ module to read the raw data into Corryvreckan. The variable ´file_name´ specifies the input file.
- Finally, load the ´[MaskCreator]´ module, to create a detector mask. The variable ´frequency_cut´ specifies how frequent a pixel has to hit before
it will be masked. If it is set to 1000, the module will mask every pixel that fires 1000x more often than average.

## Further reading
Other helpful resources are
- [The Corryvreckan project website](https://project-corryvreckan.web.cern.ch/project-corryvreckan/)
- [The Corryvreckan user manual](https://project-corryvreckan.web.cern.ch/project-corryvreckan/usermanual/corryvreckan-manual-v2.0.1.pdf)
