import math  


setWord = "hello"

my_file = open("wordlist")
all_words = my_file.readlines() # now we can just treat the entire file as a list of strings named all_words
my_file.close()

my_file = open("answerlist")
word_list = my_file.readlines() # now we can just treat the entire file as a list of strings named word_list
my_file.close()

NAnswers = len(word_list) #2309

possible = [] # Initialize to answerlist
guessNumber = 0 # number of words guessed so far. If its 6 and the word isn't guessed then the game ends


#given answer word 1, find the pattern in word 2
def patternMatrix(words2, words1): 
    # find the number 0 to 3^5-1 corresponding to the pattern between two words. base 3: 0 = gray, 1 = yellow, 2 = green

  currentGuess1 = 0 # the number between 0 and 3^5-1 of the current guess
  currentGuess2 = 0
  
  for element in range(5): # iterating through each letter of the input word    
    if words2[element] == words1[element]: # if the letter in input word and answer word are same in same position, set that position to 2
      currentGuess1+=2
      words1 = words1[:element] + '.' + words1[(element+1):] # set the position in the answer word to '.' so that it is not double counted in case the input word has 1 letter twice when the answer word only has it once
      words2 = words2[:element] + ',' + words2[(element+1):]
    currentGuess1 *= 3
    
  for element in range(5): 
    for i in range(5): # iterating through each letter of the answer word
      if words2[element] == words1[i]: # if the letter in the input word is in the answer word, set the position of the letter from the input word to 1 
        currentGuess2+=1
        words1 = words1[:i] + '.' + words1[(i+1):] # set the position in the answer word to '.' so that it is not double counted in case the input word has 1 letter twice when the answer word only has it once
        words2 = words2[:element] + ',' + words2[(element+1):]
        
    currentGuess2*=3 # "sll" but in base 3
  currentGuess = currentGuess1 + currentGuess2
  currentGuess/=3
  return (int)(currentGuess)




def getNextGuess(): 
  # Loop through all 12k possible guesses. For each, loop through currentPossible and compute pattern matrix number for each. If a pattern n is reached, do pattern[n]++. Then, compute entropy using the pattern matrix. Return the highest entropy word.
  global guessNumber
  global possible
  if guessNumber==0:
    return 9490 # salet
  entropyMaxI = 0
  entropyMax = 0
  
  NLeft = len(possible)
  if(NLeft==1):
    return all_words.index(word_list[possible[0]])
  if(NLeft==2):
    return all_words.index(word_list[possible[0]])
  
  for i in range(len(all_words)):
    pattern = [0 for x in range(243)]
    for j in range(NLeft):
      pattern[patternMatrix(all_words[i], word_list[possible[j]])]+=1
      
    entropy = 0
    for j in range(243):
      if(pattern[j]!=0):
        entropy -= pattern[j]*math.log2(pattern[j]/NLeft)/NLeft
    
    if(entropyMax<entropy):
      entropyMaxI = i
      entropyMax = entropy
    if(entropyMax==entropy and (all_words[i] in word_list) and (word_list.index(all_words[i]) in possible)):
      entropyMaxI = i
  return entropyMaxI



def updateCurrentPossible(nextWord, matrixVal): 
  # determine all possible answers at this point. Loop through the current all possible list and then get rid of the inconsistent ones 
  global possible
  i=0
  while(i<len(possible)):
    if patternMatrix(all_words[nextWord], word_list[possible[i]]) != matrixVal:
      possible.pop(i)
      i-=1
    i+=1
  return


def enterPattern(word):
  # ask user to enter BYG and then convert into a number and return it.
  matrixValue = 0

  print("Enter " + word[0] + word[1] +word[2] +word[3] +word[4]+""" for your next guess. Then, type the color pattern you get back, with 5 letters (B, Y, or G).\n""")
  matrix = input();

  for i in matrix:
    if i == 'G':
      matrixValue += 2
    elif i == 'Y':
      matrixValue +=1
    matrixValue *= 3
  matrixValue = (int)(matrixValue/3)
  return matrixValue
  

def main():  
  global possible
  global NAnswers
  global guessNumber
  global setWord
  
  possible = list(range(NAnswers))
  guessNumber = 0
  p = 0
  while(p!=242):
    nextWord = getNextGuess()
    txt = all_words[nextWord].replace('\n', '')
    guessNumber+=1
    print("Guess #" + str(guessNumber) + ": " + txt)
    p = enterPattern(all_words[nextWord])
    updateCurrentPossible(nextWord, p)
    print()
  print("\nHooray.")

main()
