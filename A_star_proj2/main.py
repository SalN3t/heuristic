import sliding_jumping_puzzle as sjp

def main():
    quit  = -1
    while quit < 0:
        print "-"*30 +" Project 1 "+"-"*30
        print "Choose:"
        print "\n\n  \n  1: n = 2 \n  2: n = 4 \n  3: n = 8 \n\n To Quit: \n  4: quit\n\n"
        choice = input('Enter your choise: ')
        if choice == 4:
            quit = 1
        elif choice == 3:
            sjp.main(8,1)
        elif choice == 2:
            sjp.main(4,1)
        elif choice == 1:
            sjp.main(2,1)
if __name__ == '__main__':
    main()
