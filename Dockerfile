# Licensed under the MIT License.

####################################################################################################
################################## Stage: builder ##################################################

# The balenalib/raspberry-pi-debian-python image was tested but missed many dependencies.
FROM python:3.9-bookworm AS builder

# Nebra uses /opt by convention
WORKDIR /opt/

# Copy python dependencies for `poetry install` later
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
COPY README.md ./README.md
COPY lib/ lib/
COPY gatewayconfig/ gatewayconfig/
COPY *.sh ./


# This will be the path that venv uses for installation below
ENV PATH="/opt/venv/bin:$PATH"

# Install python3-minimal, pip3, wget, venv.
# Then set venv environment copied from builder.
# Finally, use pip to install dependencies.
# hadolint ignore=DL3013
RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends \
#            python3-minimal \
#            python3-pip \
            wget \
#            python3-venv \
            # The remaining dependencies are for PyGObject
            # https://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-logo-ubuntu-debian-logo-debian
            libgirepository1.0-dev\
            libcairo2-dev \
            pkg-config \
#            python3-dev \
            libdbus-1-dev \
            gir1.2-gtk-3.0 \
            && \
    # Because the PATH is already updated above, this command creates a new venv AND activates it
    python -m venv /opt/venv && \
    # Given venv is active, this `pip` refers to the python3 variant
    pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config installer.max-workers 10  && \
    poetry install --no-cache --no-root --no-interaction --no-ansi -vvv && \
    poetry build && \
    pip install --no-cache-dir dist/hm_config-1.0.tar.gz

# No need to cleanup the builder

####################################################################################################
################################### Stage: runner ##################################################

#TODO: switch to "Raspberry Pi OS Lite"
FROM python:3.9-slim-bullseye AS runner


#ADD https://apt.radxa.com/bullseye-stable/public.key /etc/apt/keyrings/bullseye.key
#ADD https://apt.radxa.com/bullseye-stable/public.key /etc/apt/trusted.gpg.d/bullseye.key
 

# Install bluez, libdbus, network-manager, python3-gi, and venv
RUN \
    #required with old distro: add correct sources
    #export DISTRO=bullseye-stable && \
    #echo "deb https://apt.radxa.com/$DISTRO/ ${DISTRO%-*} main" | tee -a /etc/apt/sources.list.d/apt-radxa-com.list && \
    apt-get install raspberrypi-archive-keyring && \
    #update
    apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        bluez \
        wget \
        libdbus-1-3 \
        network-manager \
        python3-gi \
#        python3-venv \
        nano \
        curl \
        dbus \
        procps \
        python3-gpiozero \
        libc6 \
    apt-get autoremove -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Nebra uses /opt by convention
WORKDIR /opt/

# pigpio (ok, but frequent disconnections)
# RUN \
#     apt-get update && \
#     apt-get install -y wget make unzip gcc && \
#     wget -O pigpio.zip https://github.com/joan2937/pigpio/archive/master.zip && \
#     unzip pigpio.zip && \
#     cd pigpio-master && make && make install && cd .. && \
#     rm pigpio.zip && rm -r pigpio-master && apt-get remove -y make unzip gcc && \
#     apt-get autoremove -y && apt-get clean
#required as gpiozero now default to lgpio, which is non working
#ENV GPIOZERO_PIN_FACTORY=pigpio

ENV GPIOZERO_PIN_FACTORY=rpigpio


COPY *.sh ./
ENV PYTHONPATH="/opt:$PYTHONPATH"
ENV PATH="/opt/venv/bin:$PATH"

# Copy venv from builder and update PATH to activate it
COPY --from=builder /opt/venv /opt/venv

#RockChip: add libmraa (python 3.9 only)
# hadolint ignore=DL3008, DL4006
# export DISTRO=bullseye-stable && \
#https://github.com/radxa/apt (not available for bullseye)
#unmet dependencies: python,python2.7,libpython2.7,python3.9,libpython3.9 
#    wget -nv -O - apt.radxa.com/$DISTRO/public.key | gpg --dearmor -o /usr/share/keyrings/apt-radxa-com-archive-keyring.gpg && \

#RUN \
#     export DISTRO=bullseye-stable && \
#    apt-get update -qq && \
#     apt-get install -y --no-install-recommends gnupg && \
#     echo "deb http://apt.radxa.com/$DISTRO/ ${DISTRO%-*} main" | tee -a /etc/apt/sources.list.d/apt-radxa-com.list && \
#     wget -nv -O - apt.radxa.com/$DISTRO/public.key | apt-key add - && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends libmraa && \
#    apt-get autoremove -y && \
#    apt-get clean


# This is the libmraa install location, because we are using venv
# it must be added to path explicitly
#ENV PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.9/dist-packages"

# Run start-gateway-config script
ENTRYPOINT ["/opt/start-gateway-config.sh"]

