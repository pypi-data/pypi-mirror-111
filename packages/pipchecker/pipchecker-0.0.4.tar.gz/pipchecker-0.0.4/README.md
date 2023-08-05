# Pipcheck

This is a simple package used to check if a pip package is installed

# Usage

In your python script simply import the module and use as follows  
from pipchecker import pipcheck

pipcheck.main('requests')  

Where 'requests' is the package to check if it is installed.
If the package is installed this should return 'requests is already installed in your system'.    
Similarly if the package is not installed in your system or python enviornment,  
it will return 'requests is currently not installed in your system' 




