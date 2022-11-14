# Not in final build -> just for testing
def main():
    name = input("Enter name of file")


    with open(name, "r") as readFile:
        Lines = [l.strip() for l in readFile.readlines()]


    


if __name__ == "__main__":
    main()