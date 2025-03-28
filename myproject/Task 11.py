# Task 1

with open("File.txt", 'w') as file:
    for i in range(1, 1001):
        file.write(f"Line {i}\n")

with open("File.txt", 'r') as file:
    print(f"Filled Lines: {len(file.readlines())}")


# Task 2

dict_ = {
    2: "Two",
    8: "Eight",
    10: "Ten",
    13: "Thirteen",
    17: "Seventeen"
}

with open("File2.txt", "w") as file2:
    for i in range(1, 20):
        if i in dict_:
            print(dict_[i])
        else:
            print("\n")


# Task 3

with open("File3.txt", "w+") as file3:
    file3.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n"
                "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,\n"
                "when an unknown printer took a galley of type and scrambled it to make a type specimen book.")
    file3.seek(0)
    file_1 = file3.read()

with open("File4.txt", "w+") as file4:
    file4.write("\nContrary to popular belief, Lorem Ipsum is not simply random text.\n"
                "It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old.\n"
                "Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia,\n"
                "looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage,\n"
                "and going through the cites of the word in classical literature, discovered the undoubtable source.")
    file4.seek(0)
    file_2 = file4.read()

with open("Merged.txt", "w+") as merged:
    merged.write(file_1 + "\n" + file_2)
    merged.seek(0)
    print(merged.read())


# Task 4

with open("Palindrom.txt", "w") as f:
    f.write("moon\n"
            "noon\n"
            "letter\n"
            "mood\n"
            "aiia\n"
            "lool\n")

def is_palindrom(x):
    return x == x[::-1]

def is_palindrom_final(x):
    with open(x, "r") as polindrom:
        for i in polindrom:
            if is_palindrom(i.strip()):
                print(i.strip())

is_palindrom_final("Palindrom.txt")


# Task 5

def split(x):
    with open(x, "r") as fi:
        lines = fi.readlines()

    count = 0

    for i in range(0, len(lines), 10):
        with open(f"split_file_{count}.txt", "w") as new_file:
            new_file.writelines(lines[i:i+10])
        count += 1

split("File.txt")

with open("split_file_0.txt", "r") as f:
    print(f.read())


# Task 6

def changing(x, y):
    with open(x, "r") as first:
        lines = first.readlines()

    output = []

    for i in lines:
        if i.strip() != "":
            output.append(i)

    with open(y, "w") as fo:
        fo.writelines(output)

with open("first.txt", "w") as f:
    f.write("dog\n"
            "\n"
            "cat\n"
            "\n"
            "\n"
            "cow")

changing("first.txt", "Palindrom.txt")

with open("Palindrom.txt", "r") as f:
    print(f.read())
