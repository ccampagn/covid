filepath = 'C:\\Users\\chris\\OneDrive\\Documents\\covid.csv'
casedata= {}
with open(filepath, "r") as ifile:
    for line in ifile:
        line=line.split(',')
        date=None
        geoid=None
        case=None
        date=line[0].strip('"')
        geoid=line[3].strip('"')
        cases=line[4].strip('"')
        if date=='2020-08-16' or date=='2020-08-23':
            if geoid not in casedata:
                casedata[geoid]={}
            casedata[str(geoid)][date]=cases
#print(casedata)
with open('geoidcases.csv', 'a') as f:
    f.write('geoid,case')
    f.write('\n')
for geoid in casedata:
    firtcase=0
    #print(geoid)
    if '2020-08-16' in casedata[geoid]:
        firstcase=int(casedata[geoid]['2020-08-16'])
    secondcase=int(casedata[geoid]['2020-08-23'])
    with open('geoidcases.csv', 'a') as f:
        f.write(str(geoid)+","+str(secondcase-firstcase))
        f.write('\n')
