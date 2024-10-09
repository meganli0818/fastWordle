import math  

setWord = "hello"

# Load the wordlists from files
my_file = open("wordlist")
all_words = my_file.readlines() # List of all possible guesses
my_file.close()

my_file = open("answerlist")
word_list = my_file.readlines() # List of all possible answers
my_file.close()

NAnswers = len(word_list) # Total number of possible answers (2309)

possible = [] # Tracks remaining possible answers
guessNumber = 0 # Number of guesses made so far


# Computes the pattern between two words as a base-3 number (0=gray, 1=yellow, 2=green)
def patternMatrix(guess, answer): 
    currentGuess1, currentGuess2 = 0, 0
  
    # First pass: mark green positions and update both words to avoid double counting
    for element in range(5):
        if guess[element] == answer[element]: 
            currentGuess1 += 2
            answer = answer[:element] + '.' + answer[element+1:]
            guess = guess[:element] + ',' + guess[element+1:]
        currentGuess1 *= 3

    # Second pass: mark yellow positions
    for element in range(5):
        for i in range(5):
            if guess[element] == answer[i]:
                currentGuess2 += 1
                answer = answer[:i] + '.' + answer[i+1:]
                guess = guess[:element] + ',' + guess[element+1:]
        currentGuess2 *= 3

    # Combine the two results and return the final pattern number
    currentGuess = (currentGuess1 + currentGuess2) // 3
    return int(currentGuess)


# Finds the next best guess based on entropy calculations
def getNextGuess(): 
    global guessNumber, possible
    
    if guessNumber == 0:
        return 9490 # 'salet' is a common first guess

    entropyMaxI = 0
    entropyMax = 0
    NLeft = len(possible)

    if NLeft <= 2:
        return all_words.index(word_list[possible[0]])

    # Loop through all possible guesses and compute entropy
    for i in range(len(all_words)):
        pattern = [0] * 243
        for j in range(NLeft):
            pattern[patternMatrix(all_words[i], word_list[possible[j]])] += 1
      
        # Calculate entropy for this guess
        entropy = 0
        for count in pattern:
            if count != 0:
                entropy -= count * math.log2(count / NLeft) / NLeft
        
        # Update max entropy guess
        if entropy > entropyMax:
            entropyMaxI = i
            entropyMax = entropy
        elif entropy == entropyMax and all_words[i] in word_list and word_list.index(all_words[i]) in possible:
            entropyMaxI = i
            
    return entropyMaxI


# Updates the list of possible answers based on the pattern result
def updateCurrentPossible(nextWord, matrixVal): 
    global possible
    i = 0
    while i < len(possible):
        if patternMatrix(all_words[nextWord], word_list[possible[i]]) != matrixVal:
            possible.pop(i)
            i -= 1
        i += 1


# Prompts the user to enter the feedback pattern (B=gray, Y=yellow, G=green) and converts it to a matrix value
def enterPattern(word):
    matrixValue = 0
    print(f"Enter {word.strip()} for your next guess. Then, type the color pattern you get back, with 5 letters (B, Y, or G).")
    matrix = input()

    for i in matrix:
        if i == 'G':
            matrixValue += 2
        elif i == 'Y':
            matrixValue += 1
        matrixValue *= 3
    matrixValue = int(matrixValue // 3)
    
    return matrixValue
  

# Main game loop: guesses words until the correct answer is found
def main():  
    global possible, NAnswers, guessNumber, setWord
  
    possible = list(range(NAnswers))  # Start with all possible answers
    guessNumber = 0
    p = 0

    # Loop until the correct answer (all green = 242) is found
    while p != 242:
        nextWord = getNextGuess()
        txt = all_words[nextWord].strip()
        guessNumber += 1
        print(f"Guess #{guessNumber}: {txt}")
        p = enterPattern(all_words[nextWord])
        updateCurrentPossible(nextWord, p)
        print()

    print("\nYou guessed the word!")

main()
