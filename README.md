# Search Engine
## By Mugagga Kimera

### Install
### Unix / Macos
#### Run these commands
```bash
python3 -m venv .venv
python -m pip install -r requirements.txt 
source .venv/bin/activate
```

### Windows
#### Run these commands
```bash
py -m venv .venv
python -m pip install -r requirements.txt 
.venv/bin/activate
```

### Usage
#### By default - stemming will be used and no query expansion will be used
#### Unix / Macos
```bash
python main.py
```

#### Windows
```bash
py main.py
```

# Turning on Lemmatization or Query expansion
### In the "main.py" file there will be code as follows
```python
def main():
    SearchEngineIns = SearchEngine(True)
    SearchEngineIns.search()
```

### To change to Lemmatization , set the true value to false.
```python
def main():
    SearchEngineIns = SearchEngine(False)
    SearchEngineIns.search()
```
### Then delete the data folder and run the program.

## Query Expansion
### To enable query expansion go the the main function in main.py
```python
def main():
    SearchEngineIns = SearchEngine(True)
    SearchEngineIns.search()
```

### Add another paramter with the value of true to the Search engine initiatior
```python
def main():
    SearchEngineIns = SearchEngine(True,True)
    SearchEngineIns.search()
```

### Then re-run the program