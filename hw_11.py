from icmplib import traceroute
import sys


def main():
    messages_count = int(sys.argv[1])
    hostname = sys.argv[2]
    hops = traceroute(hostname, count=messages_count)
    last_distance = 0
    print('Distance/TTL    Address    Average round-trip time')

    for hop in hops:
        if last_distance + 1 != hop.distance:
            print('Some gateways are not responding')
        print(f'{hop.distance}    {hop.address}    {hop.avg_rtt} ms')
        last_distance = hop.distance


if __name__ == '__main__':
    main()
