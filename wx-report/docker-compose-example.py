version: "3"
services:

  wx-report:
    image: marrold/wx-report
    container_name: wx-report
    restart: always
    environment:
      - CITY=London
      - IP_ADDRESS=0.0.0.0
      - PORT=9000
