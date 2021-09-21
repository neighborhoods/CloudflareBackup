import CloudFlare
import json
import time

cf = CloudFlare.CloudFlare(raw=True)

def fetch_zones():
    print("Fetching zones...")
    page_num = 0
    zones = []
    while True:
        page_num += 1
        raw_results = cf.zones.get(params={'per_page': 100})
        results = raw_results['result']
        for zone in results:
            zones.append(zone)

        total_pages = raw_results['result_info']['total_pages']
        if page_num == total_pages:
            break

    print("Fetched {} Zones".format(len(zones)))
    return zones

def fetch_dns_records(zone):
    print("Fetching DNS Records for {}...".format(zone["name"]))
    page_num = 0
    dns_records = []
    while True:
        page_num +=1
        raw_results = cf.zones.dns_records.get(zone["id"], params={'per_page': 100,'page':page_num})
        results = raw_results['result']
        for dns_record in results:
            dns_records.append(dns_record)

        total_pages = raw_results['result_info']['total_pages']
        if page_num == total_pages:
            break

    print("Fetched {} DNS Records for {}".format(len(dns_records), zone["name"]))
    return dns_records

def fetch_page_rules(zone):
    print("Fetching Page Rules for {}...".format(zone["name"]))
    page_num = 0
    page_rules = []
    raw_results = cf.zones.pagerules.get(zone["id"], params={'per_page': 100})
    results = raw_results['result']
    for page_rule in results:
        page_rules.append(page_rule)

    print("Fetched {} Page Rules for {}".format(len(page_rules), zone["name"]))
    return page_rules

def append_dns_records_to_zones(zones):
    for index, zone in enumerate(zones):
        zones[index]["dns_records"] = fetch_dns_records(zone)

    return zones

def append_page_rules_to_zones(zones):
    for index, zone in enumerate(zones):
        zones[index]["page_rules"] = fetch_page_rules(zone)

    return zones

def output_to_file(filename, content):
    output_path = "output/" + filename
    with open(output_path, "a") as zone_file:
        zone_file.write(json.dumps(content))

def main():
    # Build Zones Object
    zones = fetch_zones()
    zones = append_dns_records_to_zones(zones)
    zones = append_page_rules_to_zones(zones)

    # Output File
    timestamp=int(time.time())
    filename = "cf_zones_{}.json".format(timestamp)
    output_to_file(filename,zones)

if __name__ == '__main__':
    main()
