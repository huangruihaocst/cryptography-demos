#Padding oracle against CBC encryption

[Programming Assignment #1](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/iyp83k9edi11h1/prog1.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1486683387&Signature=kRutt%2FswaAs4rjh5cRnXCYZCy0I%3D) - Problem 2

All the codes are self-documented or have further comments beside. 

##Requirements
- Python 3.6.0
- Pycrypto 2.6.1

##Solution
I implemented the padding oracle attack in the way discussed in class. That is to first calculate the length of the padding, so we know the last several bytes of the last block. Then traverse all the possible bytes of the byte currently being guessed and send it to server until the padding is valid. At this time by using some definitized algorithm we can know precise of this byte. Use this way to guess from the last unknown byte to the first unknown byte. Finally we get the entire last block.

##References
[Slides 08](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/iyp7ti643q0z5/CS47708.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1486682866&Signature=GiG1IlwPdp5Q%2B1jdeM1ZkgYHf6U%3D)

[Padding oracle attack (Wikipedia)](https://en.wikipedia.org/wiki/Padding_oracle_attack)