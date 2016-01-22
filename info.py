import shelve

data = shelve.open('argentron_shelf')
#data.clear()
#data.sync()
#print("emptied")

for game in sorted(list(data.keys())):
    print(game + ':')
    for key in sorted(list(data[game].keys())):
        print('\t' + str(key).rjust(16) + ' = ' + str(data[game][key]))

data.close()