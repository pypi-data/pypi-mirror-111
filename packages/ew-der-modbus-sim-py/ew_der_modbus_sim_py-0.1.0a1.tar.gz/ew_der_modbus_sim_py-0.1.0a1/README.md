<div align="center">
  <a href="https://www.energyweb.org/"><img src="https://www.energyweb.org/wp-content/uploads/2019/04/logo-brand.png" alt="EnergyWeb" width="150"></a>
  <h1 style="padding:25px;">
    DER Modbus Simulator
  </h1>
</div>

## Prerequisites
- ```pip>=20.3.4```
- ```pipenv>=2020.8.13```

## Quick start

### Installation steps
```
# Clone demo repository
git clone https://github.com/energywebfoundation/ew_der_modbus_sim_py.git

# Acces project folder
cd ew_der_modbus_sim_py

# Installs pipenv
pip install pipenv --upgrade

# Creates a python3 virtual environment
pipenv --three

# Installs all demo dependencies
pipenv install '.[all]'
```

### Preset environment variables
```
# Modbus Mode [TCP or RTU]
SLAVE_MODE=TCP
# A slave unique ID [int]
SLAVE_ID=1

# Slave TCP address and port. Defaults to 'localhost:8502'
SLAVE_TCP_ADDRESS=
SLAVE_TCP_PORT=8502

# Slave RTU port 
SLAVE_RTU_PORT=/dev/ptyp5

# DER model map name 
MODEL_MAP_NAME=STP8-10-3AV-40
```

### Virtual environment
```
# Access pipenv's virtual environment in order to run the examples below
pipenv shell
```

## Documentation
### DER Simulator

```
# Running Simulator
python3 ./src/ew_der_modbus_sim_py/der_simulator.py
```