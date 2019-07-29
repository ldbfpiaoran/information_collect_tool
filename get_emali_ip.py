import re
import dns.resolver
import sys

class SPF(object):
    def __init__(self):
        self.ips = []
        self.included_domains = []
        self.ip_segments = []
        self.root = []

    def spf(self, domain):
        txt_items = dns.resolver.query(domain, 'txt')
        for txt in txt_items:
            txt = txt.to_text().strip()
            if re.search(r"^\"v=spf", txt):
                self.parse_spf(domain, txt.strip('"'))

    def parse_spf(self, domain, record):
        for item in record.split(' '):
            if re.search(r'^ip4:', item):
                ip = item[4:]
                is_ip_segment = False
                if '/' in ip:
                    self.ip_segments.append(ip)
                    is_ip_segment = True
                else:
                    self.ips.append(ip)
                self.root.append({"domain": domain, "ip": ip, "ip_segment": is_ip_segment})
            elif re.search(r'^include:', item):
                include = item[8:]
                if not (include in self.included_domains or include == domain):
                    self.spf(include)
                self.included_domains.append(include)


spf = SPF()
domain = sys.argv[1]
spf.spf(domain )

print(spf.root)

print(spf.ips)

print(spf.ip_segments)

print(spf.included_domains)
