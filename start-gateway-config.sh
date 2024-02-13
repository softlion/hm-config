#! /bin/bash

# Wait for the diagnostics app to be loaded
DIAGNOSTICS_JSON_URL=${DIAGNOSTICS_JSON_URL:-'http://diagnostics/json'}

until curl -s -m 10 -o /dev/null $DIAGNOSTICS_JSON_URL
do
    echo "Diagnostics container not ready. Sleeping 10s."
    sleep 10
done

# Load dbus-wait script
source /opt/dbus-wait.sh

# Advertise on channels 37, 38 and 39
echo 7 > /sys/kernel/debug/bluetooth/hci0/adv_channel_map
# Send a beacon every 153 x 0.625ms = 95.625ms (244 is 152.5ms)
echo 153 > /sys/kernel/debug/bluetooth/hci0/adv_min_interval
echo 153 > /sys/kernel/debug/bluetooth/hci0/adv_max_interval

# Disable pairing
printf "pairable off\nquit" | /usr/bin/bluetoothctl

# Load setenv script
source /opt/setenv.sh

prevent_start="${PREVENT_START_GATEWAYCONFIG:-0}"
if [ "$prevent_start" = 1 ]; then
    echo "gatewayconfig will not be started. PREVENT_START_GATEWAYCONFIG=1"
    while true; do sleep 1000; done
else
	# Check dbus container is ready and then launch config
    wait_for_dbus \
        && python -m gatewayconfig
fi
