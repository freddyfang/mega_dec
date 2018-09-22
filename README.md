# Mega Encrypted Link Decryption

Some mega links are encrypted by MegaDownload. However, MegaDownloader does not support MacOS. This useful script can help decrypt links either singly or in batch.

Support following link formats:
 - mega://enc?xxxxxx
 - mega://enc2?xxxxxx

## How to Use

### Single link
```python
python mega_dec.py {link}
```
### Links file
```python
# Each link as a new line
python mega_dec.py -b {input} {output}
```

### Requirements
     1. PyCrypto
