#!/usr/bin/env python3
# Made By R1Px

import requests
import argparse
import urllib.parse
import urllib3
import threading
import queue
import sys
import time
import os

PEMBE = '\033[95m'
MAVI = '\033[94m'
CAMGOBEGI = '\033[96m'
YESIL = '\033[92m'
SARI = "\033[33m"
Black = "\033[30m"
ACIKSARI = '\033[93m'
KIRMIZI = '\033[91m'
DUZ = '\033[0m'
KALIN = '\033[1m'
ALTICIZILI = '\033[4m'
MOR = '\33[35m'
BackgroundDefault = "\033[49m"
BackgroundBlack = "\033[40m"
BackgroundYellow = "\033[43m"

os.system("cls")
time.sleep(1.0)
print(MAVI + """
                                                                                                                                                                                                  
o      o        8         .oPYo.          o  8        .oPYo.                                        
8      8        8         8    8          8  8        8                                             
8      8 .oPYo. 8oPYo.   o8YooP' .oPYo.  o8P 8oPYo.   `Yooo. .oPYo. .oPYo. odYo. odYo. .oPYo. oPYo. 
8  db  8 8oooo8 8    8    8      .oooo8   8  8    8       `8 8    ' .oooo8 8' `8 8' `8 8oooo8 8  `' 
`b.PY.d' 8.     8    8    8      8    8   8  8    8        8 8    . 8    8 8   8 8   8 8.     8     
 `8  8'  `Yooo' `YooP'    8      `YooP8   8  8    8   `YooP' `YooP' `YooP8 8   8 8   8 `Yooo' 8     
::..:..:::.....::.....::::..::::::.....:::..:..:::..:::.....::.....::.....:..::....::..:.....:..::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
01010111 01100101 01100010 01010000 01100001 01110100 01101000 01010011 01100011 01100001 01101110 01101110 01100101 01110010
[*]  Created By R1Px :) https://github.com/R1Px/  [*]

""")

time.sleep(2.0)

def parse_args():
    parser = argparse.ArgumentParser(description="Brute force web directories, ignore responses of a certain size")
    parser.add_argument('-u', '--url', dest='url', help='URL to scan, will be prefixed to each wordlist line',
                        required=True)
    parser.add_argument('-w', '--wordlist', dest='wordlist', help='path to wordlist, one word per line', required=True)
    parser.add_argument('-p', '--proxy', dest='proxy', default=None, help='send identified resources to this proxy. The proxy must do HTTP and HTTPS.')
    parser.add_argument('-s', '--size', dest='size', default='2392', help='If a reply is this size, ignore it. Pass ' +
                        'multiple values comma-separated (100,123,3123)')
    parser.add_argument('-t', '--threads', dest='threads', type=int, default=10)
    parser.add_argument('-a', '--useragent', dest='useragent', default='buster/1.0', help='Set User-Agent')
    parser.add_argument('-f', '--addslash', dest='addslash', default=False, action='store_true',
                        help='append a slash to each request')
    parser.add_argument('-r', '--redirects', dest='follow', default=False, action='store_true', help='Follow redirects')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true', help='be more verbose, not used atm.')
    return parser.parse_args()


def check_url(word_queue, args):
    while not word_queue.empty():
        try:
            word = word_queue.get_nowait()
        except queue.Empty:
            break
        url = args.url + word.lstrip('/')
        if args.addslash and not url.endswith('/'):
            url += '/'
        headers = {'User-Agent': args.useragent}
        response = requests.get(url, verify=False, allow_redirects=args.follow, headers=headers)
        if response.status_code in [200, 204, 301, 302, 307, 401, 403] and len(response.text) not in args.size:
            print(MOR + f"[+] {YESIL}{str([response.status_code])} {SARI}{str(url)} {YESIL}({len(response.text)}) {MOR}[+]")
            if args.proxy is not None:
                proxies = {'http': args.proxy, 'https': args.proxy}
                requests.get(url, verify=False, allow_redirects=args.follow, headers=headers, proxies=proxies)


def main():
    args = parse_args()
    if not args.url.endswith('/'):
        args.url = args.url + '/'

    try:
        sizelist = [int(x) for x in args.size.split(',')]
    except ValueError:
        print(f'Can not parse {args.size}.')
        sys.exit(-1)
    args.size = sizelist

    words = open(args.wordlist).readlines()
    word_queue = queue.Queue()
    for word in words:
        word_queue.put(urllib.parse.quote(word.strip()))


    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=check_url, args=(word_queue, args))
        t.start()
        threads.append(t)

    while True:
        try:
            time.sleep(0.5)
            if word_queue.empty() and True not in [t.is_alive() for t in threads]:
                sys.exit(0)
        except KeyboardInterrupt:
            while not word_queue.empty():
                try:
                    word_queue.get(block=False)
                except queue.Empty:
                    pass
            sys.exit(0)


if __name__ == "__main__":
    urllib3.disable_warnings()
    main()

#########################################
#                                       #
#                                       #
#                                       #
# Coded By R1Px, Enjoy To Use !!!       #
#                                       #
#                                       #
#                                       #
#########################################