import operation

if __name__ == "__main__":

    op = operation.Operation()

    op.create_squad("alpha")
    squad = op.squads["alpha"]
    squad.set_comp({"HA": 0})
    squad.add("me", "HB")
