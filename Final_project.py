'''
CCNY 2019 Spring CSC113
Final project
Group menber: Qing Lan, Bryan Arevalo, Angel Baez
'''

import turtle, math, random
from tkinter import *
from itertools import cycle

#read_file() opens the Words.txt text file as a readable, and extracts the occurrences
#of characters. returns a dictionary containing the count of each letter, symbol, and space.
def read_file() :
  #open the txt file
  f = open('Words.txt','r')
  readContent = f.readlines()
  letterdic = {}
  spacedic = {}
  symboldic = {}
  letterdic['space'] = 0
  letterdic['symbol'] = 0
  
  #iterate the file contents
  #depending on the unicode value, A-Z a-z are normal letters, while symbols and white space
  #are put into a separate dictionary and placed into the letter dictionary at the end
  for n in readContent:
    for letter in n:
      unival = ord(letter)
      if unival >= 65 and unival <= 122 :
        CountLetter = n.count(letter)
        letterdic[letter] = CountLetter
      elif unival == 32 or unival == 9 or unival == 10 : 
        CountLetter = n.count(letter)
        spacedic[letter] = CountLetter
      else:
        CountLetter = n.count(letter)
        symboldic[letter] = CountLetter

  #combines all forms of white space into one 'space' entry in letterdic     
  for space, count in spacedic.items():
      letterdic['space'] = letterdic['space'] + count
      
  #combines all forms of symbols into one 'symbol' entry in letterdic
  for symbol, count in symboldic.items():
      letterdic['symbol'] = letterdic['symbol'] + count

  #closes the file and returns the letterdic
  f.close()
  return letterdic

def calculate_frequency(letterdic) :
  #probability_list will contain the probability of each letter, and be in reversely
  #sorted order when returned
  probability_list = []
  
  #find the sum of Frequencies of all Letters
  sumFrequencyofAllLetters = 0
  for letter,CountLetter in letterdic.items():
     sumFrequencyofAllLetters = sumFrequencyofAllLetters + CountLetter
     
  #find the probability of each letter and add them to probability_list
  for letter,Countletter in letterdic.items():
    probabilityofLetter = letterdic[letter]/int(sumFrequencyofAllLetters)
    probability_list.append(probabilityofLetter)

  #reversely sort probability_list and return it
  probability_list.sort(reverse = True)
  return probability_list

def pie_draw(probability_list, most_frequent_chars, count) :
  
  #draw pie chart
  tempCount = int(count)
  totalProb = 1
  radius = 175
  tess = turtle.RawTurtle(canvas)
  tess.penup()
  tess.sety(-radius)
  tess.pendown()
  tess.speed(7)
  
  #display n pie regions using random rgb values
  #colors will be distinct, the probability of a color repeating is extremely low
  for i in range(tempCount) :
    totalProb = totalProb - probability_list[i]
    Red = random.random()
    Green = random.random()
    Blue = random.random()
    tess.fillcolor(Red,Green,Blue)
    tess.begin_fill()
    tess.circle(radius, 360*probability_list[i])
    position = tess.position()
    tess.goto(0,0)
    tess.end_fill()
    tess.setposition(position)
    
  #displays the last pie region if the user entered less than the total number of entries
  #in the dictionary  
  if len(probability_list) != int(count):
    #display the last pie region
    Red = random.random()
    Green = random.random()
    Blue = random.random()
    tess.fillcolor(Red,Green,Blue)
    tess.begin_fill()
    tess.circle(radius, 360 * totalProb)
    tess.goto(0,0)
    tess.end_fill()
  
  #add labels along the edge of the pie chart
  #label is the character itself and its frequency
  tess.penup()
  labelRadius = radius * 1.3
  tess.sety(-labelRadius)
  tempCount = int(count)
  for i in range(tempCount) :
      label_string = most_frequent_chars[i] + ', ' + str("%.4f" % probability_list[i])
      tess.circle(labelRadius, 360*probability_list[i]/2)
      tess.write(label_string, align="center",  font=("Arial", 6, "normal"))
      tess.circle(labelRadius, 360*probability_list[i]/2)

  #again, label the last pie region only if the user did not enter the max number
  #of regions
  if len(probability_list) != int(count):
    label_string = 'Other chars, ' + str("%.4f" % totalProb)
    tess.circle(labelRadius, 360*totalProb/2)
    tess.write(label_string, align="center",  font=("Arial", 6, "normal"))
    tess.circle(labelRadius, 360*totalProb/2)

#handles the "Enter" button press, validates user input and extracts from the file and draws the pie chart      
def entry_pressed() :
  #deletes label in row 1 column 0, usually the error display message
  for component in main_window.grid_slaves():
      if int(component.grid_info()['row']) == 1 and int(component.grid_info()['column']) == 0 :
          component.grid_forget()

  #validates user input, catches errors and displays a message if the user inputs an invalid entry
  try:
    number_frequent = int(letter_entry.get())
    if number_frequent <= 0 or number_frequent > 54 :
        Label(main_window, text = 'You must enter a valid number', font=("Arial", 12, "bold")).grid(row = 1, column = 0)
        return

    #gets the letter dictionary, the probability list, and draws the pie chart
    #also reversely sorts the letter dictionary so that the probabilities and dictionary keys can be aligned
    letterdic = read_file()
    probability_list = calculate_frequency(letterdic)
    most_frequent_chars = sorted(letterdic, key=letterdic.get, reverse = True)

    #empties the pie chart canvas so the pie chart can be redrawn
    canvas.delete("all")

    #makes sure that if the user inputs 54 but there aren't enough entries, changes the value to maximum entry number
    if number_frequent > len(letterdic) :
        number_frequent = len(letterdic)

    #draws the pie chart and displays a label for convenience
    Label(main_window, text = 'Displaying ' + str(number_frequent) + ' Most Frequent Characters' , font=("Arial", 12, "bold")).grid(row = 1, column = 0)
    pie_draw(probability_list, most_frequent_chars, number_frequent)
  except:
      #display a label telling the user to input a correct value if ANY error occurs in the try block
      Label(main_window, text = 'You must enter a valid number', font=("Arial", 12, "bold")).grid(row = 1, column = 0)
  
#creates the main window for the GUI, an enter and exi button, an entry box for user input, and a canvas for the pie chart
#program will continue to run until the exit button or the window is closed
main_window = Tk(className = "letter frequency")
Label(main_window, text = 'Enter a number less than or equal to 54').grid(row = 0)
letter_entry = Entry(main_window)
letter_entry.grid(row = 0, column = 1)
entry_button = Button(main_window, text = "Enter", width = 20, command = entry_pressed)
entry_button.grid(row = 1, column = 1)
canvas = Canvas(main_window, width = 600, height = 500)
canvas.grid(row = 2, column = 0)
exit_button = Button(main_window, text = "Exit", width = 20, command = exit)
exit_button.grid(row = 2, column = 1)
main_window.mainloop()



