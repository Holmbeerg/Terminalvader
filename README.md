# Terminalväder
Small CLI program for checking the weather! The SMHI API has bounds and is meant to be used for the Nordic region.

## Installation

Before installing make sure you have Python and pip installed.  

Clone the project, enter the project directory and then you can install with 
```bash
pip install -e .  
```

## PATH

On Linux I had to add:  
```bash
export PATH="$HOME/.local/bin:$PATH"
```
to my .bashrc, might have to do something similar on Mac or Windows if you don't have this added to PATH already.

