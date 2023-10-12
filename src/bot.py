import numpy as np

def random_bot() -> str:
    """Make a random action for the block"""
    choice = np.random.randint(3)

    if choice == 0:
        move = "left"
    elif choice == 1:
        move = "right"
    elif choice == 2:
        move = "rotation"

    return move

