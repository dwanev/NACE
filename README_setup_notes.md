

# Installing & Running

This page gives instructions on checking this out and getting it running by a set of new eyes. The steps are:

- Create python environment, (i.e. using conda) 
- install dependencies
- Install Prerequisites
- Run NACE

# Create python environment, install dependencies


```commandline

conda create -n NACE python=3.11  
conda activate NACE  
python3 -m pip install matplotlib  

```

# Install Prerequisites


## To Install and compile ONA

```commandline
cd ~/projects
git clone https://github.com/opennars/OpenNARS-for-Applications.git
cd OpenNARS-for-Applications
./build.sh

```

## Add ONA's NAR.py to the PYTHONPATH

PYTHONPATH=$PYTHONPATH:~/projects/OpenNARS-for-Applications/misc/Python/NAR.py



# Run NACE

```commandline

conda activate NACE
PYTHONPATH=~/projects/OpenNARS-for-Applications/misc/Python/NAR.py python3 main.py


```




# Other Information

### FYI:  To start an ONA process in a terminal window 

cd ~/projects/OpenNARS-for-Applications  
./NAR shell  

### FYI: To call ONA from python

Ensure the python file OpenNARS-for-Applications/misc/Python/NAR.py is on the python path and import it.  
OR  
(One of my other projects pulls NAR.py from the ONA project, and replicates it with helper functions
TX-Jupiter-Notebooks/0023_nuts2/nar_wrapper.py )









