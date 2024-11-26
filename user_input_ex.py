import plumbum.cli.terminal as terminal
# see also ask and prompt
choice = terminal.choose("favorite color?", ['red', 'green', 'blue'], default='blue')

colors = {'red' : 1, 'green' : 2, 'blue' : 3}
print("you chose: ")
print(choice)