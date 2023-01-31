#!/usr/bin/env python
import pika, sys, os, send

def main():
    send.send(pika.BasicProperties(), 'This is the message')
    
if __name__ == '__main__':
    try:
        main()
    
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
