
# adventure-server
A Docker container for running [Colossal Cave Adventure](https://en.wikipedia.org/wiki/Colossal_Cave_Adventure), intended for use with Packet Radio.

Based on a modified version of John Newcombe G6AML's [original conversion](https://bitbucket.org/johnnewcombe/adventureserver/src/master/). Also checkout John's [website](https://glasstty.com/)

[Github](https://github.com/marrold/packet-apps)
[Docker Hub](https://hub.docker.com/repository/docker/marrold/wx-report)

## Usage

### Docker

See `docker-compose-example.yml` for hints on running inside Docker.

### Native Python

Install the dependencies:

```
apt-get -y install python3-tornado python3-pip
pip3 install adventure
```

Run the program:

```python adventure_server.py [--listen-ip] [--listen-port] [--term-width]```


## Configuration

Configuration can be supplied as arguments or environment variables:

| Argument | Env Var| Description | Default                                                           |
|--------------|---------------|--|---------------------------------------------------------------------------|--|
| `--help`     |  N/A | Show the help message and exit   | N/A                                      |
| `--listen-ip` | LISTEN_IP| The IP address to listen on   | 127.0.0.1 | 
| `--listen-port` | LISTEN_PORT | The port to listen on | 9001 |
| `--term-width` | TERM_WIDTH| The client's terminal width (40 or 80 chars) | 80|


