class Solution:
    def __init__(self, board):
        print(board)
        self.board = board

    def __del__(self):
        print("OBS! Deleting solution.")
        """
        while not self.button:
            item = self.button.popitem()
            print("-------------")
            print(item.buttonText)
            item.y = -100
            del item
        del self
        """
solution = Solution("hej")
del solution