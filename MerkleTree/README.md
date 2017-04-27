#Merkle trees

[Programming Assignment #2](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/j0kbmhds71h4ws/prog2.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1491028922&Signature=UvemW2YNv0nZM2y4FoRNWweGfW0%3D) - Problem 2

All the codes are self-documented or have further comments beside. 

##Requirements
- Python 3.6.0
- Pycrypto 2.6.1

##Solution
I simply implemented the algorithm on the slides. Each node stores its data(hash), left child, right child, parent, and it contains which files' information. The tree stores the root node. Using this node, I can get all the information of this tree, including all the nodes. I just operated the tree to implement the creating, reading and writing operation.

##References
[Slides 12](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/izm7tyj3ppf5iv/CS477012.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1491030317&Signature=ylIypPovgwA9dP0upziLeQk4AtY%3D)

