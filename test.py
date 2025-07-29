move_leaderboard = []
move_leaderboard.append([0, 2, 3])
move_leaderboard.append([4, 22, 1])
move_leaderboard.append([2, 6, 19])
move_leaderboard.append([10, 1, 5])

move_leaderboard.sort(reverse=True, key = lambda a: a[0])
print(move_leaderboard)