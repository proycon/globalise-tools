#!/usr/bin/env python3
import csv
from itertools import chain

import tabulate
from pagexml.parser import parse_pagexml_file

data_dir = '/Users/bram/workspaces/globalise/globalise-tools/data'
headers = ["url", "n", "line n", "join?", "line n+1", "below/next", "roi n", "roi n+1"]

files = [
    '199/NL-HaNA_1.04.02_1297_0019.xml',
    '199/NL-HaNA_1.04.02_1297_0020.xml',
    '199/NL-HaNA_1.04.02_1297_0021.xml',
    '199/NL-HaNA_1.04.02_1297_0022.xml',
    '199/NL-HaNA_1.04.02_1297_0023.xml',
    '199/NL-HaNA_1.04.02_1297_0024.xml',
    '199/NL-HaNA_1.04.02_1297_0025.xml',
    '199/NL-HaNA_1.04.02_1297_0026.xml',
    '199/NL-HaNA_1.04.02_1297_0027.xml',
    '199/NL-HaNA_1.04.02_1297_0028.xml',
    '199/NL-HaNA_1.04.02_1297_0029.xml',
    '199/NL-HaNA_1.04.02_1297_0030.xml',
    '199/NL-HaNA_1.04.02_1297_0031.xml',
    '199/NL-HaNA_1.04.02_1297_0032.xml',
    '199/NL-HaNA_1.04.02_1297_0033.xml',
    '199/NL-HaNA_1.04.02_1297_0034.xml',
    '199/NL-HaNA_1.04.02_1297_0035.xml',
    '199/NL-HaNA_1.04.02_1297_0036.xml',
    '199/NL-HaNA_1.04.02_1297_0037.xml',
    '199/NL-HaNA_1.04.02_1297_0038.xml',
    '199/NL-HaNA_1.04.02_1297_0039.xml',
    '199/NL-HaNA_1.04.02_1297_0040.xml',
    '199/NL-HaNA_1.04.02_1297_0041.xml',
    '199/NL-HaNA_1.04.02_1297_0042.xml',
    '199/NL-HaNA_1.04.02_1297_0043.xml',
    '199/NL-HaNA_1.04.02_1297_0044.xml',
    '199/NL-HaNA_1.04.02_1297_0045.xml',
    '199/NL-HaNA_1.04.02_1297_0046.xml',
    '199/NL-HaNA_1.04.02_1297_0047.xml',
    '199/NL-HaNA_1.04.02_1297_0048.xml',
    '199/NL-HaNA_1.04.02_1297_0049.xml',
    '199/NL-HaNA_1.04.02_1297_0050.xml',
    '199/NL-HaNA_1.04.02_1297_0051.xml',
    '199/NL-HaNA_1.04.02_1297_0052.xml',
    '199/NL-HaNA_1.04.02_1297_0053.xml',
    '199/NL-HaNA_1.04.02_1297_0054.xml',
    '199/NL-HaNA_1.04.02_1297_0055.xml',
    '199/NL-HaNA_1.04.02_1297_0056.xml',
    '199/NL-HaNA_1.04.02_1297_0057.xml',
    '316_1/NL-HaNA_1.04.02_1589_0019.xml',
    '316_1/NL-HaNA_1.04.02_1589_0020.xml',
    '316_1/NL-HaNA_1.04.02_1589_0021.xml',
    '316_2/NL-HaNA_1.04.02_1589_0048.xml',
    '316_2/NL-HaNA_1.04.02_1589_0049.xml',
    '316_3/NL-HaNA_1.04.02_1589_0052.xml',
    '316_3/NL-HaNA_1.04.02_1589_0053.xml',
    '316_3/NL-HaNA_1.04.02_1589_0054.xml',
    '316_3/NL-HaNA_1.04.02_1589_0055.xml',
    '316_3/NL-HaNA_1.04.02_1589_0056.xml',
    '405/NL-HaNA_1.04.02_1859_0115.xml',
    '405/NL-HaNA_1.04.02_1859_0116.xml',
    '405/NL-HaNA_1.04.02_1859_0117.xml',
    '405/NL-HaNA_1.04.02_1859_0118.xml',
    '405/NL-HaNA_1.04.02_1859_0119.xml',
    '405/NL-HaNA_1.04.02_1859_0120.xml',
    '405/NL-HaNA_1.04.02_1859_0121.xml',
    '405/NL-HaNA_1.04.02_1859_0122.xml',
    '405/NL-HaNA_1.04.02_1859_0123.xml',
    '405/NL-HaNA_1.04.02_1859_0124.xml',
    '405/NL-HaNA_1.04.02_1859_0125.xml',
    '405/NL-HaNA_1.04.02_1859_0126.xml',
    '405/NL-HaNA_1.04.02_1859_0127.xml',
    '405/NL-HaNA_1.04.02_1859_0128.xml',
    '405/NL-HaNA_1.04.02_1859_0129.xml',
    '405/NL-HaNA_1.04.02_1859_0130.xml',
    '405/NL-HaNA_1.04.02_1859_0131.xml',
    '405/NL-HaNA_1.04.02_1859_0132.xml',
    '405/NL-HaNA_1.04.02_1859_0133.xml',
    '405/NL-HaNA_1.04.02_1859_0134.xml',
    '405/NL-HaNA_1.04.02_1859_0135.xml',
    '43/NL-HaNA_1.04.02_1092_0017.xml',
    '43/NL-HaNA_1.04.02_1092_0018.xml',
    '43/NL-HaNA_1.04.02_1092_0019.xml',
    '43/NL-HaNA_1.04.02_1092_0020.xml',
    '43/NL-HaNA_1.04.02_1092_0021.xml',
    '685_1/NL-HaNA_1.04.02_7573_0077.xml',
    '685_1/NL-HaNA_1.04.02_7573_0078.xml',
    '685_2/NL-HaNA_1.04.02_7573_0183.xml',
    '685_2/NL-HaNA_1.04.02_7573_0184.xml',
    '685_2/NL-HaNA_1.04.02_7573_0185.xml',
    '685_2/NL-HaNA_1.04.02_7573_0186.xml',
    '685_2/NL-HaNA_1.04.02_7573_0187.xml',
    '685_2/NL-HaNA_1.04.02_7573_0188.xml',
    '685_2/NL-HaNA_1.04.02_7573_0189.xml',
    '685_2/NL-HaNA_1.04.02_7573_0190.xml',
]


