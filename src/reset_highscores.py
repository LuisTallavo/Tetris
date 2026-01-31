"""
Utility script to reset all high scores in Avalanche.
Run this to clear the highscore file and start fresh.
"""

def reset_highscores():
    with open("Highscores.txt", "w") as f:
        for _ in range(5):
            f.write("---\n")
        for _ in range(5):
            f.write("0\n")
    print("High scores have been reset!")

if __name__ == "__main__":
    reset_highscores()
