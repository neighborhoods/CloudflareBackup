import time
import json
import CloudFlare

cf = CloudFlare.CloudFlare(raw=True)

backup_data = json.load(open('cf_zones_1518489811.json'))
new_zone_id = "1c1d50fc3ea017ec77f1f2911ff47b54"

def fetch_zones():
    for zone in backup_data:
        if zone["name"] == "55places.com":
            cf.zones.post(params={'name':'55places.com'})

def main():
    fetch_zones()
    cf.zones.dns_records.put()

if __name__ == '__main__':
    main()