import random


class Player:
    """The players that play the noughts and crosses game.

    Attributes:
        symbol: A character string that is either 'X' or 'O'.
        computer: A bool for whether the player should be a computer.
    """

    def __init__(self, symbol: str, computer: bool = False) -> None:
        """Initialises based on symbol and if it is non-player controlled.

        Args:
          symbol: Defines if instance is X or O.
          computer: Defines if instance should be non-player controlled.
        """

        self.symbol = symbol
        self.computer = computer

    def __str__(self) -> str:
        """Returns symbol of player as character."""

        return self.symbol


class Game:
    """The instance of a noughts and crosses game.

    Attributes:
        winning_combinations: All the possible 3-tuples of spaces in grid that
        if all spaces match are a winning combination.
        spaces: A dict that stores the value of each grid space.
        players: a list containing the two player objects.
        playing: a bool used in the main loop if the game is playing.
        turns: a int used to keep track of how many turns have been played,
          used to end game in draw.
    """

    winning_combinations = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),  # Horizontal
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),  # Vertical
        (1, 5, 9),
        (3, 5, 7),  # Diagonal
    ]

    def __init__(self, players: bool):
        """Initialises based on if the 2nd player should be human controlled.

        Args:
          players: a bool that is used to determine if the second player
            is human or computer controlled
        """

        self.spaces = {
            1: "1", 2: "2", 3: "3",
            4: "4", 5: "5", 6: "6",
            7: "7", 8: "8", 9: "9",
        }
        self.players = [Player("X"), Player("O", players)]
        self.turn = random.choice(self.players)
        self.playing = False
        self.turns = 0

    def __str__(self) -> str:
        """Prints grid with values contained within each space.
        
        Returns:
            A string that represents the grid in its current state of play.
        """

        output = []
        for i in range(1, 9, 3):
            output.append(f"{self.spaces[i]} | {self.spaces[i+1]} | {self.spaces[i+2]}")
            if i < 7:
                output.append("\n---------\n")
        return ''.join(output)

    def modify_spaces(self, space: int) -> None:
        """Modifies a space within the grid to be one of the players symbols

        Args:
            space: an integer representing the space to be modified.
        """

        self.spaces[space] = self.turn.symbol

    def modify_turn(self) -> None:
        """Modifies the turn to be the next players (X to O or O to X)."""

        self.turn = next(player for player in self.players if player != self.turn)

    def valid_moves(self) -> list:
        """Returns a list of ints representing the empty spaces in the grid.
        
        Returns:
            A list of ints representing the spaces in the grid that are empty.
        """
        return [i for i in self.spaces.values() if i.isdigit()]

    def play_turn(self) -> None:
        """Plays a turn in the game.
        
        Plays a turn in the game by asking the human players to choose a move
        (or allowing them to quit) and selects a move for the computer
        controlled players. Calls the modify_spaces function with move."""
        while True:
            if self.turn.computer:
                print("The computer makes a move.")
                move = random.choice(self.valid_moves())
                break
            else:
                move = input(
                    f"Player {self.turn}, please select which space (1-9)" +
                     " you want to place your mark (q to quit): "
                )
                if move.lower() == "q":
                    exit()
                elif move in self.valid_moves():
                    break
                else:
                    print("That is not a valid move.")
        self.modify_spaces(int(move))

    def run_game(self) -> None:
        """Runs game of noughts and crosses continuously.
        
        Runs the game continuously while the bool playing is true. 
        Prints the grid and calls the function to allow the current
        players turn to take place as well as changing whose turn it is after
        each move. Also checks for a winner or a draw."""
        self.playing = True

        while self.playing:
            self.turns += 1
            self.modify_turn()
            print(self)

            self.play_turn()

            if self.check_for_win():
                self.display_winner()
            elif self.turns > 8:
                self.display_draw()

    def check_for_win(self) -> bool:
        """Checks if a win has occured.
        
        Uses the list of all possible winning combinations and determines
        if any of these are alln the same, and thus a winner.
        
        Returns:
            a bool which indicates whether there is a win or not.
        """
        for combo in self.winning_combinations:
            if all(self.spaces[pos] == self.turn.symbol for pos in combo):
                return True
        return False

    def display_winner(self) -> None:
        """Displays who has won the game."""
        print(f"Player {self.turn} wins.")
        print(self)
        self.playing = False

    def display_draw(self) -> None:
        """Displays that the game has been drawn (9 turns with no winner)."""
        print("No winner!")
        self.playing = False

"""Initialise game and ask if it should be one player or two."""
if __name__ == "__main__":
    one_player = (
        True
        if input("Do you want to play 1 or 2 player (Enter 1 or 2): ") == "1"
        else False
    )
    game = Game(one_player)
    game.run_game()
