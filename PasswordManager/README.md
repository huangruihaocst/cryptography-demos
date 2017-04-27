#Password manager

[Programming Assignment #3](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/j1eedx9gvai1kg/prog3.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1493291572&Signature=lujBMAakYB5wETxNeFihoyW1bpY%3D)

All the codes are self-documented or have further comments beside. 

##Requirements
- Python 3.6.0
- Pycrypto 2.6.1

##Solution
I implemented the protocol mainly based on the [solution of Assignment 4](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/j1hvqr9u4pa1eb/hw4sol.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1493291706&Signature=WNZor8Vym7Yti6pn7YpkWCowszo%3D) and made some modifications:

- I removed the check of cirtificates.
- I used json files for storing.
- I added a token system for the protocol. After the user authenticated, he will get a token for later operations. Each time he adds/reads/updates/removes a password, he will append this token to the front of the plaintext he is going to send and the server will check if this token corresponds with the token dictionary. Each time after the operation is done, the server generate a new token for the client and both the server and client update this token.
- As a dictionary is used, this protocol also allows for multi-client.
- I added a log out API which will remove his token in the server and he needs to authenticate again to get access to the passwords.
