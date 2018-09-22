import re
import base64
from Crypto.Cipher import AES
import sys


def urlb64_to_b64(s):
    b64 = s.replace('-', '+').replace('_', '/').replace(',', '')
    r = len(b64) * 6 % 8
    while r != 0:
        b64 += '='
        r = (r + 6) % 8

    return b64


def decrypt(link):
    match = re.match(r'mega://enc(\d*)\?([a-zA-Z0-9\-_\,]+)', link)
    if not match:
        raise ValueError('Illegal link format')

    version = match[1]
    data = match[2]
    b64data = urlb64_to_b64(data)

    iv = '79F10A01844A0B27FF5B2D4E0ED3163E'
    key = {
        '': '6B316F36416C2D316B7A3F217A30357958585858585858585858585858585858',
        '2': 'ED1F4C200B35139806B260563B3D3876F011B4750F3A1A4A5EFD0BBE67554B44'
    }[version]

    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, bytes.fromhex(iv))
    plain = cipher.decrypt(base64.b64decode(b64data))

    return 'https://mega.nz/#' + plain.decode('ASCII').strip()


def print_usage():
    print('''
    Usage: 
        1. python main.py {link}
        2. python main.py -b {links file} {output file}''')


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    # Single link
    if sys.argv[1].startswith('mega'):
        print(decrypt(sys.argv[1]))
        return

    try:
        operation = sys.argv[1][0:2]
    except KeyError:
        print_usage()
        return

    # Further operations
    if operation == '-b' and len(sys.argv) > 3:

        # Batch decryption
        with open(sys.argv[2]) as src, open(sys.argv[3], 'w') as dest:
            for link in src:
                try:
                    dec_link = decrypt(link)
                except ValueError as err:
                    dec_link = str(err)

                dest.write(dec_link + '\n')


if __name__ == '__main__':
    main()