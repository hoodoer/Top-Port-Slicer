# Top-Port-Slicer
Python script to give you subsets of the nmap "top-ports". For example, I want the 10th to 100th most common TCP ports. Why would you want to skip the first 10 ports in this example? Because you already scanned them :) \
 \
Useful on external network assessments when you have a lot of scanning to do. \
 \
It spits out a comma separated list you can copy into -p arg for nmap or masscan \
 \
Can also do UDP, but not UDP and TCP at the same time.
Order based on the /usr/share/nmap/nmap-services file, just like nmap's baked in top-ports functionality \
 \
Example: \
root@kaliboxen:/root/dev/portSlicer# ./topPortSlicer.py \-range 10\-20 -tcp \
Top 10 to 20 TCP services: \
139,143,53,135,3306,8080,1723,111,995,993,5900 


The optional '\-setEnvVar' parameter takes an environmental variable name. When this option is used, a new bash instance is created with the ports set to the provided environmental variable name. You can then use:
nmap \-p $ENVVARIABLENAME

This allows you to avoid the copy pasta. Note that this is a new bash instance, so after you run nmap, you probably want to call exit to get back to your original bash context. 

For example: \
root@kaliboxen:/root/dev/Top-Port-Slicer# ./topPortSlicer.py \-range 5\-10 -udp \-setEnvVar PORTS2SCAN \
Top 5 to 10 UDP services: \
138,1434,445,135,67,53 \
Ports exported to environmental variable: PORTS2SCAN \
Use with nmap, etc, like: nmap \-p $PORTS2SCAN \
 \
root@kaliboxen:/root/dev/Top\-Port\-Slicer# nmap \-sUV \-p $PORTS2SCAN localhost \
Starting Nmap 7.70SVN ( https://nmap.org ) at 2019-03-08 14:44 EST \
Nmap scan report for localhost (127.0.0.1) \
Host is up (0.000031s latency). \
Other addresses for localhost (not scanned): ::1 \
 \
PORT     STATE  SERVICE      VERSION \
53/udp   closed domain \
67/udp   closed dhcps \
135/udp  closed msrpc \
138/udp  closed netbios\-dgm \
445/udp  closed microsoft\-ds \
1434/udp closed ms\-sql\-m \
 \
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ . \
Nmap done: 1 IP address (1 host up) scanned in 0.64 seconds \
root@kaliboxen:/root/dev/Top\-Port\-Slicer# exit \
exit \
root@kaliboxen:/root/dev/Top\-Port\-Slicer#  
