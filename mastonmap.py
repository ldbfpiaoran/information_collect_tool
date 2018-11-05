import sys
import xmltodict
import subprocess
import logging
import colorlog


'''
set log this code is Useless
log.debug  is white ,info is green ,warn is yellow ,error is red ,critical  red!
'''
LOG_LEVEL = logging.NOTSET
LOGFORMAT = "[%(log_color)s%(levelname)s] [%(log_color)s%(asctime)s] %(log_color)s%(filename)s [line:%(log_color)s%(lineno)d] : %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
colorlog.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', filename='myapp.log',filemode='w', datefmt='%a, %d %b %Y %H:%M:%S', )
formatter = colorlog.ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(LOG_LEVEL)
log.addHandler(stream)




default_encodeing = 'utf-8'
scan_dict = {}

ipdata = sys.argv[1]
log.info('start  use masscan scan {}'.format(ipdata))
log.info('masscan -p0-65535 {}  --rate=100000  --banners -oX scan.xml'.format(ipdata))
chi = subprocess.Popen('masscan -p0-65535 {}  --rate=10000  --banners -oX scan.xml'.format(ipdata), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
result = chi.stdout.read().decode("utf8", "ignore")
log.info('masscan is ok\n\n\n')



with open('scan.xml') as f ,open(ipdata.replace('/24',''),'w') as e:
    try:
        xml_obj = xmltodict.parse(f.read())
        host = xml_obj['nmaprun']['host']
        for line in host:
            ip = line['address']['@addr']
            port = line['ports']['port']['@portid']
            if ip in scan_dict.keys():
                scan_dict[ip] = scan_dict[ip]+','+port
            else:
                scan_dict[ip] = port
    except Exception as e:
        log.error(e)
    for i in scan_dict:
        try:
            command = 'nmap -sV -Pn -T4 -sC --version-all {} -p{}'.format(i,scan_dict[i])
            log.info('start {}'.format(command))
            child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            result = child.stdout.read().decode("utf8", "ignore")
            log.info(result+'##################\n\n')
            e.write(result+'##################\n\n')
        except Exception as e:
            log.error(e)

        
