import CloudFlare
import json
import time
import re

cf = CloudFlare.CloudFlare(raw=True)
cf_write = CloudFlare.CloudFlare()
agent_pattern = re.compile("^([a-zA-Z]+)55places.com$")
old_endpoint = "55places-facade-elb-663916359.us-east-1.elb.amazonaws.com"
cname_endpoint = "nhds-public-application-478477221.us-east-1.elb.amazonaws.com"

def fetch_zones():
    print "Fetching zones..."
    page_num = 0
    zones = []
    while True:
        page_num += 1
        raw_results = cf.zones.get(params={'per_page':100,'page':page_num})
        results = raw_results['result']
        for zone in results:
            if agent_pattern.match(zone["name"]):
                print(zone["name"])
                zones.append(zone)

        total_pages = raw_results['result_info']['total_pages']
        if page_num == total_pages:
            break

    print "Fetched {} Zones".format(len(zones))
    return zones

def append_dns_records_to_zones(zones):
    for index, zone in enumerate(zones):
        zones[index]["dns_records"] = fetch_dns_records(zone)

    return zones

def fetch_dns_records(zone):
    print "Fetching DNS Records for {}...".format(zone["name"])
    page_num = 0
    dns_records = []
    while True:
        page_num +=1
        raw_results = cf.zones.dns_records.get(zone["id"], params={'per_page': 100,'page':page_num})
        results = raw_results['result']
        for dns_record in results:
            if dns_record["name"] == zone["name"] or dns_record["name"] == "www.{}".format(zone["name"]):
                dns_records.append(dns_record)

        total_pages = raw_results['result_info']['total_pages']
        if page_num == total_pages:
            break

    print "Fetched {} DNS Records for {}".format(len(dns_records), zone["name"])
    return dns_records

def update_records(zones):
    for zone in zones:
        for dns_record in zone["dns_records"]:
            if dns_record["content"] != old_endpoint:
                print "Endpoint does not need an update."
                continue

            data = {
                "type": "CNAME",
                "name": dns_record["name"],
                "content": cname_endpoint,
                "proxied": True,
                "ttl": 1
            }
            try:
                cf_write.zones.dns_records.put(
                    zone["id"],
                    dns_record["id"],
                    data=data
                )
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                print('/zones.dns_records.put %s - %d %s - api call failed' % (dns_record["name"], e, e))


def add_root_to_www_page_rule(zones):
    for zone in zones:
        print "Adding Redirect Rule for: {}".format(zone["name"])
        data = {
            'targets': [
            {
                "target": "url",
                "constraint": {
                    "operator": "matches",
                    "value": "http://{}/*".format(zone["name"])
                }
            }
        ],
            'actions': [
                {
                    'id': 'forwarding_url',
                    'value': {
                        'status_code': 301,
                        'url': "https://www.{}/$1".format(zone["name"])
                    }
                }

            ],
            'priority': 1,
            'status': "active"
        }

        cf.zones.pagerules.post(
            zone["id"],
            data=data
        )


def main():
    zones = fetch_zones()
    #zones = append_dns_records_to_zones(zones)
    #update_records(zones)
    add_root_to_www_page_rule(zones)

if __name__ == '__main__':
    main()