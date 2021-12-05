# This file contains all the UUIDs for each service to try and cut it down.
# Also contains all the descriptors

# Helium service
HELIUM_SERVICE_UUID = "0fda92b2-44a2-4af2-84f5-fa682baa2b8d"

# Generic UUIDs
FIRMWARE_VERSION = "2021.01.01.1"
DEVINFO_SVC_UUID = "180A"
FIRMWARE_SVC_UUID = "0000180a-0000-1000-8000-00805f9b34fb"
MANUFACTURER_NAME_CHARACTERISTIC_UUID = "2A29"
FIRMWARE_REVISION_CHARACTERISTIC_UUID = "2A26"
SERIAL_NUMBER_CHARACTERISTIC_UUID = "2A25"
USER_DESC_DESCRIPTOR_UUID = "2901"
PRESENTATION_FORMAT_DESCRIPTOR_UUID = "2904"

# Firmware UUID
FIRMWARE_VERSION_CHARACTERISTIC_UUID = "00002a26-0000-1000-8000-00805f9b34fb"

# Software Version UUID
SOFTWARE_VERSION_CHARACTERISTIC_UUID = "c0b64050-697d-463a-a33f-70c4825731f8"
SOFTWARE_VERSION_VALUE = "Software Version"

# Onboarding Key
ONBOARDING_KEY_CHARACTERISTIC_UUID = "d083b2bd-be16-4600-b397-61512ca2f5ad"
ONBOARDING_KEY_LABEL = "Onboarding Key"

# Public Key
PUBLIC_KEY_CHARACTERISTIC_UUID = "0a852c59-50d3-4492-bfd3-22fe58a24f01"
PUBLIC_KEY_LABEL = "Public Key"

# WiFiServices
WIFI_SERVICES_CHARACTERISTIC_UUID = "d7515033-7e7b-45be-803f-c8737b171a29"
WIFI_SERVICES_LABEL = "WiFi Services"

# WiFiConfiguredServices
WIFI_CONFIGURED_SERVICES_CHARACTERISTIC_UUID = "e125bda4-6fb8-11ea-bc55-0242ac130003"
WIFI_CONFIGURED_SERVICES_LABEL = "WiFi Configured Services"

# WiFiRemove
WIFI_REMOVE_CHARACTERISTIC_UUID = "8cc6e0b3-98c5-40cc-b1d8-692940e6994b"
WIFI_REMOVE_VALUE = "WiFi Remove"

# Diagnostics
DIAGNOSTICS_CHARACTERISTIC_UUID = "b833d34f-d871-422c-bf9e-8e6ec117d57e"
DIAGNOSTICS_LABEL = "Diagnostics"

# Mac address
MAC_ADDRESS_CHARACTERISTIC_UUID = "9c4314f2-8a0c-45fd-a58d-d4a7e64c3a57"
MAC_ADDRESS_LABEL = "Mac Address"

# Lights
LIGHTS_CHARACTERISTIC_UUID = "180efdef-7579-4b4a-b2df-72733b7fa2fe"
LIGHTS_LABEL = "Lights"

# WiFiSSID
WIFI_SSID_CHARACTERISTIC_UUID = "7731de63-bc6a-4100-8ab1-89b2356b038b"
WIFI_SSID_LABEL = "WiFi SSID"

# AssertLocation
ASSERT_LOCATION_CHARACTERISTIC_UUID = "d435f5de-01a4-4e7d-84ba-dfd347f60275"
ASSERT_LOCATION_LABEL = "Assert Location"

# Add Gateway
ADD_GATEWAY_CHARACTERISTIC_UUID = "df3b16ca-c985-4da2-a6d2-9b9b9abdb858"
ADD_GATEWAY_KEY_LABEL = "Add Gateway"

# WiFiConnect
WIFI_CONNECT_CHARACTERISTIC_UUID = "398168aa-0111-4ec0-b1fa-171671270608"
WIFI_CONNECT_KEY_LABEL = "WiFi Connect"

# Ethernet Online
ETHERNET_ONLINE_CHARACTERISTIC_UUID = "e5866bd6-0288-4476-98ca-ef7da6b4d289"
ETHERNET_ONLINE_LABEL = "Ethernet Online"

# NM Device State
# https://github.com/ProtoThis/NetworkManager/blob/master/tools/test-networkmanager-service.py#L28
NM_DEVICE_STATE_UNKNOWN = "0"
NM_DEVICE_STATE_UNMANAGED = "10"
NM_DEVICE_STATE_UNAVAILABLE = "20"
NM_DEVICE_STATE_DISCONNECTED = "30"
NM_DEVICE_STATE_PREPARE = "40"
NM_DEVICE_STATE_CONFIG = "50"
NM_DEVICE_STATE_NEED_AUTH = "60"
NM_DEVICE_STATE_IP_CONFIG = "70"
NM_DEVICE_STATE_IP_CHECK = "80"
NM_DEVICE_STATE_SECONDARIES = "90"
NM_DEVICE_STATE_ACTIVATED = "100"
NM_DEVICE_STATE_DEACTIVATING = "110"
NM_DEVICE_STATE_FAILED = "120"

# Wifi Status Response
# https://github.com/helium/hotspot-app/blob/75df9970088606b0cc919929edc86764cf814668/src/features/hotspots/settings/WifiSetup.tsx#L26
WIFI_CONNECTED = "connected"
WIFI_ERROR = "error"
WIFI_INVALID_PASSWORD = "invalid"  # nosec B105:hardcoded_password_string false positive

# WiFi Status Mapping
WIFI_STATUSES = {
    NM_DEVICE_STATE_UNKNOWN: WIFI_ERROR,
    NM_DEVICE_STATE_UNMANAGED: WIFI_ERROR,
    NM_DEVICE_STATE_UNAVAILABLE: WIFI_ERROR,
    NM_DEVICE_STATE_DISCONNECTED: WIFI_INVALID_PASSWORD,
    NM_DEVICE_STATE_PREPARE: WIFI_ERROR,
    NM_DEVICE_STATE_CONFIG: WIFI_ERROR,
    NM_DEVICE_STATE_NEED_AUTH: WIFI_ERROR,
    NM_DEVICE_STATE_IP_CONFIG: WIFI_ERROR,
    NM_DEVICE_STATE_IP_CHECK: WIFI_ERROR,
    NM_DEVICE_STATE_SECONDARIES: WIFI_ERROR,
    NM_DEVICE_STATE_ACTIVATED: WIFI_CONNECTED,
    NM_DEVICE_STATE_DEACTIVATING: WIFI_ERROR,
    NM_DEVICE_STATE_FAILED: WIFI_ERROR,
}

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
ETHERNET_IS_ONLINE_CARRIER_VAL = "1"
