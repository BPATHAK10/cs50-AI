from nim import train, play

ai = train(10000)

#loop to keep playing until user says no
keepPlay = True
while keepPlay:
    play(ai)
    ans = input("Wanna play again? y/n::")
    if ans == "n":
        keepPlay = False
