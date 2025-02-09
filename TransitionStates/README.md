Directory for transition state geometry optimizations.  

Only the "Calcall" directory used the MiMe script (to calculate a new Hessian at each optimization step).  
All other directories in this repository used checkpoint files to read-in the Hessian at the different optimization stages, although this behaviour is what MiMe seeks to automate without the need for saved checkpoint files.
