import sys
import socket
import os
import json


if len(sys.argv) == 3:
    address = sys.argv[1]
    port = int(sys.argv[2])
elif len(sys.argv) == 2:
    address = sys.argv[1]
    port = 11211
else:
    address = '127.0.0.1'
    port = 11211


def get_stats(address, port):
    timeout = 2
    s = socket.create_connection((address, port), timeout)
    s.send('stats\r\n')
    ret = s.recv(2046)
    stats = {}
    for line in ret.split('\r\n'):
        slabs = line.split()
        if len(slabs) != 3:
            continue
        [_, stats_name, stats_value] = slabs
        stats[stats_name] = stats_value

    return stats


def load_stats():
    file_name = 'stats.txt'
    if not os.path.exists(file_name):
        return {}
    else:
        with file(file_name) as stats:
            ret = json.loads(stats.read())
    return ret


def save_stats(new_stats):
    file_name = 'stats.txt'
    with file(file_name, 'w') as stats:
        stats.write(json.dumps(new_stats))

new_stats = get_stats(address, port)
old_stats = load_stats()

new = int(new_stats['evictions'])
old = int(old_stats.get('evictions', 0))
delta = new - old
formatter = "evictions %(new)s > %(old)s evictions_grow_up_about:%(delta)s"
print formatter % {'new': new, 'old': old, 'delta': delta}

save_stats(new_stats)
