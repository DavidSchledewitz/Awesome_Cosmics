# Awesome Cosmics
Hey, this is a github repository for all of you fellow hardware fans which wanna have some fun on the dark side!

This repository contains all the information needed to work with the
ALPIDE telescope, from Data acquisition, through conversion into different
formats, and finally analysis.

## Prerequisites

To understand how to work with this detector, a fundamental knowledge of
**solid-state physics** and specifically **semiconductors** is required. Please
refer to the literature recommendations before continuing.

What is also required is some basic knowledge of how to work with a **linux
system**. You should be able to move/rename and edit text files, as well
as install packages on your linux distribution of choice. There is no
recommendation here, as nearly all linux distributions will work fine.

Furthermore, you should have some experience in working with [Python](https://www.python.org/).

## First Steps

Clone this repository onto your system by executing
```shell
git clone https://github.com/DavidSchledewitz/Awesome_Cosmics.git
```
in your terminal emulator. If you do not have git installed, check out the 
installation tutorial
[here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

After you've successfully finished this step, you should have a copy of all
of the files contained in this repository on your local machine, and are ready
to work with them.

## Contents

### Data Acquisition

[This section](1_DataAcquisition) concerns all the steps required in the process
of operating the ALPIDE telescope

### Standard Analysis

Usually, data analysis with the ALPIDE telescope is done in the
[Corryvreckan test beam data reconstruction framework](https://gitlab.cern.ch/corryvreckan/corryvreckan).
However, cosmic data is different, as the number of available tracks is much
lower, and their angles larger. This leads to Corryvreckan not being able to
analyze it properly, and we have to work with the data by hand using Python.

If you think the data set you're working with is fit for Corry, continue
[here](2_Standard_Analysis).

### Manual Analysis

If you think, the data set you're working with is **not** fit for Corry,
continue [here](3_Manual_Analysis)
