version: "3"
services:

  packet-8ball:
    image: marrold/packet-8ball
    container_name: packet-8ball
    restart: always
    environment:
      - MY_CALL=N0CALL
      - IN_FILE=/tmp/in.txt
      - OUT_FILE=/tmp/out.txt
