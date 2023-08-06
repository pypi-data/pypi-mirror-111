# Double-Ratchet Over Parity Exchange(DOPE)
Python3 Implementation of DOPE Encryption
## Installation
### From source
To install from source use the following command, make sure you have `setuptools>=50.0.0`
```bash
python3 seutp.py install
```
### From PyPI
```bash
pip3 install dope3
```
## Using the DOPE API
Import DOPE
```python
from dope3 import DOPE
```
Once the dope package is imported you need to create the Dope class and initialize it with the required parameters
The parameters include:
1. Your private Key
2. Receiver's Public Key
3. Session Key Size
4. BCH Polynomial
5. Error Correcting Code Size
6. Racheting mode (`BLAKE0x0`/`BLAKEx0x`)
7. AES Mode(`GCM`/`SIV`/`CBC`/`OFB`)
8. HMAC(`SHA256`/`SHA384`/`SHA512`)
9. Key Mode(`XOR-BL`/`AND-BL`)

## Using the DOPE2 API
Import DOPE2
```python
from dope3 import DOPE2
```
Once the dope package is imported you need to create the Dope class and initialize it with the required parameters
The parameters include:
1. Your Key
2. BCH Polynomial
3. Error Correcting Code Size
4. AES Mode(`GCM`/`SIV`/`CBC`/`OFB`)
5. Nonce
6. Block Size