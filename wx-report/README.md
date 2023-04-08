
# wx-report

Returns a basic weather report to connected users, initially for a defined city, and then prompts users if they wish to look up the weather for another City.

The data and formatting is pulled from [wttr.in](https://wttr.in/)

[Github](https://github.com/marrold/packet-apps)
[Docker Hub](https://hub.docker.com/repository/docker/marrold/wx-report)

## Usage

### Docker

See `docker-compose-example.yml` for hints on running inside Docker.

### Native Python

Install the dependencies:

`pip install -r requirements.txt`

Run the program:

```python wx-report.py [-i IP_ADDRESS] [-p PORT] [-c CITY]```


## Configuration

Configuration can be supplied as arguments or environment variables:

| Short | Long | Env Var| Description | Default                                                           |
|--------------|---------------|--|---------------------------------------------------------------------------|--|
| -h         | --help     |  N/A | Show the help message and exit   | N/A                                      |
| -i         | --ip-address | IP_ADDRESS | The IP address to listen on   | 127.0.0.1 | 
| -p         | --port | PORT | The port number to listen on (default: 9000)  | 9000 |
| -c         | --city | CITY | The home city to get the weather for (default: 'aylesbury') | Aylesbury |


## License

Released under the MIT License:


```Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