def as_file_lines(filename):
    path = f"{data_dir}/{filename}"
    scan_doc = parse_pagexml_file(path)
    lines = scan_doc.get_lines()
    return [(filename, line) for line in lines]


def as_rows(filename):
    url = na_url(filename)
    path = f"{data_dir}/{filename}"
    scan_doc = parse_pagexml_file(path)
    lines = scan_doc.get_lines()
    rows = []
    for i, line in enumerate(lines[:-1]):
        if i < len(lines) - 1:
            next_line = lines[i + 1]
            bn = ""
            if next_line.is_below(line):
                bn += "b"
            if line.is_next_to(next_line):
                bn += "n"
            roi_n = line.metadata['reading_order']['index']
            roi_n1 = next_line.metadata['reading_order']['index']
            row = [url, i, line.text, "", next_line.text, bn, roi_n, roi_n1]
            rows.append(row)
    return rows


def to_rows(file_lines):
    rows = []
    for i, file_line in enumerate(file_lines[:-1]):
        url = na_url(file_line[0])
        line = file_line[1]
        next_line = file_lines[i + 1][1]
        bn = ""
        if next_line.is_below(line):
            bn += "b"
        if line.is_next_to(next_line):
            bn += "n"
        roi_n = line.metadata['reading_order']['index']
        roi_n1 = next_line.metadata['reading_order']['index']
        row = [url, i, line.text, "", next_line.text, bn, roi_n, roi_n1]
        rows.append(row)
    return rows


def write_to_csv(csv_path, data):
    with open(csv_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f, dialect='excel', delimiter=",")
        writer.writerow(headers)
        writer.writerows(data)


def write_to_xlsx(xlsx, data):
    pass


def na_url(file_path):
    file_name = file_path.split('/')[1]
    inv_nr = file_name.split('_')[2]
    file = file_name.replace('.xml', '')
    return f"https://www.nationaalarchief.nl/onderzoeken/archief/1.04.02/invnr/{inv_nr}/file/{file}"


def main():
    lines_per_file = [as_file_lines(file) for file in files]
    file_lines = list(chain(*lines_per_file))
    data = to_rows(file_lines)

    table = tabulate.tabulate(
        data,
        tablefmt='github',
        headers=headers,
        colalign=["left", "right", "right", "left", "center", "center", "center", "center"]
    )
    # print(table)

    write_to_csv('out.csv', data)
    write_to_xlsx('globalise-word-joins.csv', data)


if __name__ == '__main__':
    main()
