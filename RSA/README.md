#Public key encryption

[Programming Assignment #2](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/j0kbmhds71h4ws/prog2.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1491028922&Signature=UvemW2YNv0nZM2y4FoRNWweGfW0%3D) - Problem 1

All the codes are self-documented or have further comments beside. 

##Requirements
- Python 3.6.0
- Pycrypto 2.6.1

##Solution
###Problem 1 a
I simply implemented the algorithm on the slides, but deleted the part checking if **N** is perfect power. 
I also used an alogorithm to speed calculation like **b<sup>e</sup> mod N**.
###Problem 1 b
I simply implemented the alogrithm on the slides. When it comes to the step choosing **d** and **e** such that **e·d ≡ 1 mod φ(N)**, I chose **e** first and there is possibility that it is a fixed public key **65537** because it is the public key. I used Extended Euclidean algorith when computing **d**.
###Problem 1 c
I simply implemented the alogrithm on the slides. I stored a RSA object inside the ISO_RSA object in order to generate keys conveniently.
###Problem 1 d
I simply implemented the alogrithm on the slides.

##References
[Slides 12](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/izm7tyj3ppf5iv/CS477012.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1491030317&Signature=ylIypPovgwA9dP0upziLeQk4AtY%3D)

[Slides 13](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/izqfmo9plkh58s/CS477013.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1491030385&Signature=EbkQJqgT7iGn6FXJHyjB8rCmJ8M%3D)

[Slides 14](https://piazza-resources.s3.amazonaws.com/ixp1n5argll6bp/j0jws4d3m9i4fq/CS477014.pdf?AWSAccessKeyId=AKIAIEDNRLJ4AZKBW6HA&Expires=1491030427&Signature=ACZNnac3cJmMrVCFiyzODB7kP4Q%3D)

[快速幂取模](http://www.cnblogs.com/7hat/p/3398394.html)

[Extended Euclidean algorithm](https://zh.wikipedia.org/wiki/%E6%89%A9%E5%B1%95%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%AE%97%E6%B3%95)

[Optimal asymmetric encryption padding(Wikipedia)](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding)
