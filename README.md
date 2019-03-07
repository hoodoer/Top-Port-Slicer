# Top-Port-Slicer
Python script to give you subsets of the nmap "top-ports". For example, I want the 10th to 100th most common TCP ports. Spits out a comma separated list you can copy into -p arg for nmap or masscan

Can also do UDP, but not UDP and TCP at the same time. At the moment. 
Order based on the /usr/share/nmap/nmap-services file, just like nmap's baked in top-ports functionality

Example:
root@kaliboxen:~/dev/portSlicer# ./topPortSlicer.py -range 10-20 -tcp \ 
Starting port rank: 10 \
Ending port rank: 20 \
139,143,53,135,3306,8080,1723,111,995,993,5900



