import os

LOCALE = os.getenv('AURA_LOCALE', 'en-US')
AURA_APP_IDENTIFIER = os.getenv('AURA_APP_IDENTIFIER', 'com.pushd.client')
# TODO: Load device identifier through config
DEVICE_IDENTIFIER = os.getenv('AURA_DEVICE_IDENTIFIER', '0000000000000000')
IMAGE_PROXY_BASE_URL = 'https://imgproxy.pushd.com'
