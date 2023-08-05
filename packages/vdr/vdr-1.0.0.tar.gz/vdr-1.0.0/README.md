
# VDR

VDR is a Python library for simulate a VDR.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vdr.

```bash
pip install vdr
```

## Usage

```python
import vdr

VDR = vdr.Vdr('/home/USER') # Create the VDR with its storage path
VDR.add_connection('ECDIS') # Create socket connection called 'ECDIS'
VDR.add_connection('nmea') # Create socket connection called 'nmea'

# Initialize threads with each data type that connections will received
ecdis = vdr.ReceivingFrame(VDR, "ECDIS")
nmea = vdr.ReceivingNmea(VDR, "nmea")

# Start threads, ready to receive and store data
ecdis.start()
nmea.start()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)