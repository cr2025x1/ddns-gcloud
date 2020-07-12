import time
import copy

from google.cloud import dns

init_rrdata = '\"INITIALIZED\"'
acme_challenge_record = '_acme-challenge'
change_await_tick_sec = 10
ttl = 60


class ClientWrapper:
    def __init__(self):
        return

    def add_acme_challenge(self, zone_name, domain, acme_challenge_token):
        rrset_name = f'{acme_challenge_record}.{domain}.'
        print(f'Adding ACME challenge token {acme_challenge_token} to recordset \"{rrset_name}\"...')

        client = dns.Client()
        zone = client.zone(name=zone_name)
        records = zone.list_resource_record_sets()
        acme_rrset = None
        for r in records:
            if r.name == rrset_name:
                print('Existing recordset is...')
                self._print_rrset(r)
                acme_rrset = r

        changes = zone.changes()

        if acme_rrset is not None:
            changes.delete_record_set(acme_rrset)
            if len(acme_rrset.rrdatas) == 1 and acme_rrset.rrdatas[0] == init_rrdata:
                new_rrdata = [f'\"{acme_challenge_token}\"']
            else:
                new_rrdata = copy.deepcopy(acme_rrset.rrdatas)
                new_rrdata.append(f'\"{acme_challenge_token}\"')
        else:
            new_rrdata = [f'\"{acme_challenge_token}\"']

        record_set = zone.resource_record_set(
            rrset_name, 'TXT', ttl, new_rrdata)
        changes.add_record_set(record_set)

        changes.create()  # API request
        self._wait_for_changes_to_done(changes)
        print('Change is done.')

        records = zone.list_resource_record_sets()
        for r in records:
            if r.name == rrset_name:
                print('Existing recordset is...')
                self._print_rrset(r)

        if acme_rrset is not None:
            print(f'Waiting for {acme_rrset.ttl} secs to let cache TTL expire...')
            time.sleep(acme_rrset.ttl)
        else:
            print(f'No existing recordset {rrset_name} confirmed.')

    def cleanup_acme_challenge(self, zone_name, domain):
        rrset_name = f'{acme_challenge_record}.{domain}.'
        print(f'Cleaning up ACME challenge token from recordset \"{rrset_name}\"...')

        client = dns.Client()
        zone = client.zone(name=zone_name)
        records = zone.list_resource_record_sets()
        acme_rrset = None
        for r in records:
            if r.name == rrset_name:
                print('Existing recordset is...')
                self._print_rrset(r)
                acme_rrset = r

        changes = zone.changes()

        if acme_rrset is not None:
            changes.delete_record_set(acme_rrset)

        record_set = zone.resource_record_set(
            rrset_name, 'TXT', ttl, [init_rrdata])
        changes.add_record_set(record_set)

        changes.create()  # API request
        self._wait_for_changes_to_done(changes)
        print('Change is done.')

        records = zone.list_resource_record_sets()
        for r in records:
            if r.name == rrset_name:
                print('Existing recordset is...')
                self._print_rrset(r)

        if acme_rrset is not None:
            print(f'Waiting for {acme_rrset.ttl} secs to let cache TTL expire...')
            time.sleep(acme_rrset.ttl)
        else:
            print(f'No existing recordset {rrset_name} confirmed.')

    def _print_rrset(self, rrset):
        print(f'Name: {rrset.name}')
        print(f'Record type: {rrset.record_type}')
        print(f'TTL: {rrset.ttl}')
        print(f'RRData: {rrset.rrdatas}')

    def _wait_for_changes_to_done(self, changes):
        while changes.status != 'done':
            print('Waiting for changes to complete...')
            time.sleep(change_await_tick_sec)  # or whatever interval is appropriate
            changes.reload()  # API request
