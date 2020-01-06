#!/usr/bin/python3

# Script to let you slice and dice nmap "top-ports"
# so you can more intelligentily scan in batches,
# i.e. scan top 10 ports, then scan top 11-50 ports, etc
# This script will give you port numbers to feed
# nmap/masscan to hit those later ranges
#
# Drew Kirkpatrick
# drew.kirkpatrick@gmail.com
# @hoodoer


import argparse
import sys
import time
import os



# The list of "top ports" is used from nmap. 
# Change this if your nmap files are located elsewheres
NMAPSERVICEFILE = "/usr/share/nmap/nmap-services"






if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-range", "-r", help="the range of 'top-ports' to generate, START_PORT_RANK-END_PORT_RANK")
	parser.add_argument("-tcp", "-t", action='store_true', help="output top TCP ports (can't use at same time as UDP)")
	parser.add_argument("-udp", "-u", action='store_true', help="output top UDP ports (can't use at the same time as TCP)")
	parser.add_argument("-setEnvVar", "-s", default="NULL", help="(OPTIONAL) export the ports to the provided environment variable name (i.e. pass to nmap with -p $ENVVAR)")

	args = parser.parse_args()

	# If we have less than 4, something is amiss
	if len(sys.argv) < 4:
		parser.print_help()
		sys.exit()


	# Can't have both
	if args.tcp and args.udp:
		print ("Error: TCP and UDP are both set, this script can only handle one at a time. \n")
		parser.print_help()
		sys.exit()


	# Must have one
	if not args.tcp and not args.udp:
		print ("Error: Neither TCP or UDP are set, you must have one. \n")
		parser.print_help()
		sys.exit()



	rankRange = args.range

	ports = rankRange.split('-')
	startRank = int(ports[0])
	endRank   = int(ports[1])

	if startRank >= endRank:
		print ("The starting port rank was not less than the ending port rank, reduce the derp and try again.")
		sys.exit()

	if endRank > 3000:
		print ("Getting desperate are we?")
		time.sleep(1)

	# Ok, let's get our super nice list of top services from nmap. Gosh darn bless those folks
	protocolLines = []
	sortedLines = []
	subsetList = []

	# Read the services
	for line in open(NMAPSERVICEFILE, 'r'):

		# Strip the comment lines
		if line.startswith('#'):
			continue

		# If we're looking for TCP services...
		if args.tcp:
			if "/tcp" in line:
				protocolLines.append(line)

		# If we're looking for UDP services...
		if args.udp:
			if "/udp" in line:
				protocolLines.append(line)

	# Sort by open-frequency column
	for line in sorted(protocolLines, key=lambda line: line.split()[2], reverse=True):
		sortedLines.append(line)

	
	index = startRank-1
	while index < endRank:
		subsetList.append(sortedLines[index])
		index += 1

	portString = ""
	for line in subsetList:
		service = line.split("\t")
		port = service[1].split("/")
		portString += port[0]
		portString += ","

	# Remove that trailing comma so you appear less moronic
	portString = portString[:-1]
	


	# Ouput our ports to scan
	if args.tcp:
		print ("Top " + str(startRank) + " to " + str(endRank) + " TCP services:")
	elif args.udp:
		print ("Top " + str(startRank) + " to " + str(endRank) + " UDP services:")
	
	# For the copy pasta crowd
	print (portString)


	# Check if we need to export and environmental variable
	if args.setEnvVar != "NULL":
		print ("Ports exported to environmental variable: " + args.setEnvVar)
		print ("Use with nmap, etc, like: nmap -p $" + args.setEnvVar)
		print ("Type 'exit' after running nmap to return to your original bash context")
		os.putenv(args.setEnvVar, portString)
		os.system('bash')

