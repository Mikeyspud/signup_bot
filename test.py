from operation import squad, main

if __name__ == "__main__":

    operation = main.Operation(name="Never Die")
    squadA = operation.create_squad("alpha")
    squadB = operation.create_squad("bravo")
#    squadC = operation.create_squad("alpha")

    squadA.sl = "Michael"
    squadB.sl = "Bob"

    print(operation)
