# hm-config: Helium Miner Config Container

# building from Windows

gpiozero does not support python > 3.9  
Until they fix it https://github.com/gpiozero/gpiozero/blob/master/gpiozero/devices.py  
Also libmraa (rock pi) does not support OS > bookworm (and we switched to bullseye)

Install required tools:  
```powershell
#pyenv
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

#python 3.9.13
pyenv install 3.9.13
pyenv global 3.9.13
python -m pip install --upgrade pip

#install pipx then poetry
python -m pip install --user pipx
python -m pipx install poetry

#Suppose docker is already installed
```

Go the the project root folder and:
```powershell
poetry lock
```

Note: after you change the content of `pyproject.toml`, update `poetry.lock`.

Build docker image, then push the docker image to `docker_ip`:
```powershell
docker buildx build --platform linux/arm64 .
docker tag <image_id> vapolia/hm-config:latest
docker save -o hm.tar vapolia/hm-config:latest
scp hm.tar user@docker_ip:~

#on the docker_ip machine:
sudo docker load -i hm.tar
```

Test:  
```bash
#change the values of VARIANT (miner brand and model), E0 (ethernet MAC), W0 (Wifi MAC), FRIENDLY, serial_number, RE (region)
VARIANT='sensecap-fl1'  

cat <<EOF > diag.json
{
  "last_updated": "19:29 UTC 11 Feb 2024",

  "AN": "helium-vapolia-ant",
  "APPNAME": "Crankk miner",

  "VA": "$VARIANT",
  "BT": true,
  "TYPE": "Full",
  "BUTTON": 27,
  "RESET": 17,
  "STATUS": 22,
  "SPIBUS": "spidev0.0",
  "CELLULAR": false,
  "E0": "FF:EE:DD:69:88:11",
  "W0": "CC:DD:BB:69:88:12",

  "FRIENDLY": "Crank's miner",
  "serial_number": "001122",

  "FW": "1.0.3",
  "OK": "solana-wallet-address",
  "PK": "solana-wallet-address",
  "RE": "EU868",

  "PF": true,
  "firmware_short_hash": "?"
}
EOF

#VARIANT: get one from the list https://github.com/NebraLtd/hm-pyhelper/blob/master/hm_pyhelper/hardware_definitions.py
#For ex: 'pisces-fl1' for Pisces P100, 'sensecap-fl1' for sensecapM1
heliumVersion=$(sudo docker exec miner helium_gateway --version)

#NET_ADMIN required, as it can configure the Wifi
#privileged required to access the system dbus, to add the bluetooth service
#note: the ble calls controlling the helium miner are non functional (ie: onboard, assert location, ...): they require the session dbus.

sudo docker run -d --name helium-config \
    --privileged \
    --net=host \
    --cap-add NET_ADMIN \
    -v $HOME/diag.json:/usr/src/diag.json \
    -e VARIANT="$VARIANT" \
    -e FIRMWARE_VERSION="$heliumVersion" \
    -e DIAGNOSTICS_JSON_URL="file:///usr/src/diag.json" \
    -v /run/dbus:/host/run/dbus \
    -v /sys/kernel/debug:/sys/kernel/debug \
    -e DBUS_SYSTEM_BUS_ADDRESS="unix:path=/host/run/dbus/system_bus_socket" \
    vapolia/hm-config
```


# intro

This repository contains the Dockerfile, basic scripts  and additional libraries required for the BTLE Application tool.
[helium/gateway-config](https://github.com/helium/gateway-config) is the upstream repo that this is built against.

Directory layout:

- `.github/`: Github workflows and other settings.
- `example/`: Files that are examples of what will be loaded on an actual hotspot. These files are especially useful for testing without a full hotspot.
- `gatewayconfig/`: The main Python application.
- `lib/`: Python files copied from other reposittories.
- `protos/`: Protobuf definitions. Generated protos go to `gatewayconfig/protos/` by default.
- `tests/`: Test files.

## Local development environment

Running locally:

```
PYTHONPATH=./ MINER_KEYS_FILEPATH=./example/onboarding_key.txt ETH0_MAC_ADDRESS_PATH=./example/eth0_mac_address.txt python minerconfig
```

The code has been developped and tested with the Raspberry Pi 3 B+. There are a few ways to build this app:

## Testing

Assuming virtualenv has been activated, execute the following command to run the tests:

```
poetry install --with dev
poetry run pytest --cov=gatewayconfig --cov=lib --cov-fail-under=70
```

## Generating protobufs

- Install protobuf
    - Ubuntu: `sudo snap install protobuf`
    - Mac: `brew install protobuf` (also see [here](https://google.github.io/proto-lens/installing-protoc.html))
- Run `generate-protos.sh`
    - `sh protos/generate-protos.sh` or simply `protos/generate-protos.sh` if it is executable

## Pre built containers

This repo automatically builds docker containers and uploads them to two repositories for easy access:
- [hm-config on DockerHub](https://hub.docker.com/r/vapolia/hm-config)
