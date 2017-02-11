## pymm (python modbus master)

###Installing

You will need the pymodbus-library to use this tool:  
```bash
sudo pip install pymodbus
```

###Usage

Options:
```
  -h, 			--help            	show this help message and exit
  -p PORT, 		--port=PORT  		The port to connect to
  -a ADDRESS, 	--address=ADDRESS 	The device-address to connect to
  -s HOST, 		--server=HOST		The server to scrape
  -r QUERY, 	--range=QUERY		The address range to scan
  -v, 			--verbose         	Enable verbose output
  -f FORMAT, 	--format=FORMAT		Formatting the output
  									e.g. int32, float32
```

To read int:  
```bash
python test.py -s 192.168.2.11 -a 1 -r 0:10 -f float32
```
