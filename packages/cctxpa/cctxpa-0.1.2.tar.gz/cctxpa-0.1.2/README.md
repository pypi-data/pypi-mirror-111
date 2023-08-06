# Pcap-analyser

> This repository concerns only on extracting features from pcap files.   
>
> The code which is used to pull feed and save them into database is in another repository.  
> 
> Please checkout support-email-extractor brunch which can be used to test. The master brunch is used for front-end and isn't completed.  


## Getting Started 使用指南
### Prerequisites
```
python 3.8.6
```

### Usage
- install from pip
```sh
pip install cctxpa
```

- usage
```sh
usage: cctxpa [-h] [--host HOST] [--port PORT] [--https] [--path PATH] -u USERNAME -p PASSWORD -f PCAPFILE [-o OUTPUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           CCTX pcap analyser server addresss
  --port PORT           CCTX pcap analyser server port
  --https               Use https or http
  --path PATH           CCTX pcap analyser server login path
  -u USERNAME, --username USERNAME
                        Username
  -p PASSWORD, --password PASSWORD
                        Password
  -f PCAPFILE, --pcapfile PCAPFILE
                        Pcap file need to parse!
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        A file to store output report
```

### Usage example 使用示例
Test pcap files are:  ids1.pcap ftp.pcap ftp2.pcap ftp3.pcap imap.pcap smtp1.pcap pop3.pcap   
Ids1.pcap file is a public dataset.
```sh
cctxpa -u zoeyyy -p 123456 -f ids1.pcap
cctxpa -u zoeyyy -p 123456 -f ftp.pcap
```

### Compile self and upload to PyPI
- Fist, modify `setup.py` 

- Second, compile and upload

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Authors 作者

* **Yangyi Zou**

