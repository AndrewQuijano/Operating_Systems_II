import re
import itertools


TIMESTAMP = re.compile(r'\d{10}\.\d{6}')
PAYLOAD = re.compile(r'\t0x([\da-fA-F]+):  ([\da-fA-F ]+?)\s{2,}(.*)')


def grouper(iterable, count, fill_value=None):
    args = [iter(iterable)] * count
    return itertools.zip_longest(*args, fillvalue=fill_value)


def convert_tcp_dump_to_text(in_filename, out_filename):
    with open(in_filename) as original:
        with open(out_filename, 'w') as output:
            for line in original:
                print(line)
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


if __name__ == '__main__':
    convert_tcp_dump_to_text('./outside.txt', './outside2.txt')
    # reader('./outside.txt', './outside-temp.txt')

