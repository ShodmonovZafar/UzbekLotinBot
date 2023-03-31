import functions as func

data_ot_soz_turkumi = []

with open("ot.txt") as file:
    ot_str = file.read()

bitta_element = ot_str.split("\n")

for i in bitta_element:
    data_ot_soz_turkumi.append(func.g(i))

with open("topilmaganlar.txt") as file:
    top_str = file.read()

count = func.f1(top_str)