import MC as mc
import graph as gr

def main():
    quit  = -1
    while quit < 0:
        print "-"*30 +" Project 1 "+"-"*30
       # print "Choose:"
        print "\n\n For a: \n  1: Graph Figure 7.16 in [GT] page 364 \n Default values (from = 'BWI', to = ['SFO','LAX']) \n\n For b: \n  2: MC with (3,2) \n  3: MC with (4,3) \n\n To Quit: \n  4: quit\n\n"
        choice = input('Enter your choise: ')
        if choice == 4:
            quit = 1
        elif choice == 3:
            mc.main(4,3)
        elif choice == 2:
            mc.main(3,2)
        elif choice == 1:
            gr.main()
if __name__ == '__main__':
    main()
