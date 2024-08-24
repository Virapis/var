import csv
import datetime
import sys
from dateutil.parser import parse as parse_date


def freezercheck(input, allowed):
    output = []
    for entry in input:
        for freezer in allowed:
            if str(freezer) in entry['Location path']:
                output.append(entry)
    return output


def trim(filename, list, vcutoff=1):
    with open(filename, newline='') as fileinput:
        reader = csv.DictReader(fileinput)
        if vcutoff == 1:
            trimmedfile = freezercheck(reader, list)
        else:
            trimmedfile = []
            relevant = freezercheck(reader, list)
            for i in relevant:
                if i['Quantity'] != '':
                    if float(i['Quantity'].split(' ')[0]) >= vcutoff:
                        trimmedfile.append(i)
        fileinput.close()
    return trimmedfile


def agecheck(input):
    date = parse_date(input['Created (UTC)'].split(' ')[0]).date()
    today = datetime.date.today()
    diff = today - date
    return diff.days


def relevancecheck(filename, datecutoff, freezers, vcutoff=1):
    input = trim(filename, freezers, vcutoff)
    output = []
    for entry in input:
        if entry['Qualified by R&D Qualification?'] == 'Yes- Passed':
            output.append([entry['Location path'],
                           entry['Name'],
                           entry['LN or NB reference'],
                           'PASSED QC'
                           ])
        elif agecheck(entry) >= datecutoff:
            output.append([entry['Location path'],
                           entry['Name'],
                           entry['LN or NB reference'],
                           agecheck(entry)
                           ])
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
