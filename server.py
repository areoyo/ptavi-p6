#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""


import sys
import socketserver
import os


if len(sys.argv) != 4:
    sys.exit("Usage: python  server.py IP port audio_file")
_, IP, PORT, FICH = sys.argv
PORT = int(PORT)


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            datos = line.decode('utf-8').split()
            print(line.decode('utf-8'))
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

            if datos[0] == "INVITE":
                self.wfile.write(b"SIP/2.0 100 Trying" + b"\r\n")
                self.wfile.write(b"SIP/2.0 180 Ring" + b"\r\n")
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n")
            if datos[0] == "ACK":
                aEjecutar = "./mp32rtp -i " + IP + " -p 23032 < " + FICH
                print("Vamos a ejecutar ", aEjecutar)
                os.system(aEjecutar)
            if datos[0] == "BYE":
                self.wfile.write(b"\r\n" + b"SIP/2.0 200 OK" + b"\r\n")
            elif datos[0] != "INVITE" or "BYE" or "ACK":
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed" + b"\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request" + b"\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
