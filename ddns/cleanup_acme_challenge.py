import os

from common.ddns_google.client_wrapper import ClientWrapper

zone_name = os.getenv('ZONE_NAME')
domain = os.getenv('DOMAIN')

cw = ClientWrapper()
cw.cleanup_acme_challenge(zone_name=zone_name, domain=domain)

