import re
import itertools


TIMESTAMP = re.compile(r'\d{10}\.\d{6}')
PAYLOAD = re.compile(r'\t0x([\da-fA-F]+):  ([\da-fA-F ]+?)\s{2,}(.*)')


def grouper(iterable, count, fillvalue=None):
    args = [iter(iterable)] * count
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def convert_tcpdump_to_text2pcap(in_filename, out_filename):
    with open(in_filename) as input, open(out_filename, 'w') as output:
        for line in input:
            time = TIMESTAMP.match(line)
            if time:
                output.write('{}\n'.format(time.group()))
                continue
            payload = PAYLOAD.match(line)
            if payload:
                address = payload.group(1)
                hex_data = payload.group(2).replace(' ', '')
                ascii_data = payload.group(3)

                hex_data = ' '.join(''.join(part) for part in grouper(hex_data, 2, ' '))
                output.write('\t{:0>6}:  {:<47}  {}\n'.format(address, hex_data, ascii_data))


#if __name__ == '__main__':
#    convert_tcpdump_to_text2pcap('../Traffic/traffic1.txt', '../Traffic/txt2.txt')