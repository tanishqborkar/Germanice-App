with open("gender text files/Masculine Gender.txt", encoding="utf8") as file:
    lines = file.readlines()
with open("gender text files/Feminine Gender.txt", encoding="utf8") as file1:
    linee = file1.readlines()
with open("gender text files/Neutral Gender.txt", encoding="utf8") as file2:
    lineee = file2.readlines()

data = dict()

for line in lines:
    data[line.strip()] = 'Der'

for line1 in linee:
    data[line1.strip()] = 'Die'

for line2 in lineee:
    data[line2.strip()] = 'Das'


def genderGetter():
    return data



