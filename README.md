# Student Statistics

## Setup and installation
```zsh
python setup.py install
```
## Usage
Start mariadb, prometheus, phpmyadmin in docker
```zsh
make start_service
```

Start web server on localhost
```zsh
web-start
```

## Developer Guide
Install tox
```zsh
pip install tox
```

Run unittests:
```zsh
tox -e unittests
```

Testing script:
```zsh
bash test.sh
```
