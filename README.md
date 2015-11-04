# IPRO Code

## Only thing actually being used out of this is particle_code
    dashboard.particle.io
    
    Just shove it onto a particle photon, correct the analog inputs, and it should log everything to your account's particle dashboard. 
    
## NOT IN USE

Currently the main file is 2.py, which reads input.txt and vals.txt. 

Input.txt contains a decision tree of the given node format, intended to be easily modified. Written line by line.
```
  line_1: node_name
  line_2: node_description
  line_n..+: conditionals declaring which node_name to goto next
  line_n..+1: line break
```
and then the next node can begin, with the same format.

Conditionals are in the form: `if [cond] [(and|or) (cond)] go node_name` with infinite depth for the and/ors. 

Reads left to right, so `A and B or C or F` becomes `(((A and B) or C) or F)`

vals.txt is a simple dict of the form `[key] : [value]`
which serves as the input for the decision tree. 

and of course, 2.py does all the work. Reads, parses, understands, and decides. Spits out the final node.
