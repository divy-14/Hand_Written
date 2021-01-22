raw_text = "Hello my name is Chintu \n \n \n what the fuck is going on a"
lines = raw_text.split("\n")  # splitting text on the basis of new line

for line in lines:
    print(line, end="")


def func():
    print("hellew")
    pass


# IF WE WRITE A FUNC WITHOUT BRACJETS IT DOES NOT DO ANYTHING
func
