# Project Title

SDV - Pre deployment validation

### Prerequisites

Use Python Virtual Environment Manager
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```
Install the required packages from requirements.txt

```
pip install -r requirements.txt
```

### Getting Started

data/ Folder contains all dummy pdf, installer-mainfests and mapping files
To start the server run,
```
python server.py
```
Currently there exists two functionalities, extrapolation and validation.

To do a extrapolate POST request, use following command
```
curl --header "Content-Type: application/json"   --request POST   --data '{"pdf_fn":"<>"}'   http://localhost:8888/extrapolate
```
Sample pdf file is located in data directory.

To do a validation POST request, use following command
```
curl --header "Content-Type: application/json"   --request POST   --data '{"pdf_fn":"<>", "inst_fn":"<>", "map_fn":"<>", "key":"<>"}'   http://localhost:8888/validate
```
Sample pdf file, installer file and mapping file is located in data directory.
