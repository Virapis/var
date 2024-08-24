import csv
import datetime
import sys
from dateutil.parser import parse as parse_date


def freezercheck(input, allowed):
    output = []
    for entry in input:
        for freezer in allowed:
            if str(freezer) in entry[2]:
                output.append(entry)
    return output


def trim(filename, list, vcutoff=1):
    with open(filename, newline='') as fileinput:
        reader = csv.reader(fileinput)
        if vcutoff == 1:
            trimmedfile = freezercheck(reader, list)
        else:
            trimmedfile = []
            relevant = freezercheck(reader, list)
            for i in relevant:
                if i[3] != '':
                    if float(i[3].split(' ')[0]) >= vcutoff:
                        trimmedfile.append(i)
        fileinput.close()
    return trimmedfile


def agecheck(input):
    date = parse_date(input[1].split(' ')[0]).date()
    today = datetime.date.today()
    diff = today - date
    return diff.days


def relevancecheck(filename, datecutoff, freezers, vcutoff=1):
    input = trim(filename, freezers, vcutoff)
    output = []
    for entry in input:
        if entry[6] == 'Yes- Passed':
            output.append([entry[2], entry[3], entry[4], 'PASSED QC'])
        elif agecheck(entry) >= datecutoff:
            output.append([entry[2], entry[3], entry[4], agecheck(entry)])
    return output


def save(data, name):
    with open(name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sorted(data))
        csvfile.close()


if __name__ == '__main__':
    filename = sys.argv[1]
    agecutoff = int(sys.argv[2])
    freezers = sys.argv[3].split(',')
    vcutoff = int(sys.argv[4])
    outfilename = sys.argv[5]

    out = relevancecheck(filename, agecutoff, freezers, vcutoff)
    save(out, outfilename)
