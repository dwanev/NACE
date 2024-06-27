

# Installing & Running

This page gives instructions on checking this out and getting it running by a set of new eyes. The steps are:

- Create python environment, (i.e. using conda) 
- install dependencies
- Run NACE

# Create python environment, install dependencies (mac)

minigrid https://minigrid.farama.org/
gymnasium https://gymnasium.farama.org/
NACE https://github.com/patham9/NACE 


```commandline

conda create -n NACE python=3.11  
conda activate NACE  
python3 -m pip install matplotlib  

# Gymnasium dependencies
conda install -c torchhd torchhd  
python3 -m pip install "gymnasium[classic-control]"
python3 -m pip install minigrid


```


# Run NACE

```commandline

conda activate NACE
python3 main.py


```










