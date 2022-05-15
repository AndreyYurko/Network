import argparse
from random import randint

import numpy as np

routers = dict()
ips = []
links = []


class Table:
    def __init__(self):
        self.dists = dict()
        self.next = dict()


class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbours = []
        self.table = Table()

    def make_link(self, ip):
        self.neighbours.append(ip)
        self.table.dists[ip] = 1
        self.table.next[ip] = ip

    def inf_init(self):
        for ip in ips:
            self.table.dists[ip] = np.inf
            self.table.next[ip] = 'None'
        self.table.dists[self.ip] = 0
        self.table.next[self.ip] = 0

    def update_neighbours_tables(self):
        for ip in self.neighbours:
            routers[ip].update_table(self.ip, self.table)

    def update_table(self, owner, table):
        for ip in ips:
            if table.dists[ip] + self.table.dists[owner] < self.table.dists[ip]:
                self.table.dists[ip] = table.dists[ip] + self.table.dists[owner]
                self.table.next[ip] = self.table.next[owner]

    def print_table(self, step):
        if step == -1:
            message = "Final state " + f'of router {self.ip} table:'
        else:
            message = "Simulation step " + str(step) + f' of router {self.ip} table:'
        print(message)
        print('Source IP            Destination IP       Next Hop         Metric')
        for ip in ips:
            if ip != self.ip and not np.isinf(self.table.dists[ip]):
                message = "{:21s}".format(self.ip) + "{:21s}".format(ip) \
                          + "{:21s}".format(self.table.next[ip]) + "{:2d}".format(self.table.dists[ip])
                print(message)
        print('')


def generate_ip():
    return str(randint(0, 255)) + '.' + str(randint(0, 255)) + '.' + str(randint(0, 255)) + '.' + str(randint(0, 255))


def generate_link(n):
    i1 = randint(0, n - 1)
    i2 = randint(0, n - 1)
    while i1 == i2:
        i1 = randint(0, n - 1)
        i2 = randint(0, n - 1)
    return ips[i1], ips[i2]


def main():
    n = randint(2, 15)

    for i in range(n):
        ip = generate_ip()
        while ip in ips:
            ip = generate_ip()
        ips.append(ip)
        routers[ip] = Router(ip)

    for ip in ips:
        routers[ip].inf_init()

    m = randint(1, n * (n - 1) // 2)
    for i in range(m):
        ip1, ip2 = generate_link(n)
        while (ip1, ip2) in links:
            ip1, ip2 = generate_link(n)
        links.append((ip1, ip2))
        routers[ip1].make_link(ip2)
        routers[ip2].make_link(ip1)

    for step in range(1, n+1):
        for ip in ips:
            routers[ip].update_neighbours_tables()
        for ip in ips:
            routers[ip].print_table(step)
    for ip in ips:
        routers[ip].print_table(-1)


if __name__ == '__main__':
    main()
