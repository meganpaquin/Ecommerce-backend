from data import me

print(me["hobbies"])
print(me['color'])

#modify
me["color"] = "purple"
print(me["color"])

#add
me["age"] = 28
print(me["age"])

holder = me["address"]
print(holder["street"] + ", " + str(holder["number"]) + " " + holder["city"])