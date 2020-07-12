import os

from ddns_google.client_wrapper import ClientWrapper

acme_challenge_token = os.getenv('ACME_CHALLENGE_TOKEN')
zone_name = os.getenv('ZONE_NAME')
domain = os.getenv('DOMAIN')

cw = ClientWrapper()
cw.add_acme_challenge(zone_name=zone_name, domain=domain, acme_challenge_token=acme_challenge_token)
# cw.cleanup_acme_challenge(zone_name=zone_name, domain=domain)

