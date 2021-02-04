#!/usr/bin/python -tt

import sys,getopt
import logging
import concurrent.futures
import time
import csv
import http.client
import json
import socket


logger = logging.getLogger('stencil')
#hdlr = logging.StreamHandler(sys.stdout)
hdlr = logging.FileHandler('myAppLog.log') 
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO) #logging.DEBUG


def Usage():
  print (" Usage: %s [--help] " % sys.argv[0])

def thread_function(line):
    a = list (getRipeData(line))
    logger.info("Thread \"%s\": started ", line)
    try:
        a.append(socket.gethostbyaddr(line)[0])
    except  socket.herror :
        a.append("")

    logger.info("Thread \"%s\": finishing ", line)
    return a
    

def getRipeData (ip):
    conn = http.client.HTTPSConnection("rest.db.ripe.net")
    payload = ''
    headers = {}
    conn.request("GET", "/search.json?bflag=false&dflag=false&rflag=true&query-string="+ip, payload, headers)
    res = conn.getresponse()
    data = res.read()
    logger.debug(ip + " querry result: " + str(res.status))
    
    try: 
        x = json.loads(data.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        logger.error("fatal error: "+str(ip))
        return ip, res.status
    
    intenum_netname = ""
    intenum_descr = ""
    route_netname = ""
    route_route = ""
    route_descr= ""
    route_asn=""
    
   
    for a in x["objects"]["object"]:
        if a["type"] == "inetnum":
            for b in a["attributes"]["attribute"]:
                if b["name"] == "netname":
                    intenum_netname = intenum_netname + " "+ b["value"]
                if b["name"] == "descr":
                    intenum_descr = intenum_descr  +" " +b["value"]
        if a["type"] == "route":
            for b in a["attributes"]["attribute"]:
                if b["name"] == "descr":
                    route_descr =  route_descr +" " + b["value"]
                if b["name"] == "origin":
                    route_asn = route_asn +" "+ b["value"]                    
                if b["name"] == "route": 
                    route_route =route_route +""+ b["value"]

    return ip,res.status,intenum_netname, intenum_descr ,route_route, route_descr,route_asn

def main(argv):

  # make sure command line arguments are valid
  try:
    options, args = getopt.getopt(

       argv, 
      'hv', 
      [ 
        'help',
        'verbose' 
    
      ])
    
    
    
  except getopt.GetoptError:
    logger.fatal("Bad options!")
    help()
    sys.exit(2)


  # handle command line arugments
  for opt, arg in options:
    if opt in ('-h', '--help'):
      Usage()
      sys.exit(2)
    elif opt in ('-v', '--verbose'):
      logger.setLevel(logger.DEBUG) 
 



  logger.info(":O start!")
  ### START here ######

 
  ## Filebeolvasás
  with open("input.txt") as f:
    content = f.readlines()
  ## leszedjük az entert a sorvégéről
  content = [x.strip() for x in content]

  logger.info("thread queue")
  futures = list()
  ## Max workers: 10
  with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
    for a in content:
        future = executor.submit(thread_function, line=a.strip())
        futures.append(future)
        
  ##Egyes 
  ## Kiiratás; thredenként stb
  
  l = csv.writer(open("output.csv", 'w', newline=''))
  ####header.
  l.writerow(["ip","http_status_code","intenum_netname","intenum_descr","route_route","route_descr","route_asn","rdns"])
 
  logger.info("várakozás hogy a threadek sorban elkészüljenek")
  for future in futures:
    
    l.writerow (future.result())
    
    
  logger.info("TheEnd")
  #### END here

if __name__ == "__main__":
  main(sys.argv[1:])
 