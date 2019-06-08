import nmap
import optparse


def nmap_scan(target_ip, target_port):
    scan = nmap.PortScanner(target_ip, target_port)
    scan.scan(target_ip, target_port)
    state = scan[target_ip]['tcp'][int(target_port)]['state']
    print(target_ip + " tcp: " +target_port + " " + state)


def main():
    parser = optparse.OptionParser('usage%prog ' + '-H <target-host> -p <target-port')
    parser.add_option('-H', dest='target_ip', type='string', help='specify target host')
    parser.add_option('-p', dest='target_ports', type='string', help='specify target port[s} separated by commas')
    (options, args) = parser.parse_args()
    target_ip = options.target_host
    target_ports = str(options.target_port).split(', ')

    if target_ip is None or target_ports[0] is None:
        print(parser.usage)
        exit(0)

    for port in target_ports:
        nmap_scan(target_ip, port)


if __name__ == 'main':
    main()
