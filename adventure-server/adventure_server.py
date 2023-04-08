import logging
import struct
import traceback
import argparse
import os
import sys
import re

from adventure import load_advent_dat
from adventure.game import Game

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.options import options as tornado_options
from tornado.tcpserver import TCPServer


parser = argparse.ArgumentParser()
parser.add_argument("--listen-ip", type=str, default="127.0.0.1", help="IP address to listen on")
parser.add_argument("--listen-port", type=int, default=9001, help="Port to listen on")
parser.add_argument("--term-width", type=str, default="80", help="The client's terminal width (40 or 80)")
opts = parser.parse_args()


LISTEN_IP = os.getenv('LISTEN_IP', opts.listen_ip)
LISTEN_PORT = int(os.getenv('LISTEN_PORT', opts.listen_port))
TERM_WIDTH = os.getenv('TERM_WIDTH', opts.term_width)

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Cache this struct definition; important optimization.
int_struct = struct.Struct("<i")
_UNPACK_INT = int_struct.unpack
_PACK_INT = int_struct.pack

loop = IOLoop.current()


class TornadoServer(TCPServer):

    def __init__(self):

        TCPServer.__init__(self)
        self.current_frame = None

    def load_advent_dat(self, data):

        """
        This method is used in place of the load_advent_dat method defined in data.py of the Adventure package.
        The method allows a alternative dat file to be specified without affecting the package.
        """
        import os
        datapath = os.path.join(os.path.dirname(__file__), f'advent{TERM_WIDTH}.dat')
        from adventure.data import parse

        with open(datapath, 'r', encoding='ascii') as datafile:
            parse(data, datafile)

    @gen.coroutine
    def handle_stream(self, stream, address):

        logger.info("[adventure] Connection from client address {0}.".format(address))

        stream.write(b"Collosal Cave Adventure - Converted by John Newcombe (G6AML)\r\n")
        stream.write(b"https://bitbucket.org/johnnewcombe/adventureserver/src/master/\r\n")
        stream.write(b"ENTER QUIT AT ANYTIME TO RETURN TO THE NODE\r\n\r\n")

        try:
            line = ''
            game = Game()
            self.load_advent_dat(game)


            game.start()
            stream.write(game.output.encode('utf-8'))

            while True:

                char = yield stream.read_bytes(1)

                # tidy up any Prestel type CRs
                if char == b'\x5f':
                    char = b'\r'

                if ord(char) < 128:
                    line += char.decode()

                if char == b'\r':

                    command = line.lower()

                    if command.startswith('save') : # disable 'SAVE'
                        command = 'evas'

                    # Hack to quit the game at anytime, including at instructions prompt
                    if command.startswith('quit') or command.startswith('QUIT'):
                        stream.write(b"\r\nDisconnected...")
                        stream.close()

                    words = re.findall(r'\w+', command)

                    if words:
                        response = game.do_command(words)
                        logger.info('[adventure] command response = {0}'.format(response))
                        stream.write(response.encode('utf-8'))
                    line = ''

                else:
                    # no echo on this service is better for telnet connections and reduces bandwidth
                    pass

                if game.is_done:
                    # TODO: Investigate how to signal a clean exit back to any calling system, e.g. TELSTAR.
                    stream.write(b"\r\nDisconnected...")
                    stream.close()

        except StreamClosedError as ex:
            logger.info("[adventure] Client address {0} disconnected.".format(address))

        except Exception as ex:
            logger.error("[adventure] {0} Exception: {1} Message: {2}".format(address, type(ex), str(ex)))
            logger.error(traceback.format_exc())


if __name__ == '__main__':

    if TERM_WIDTH not in ["40", "80"]:
        logger.error('[adventure] term-width must be 40 or 80 chars. Exiting')
        sys.exit()

    logger.info(f"[adventure] Starting server on {LISTEN_IP}:{LISTEN_PORT}. TERM_WIDTH is {TERM_WIDTH}")
    server = TornadoServer()
    server.listen(LISTEN_PORT, LISTEN_IP)
    loop.start()
