# How to analyze data

Usually, all data analysis is done in the
[Corryvreckan test beam data reconstruction framework](https://gitlab.cern.ch/corryvreckan/corryvreckan)

We are going to use an installation specifically tweaked to analyze data
taken with the ALPIDE sensors. It is provided by the ALICE ITS3 WP3 and can
be found on their
[gitlab page](https://gitlab.cern.ch/alice-its3-wp3/its-corryvreckan-tools)

## Installation

Clone the ITS-Corryvreckan-Tools repository
```Shell Session
git clone https://gitlab.cern.ch/alice-its3-wp3/its-corryvreckan-tools.git
```

The version of Corryvreckan contained in this repository is run in a Docker
container. For this, you need to make sure to have docker installed on your
system.

On some systems this might be as easy as running

```Shell Session
sudo apt-get install docker
```

However, if this doesn't work, you might need to install it manually.
Fortunately, the docker website provides version for basically all
linux distributions: https://download.docker.com/linux/

So, for example, if you're running on Debian 10 (buster) x86_64, 
you will find the docker package for your system at
`linux/debian/dists/buster/pool/stable/amd64/`. There, install the latest
version of `docker-ce` and `docker-ce-cli`.

Afterwards, take a look at the repository.

Other helpful resources are
- [The Corryvreckan project website](https://project-corryvreckan.web.cern.ch/project-corryvreckan/)
- [The Corryvreckan user manual](https://project-corryvreckan.web.cern.ch/project-corryvreckan/usermanual/corryvreckan-manual-v2.0.1.pdf)
