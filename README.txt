Matching Numbers

Regler:
1) At start 9x4-1 st random siffror (mellan 1 och 9)
2) Om summan av adjucent siffror är 10 eller två samma siffror spelaren kan trycka på de och de bli gråa

Gråa siffror:
Rälknas inte in till "adjucent siffror, t.ex 2 grå(3) 8, 2 och 8 räknas som adjucent, trots att en grå 3:a finns mellan

Adjacent siffror:
horsontellt, vertikalt eller diagonalt.
speciall regel => horsontellt till förra rad vid kanten räknas med

3) Make it so that if entire row is gray its removed
4) score: 
    [x]  +1 points for connecting a pair of numbers
    [x]  Crossing out all the numbers on the field (+150 points)
    [x]  Removing a row (+10 points) - done
    [ ]  Score +4 points by connecting numbers that are far apart (instead of +1).
5) Can use "+" up to 4 times. Game Over when no more "+" and no more legal moves.
6) Bar indicating what numbers exist on the board. (ex. if all 9 grayed out => make 9 gray on the bar)

Solving AI:
1) Make list of all possible moves
2) Make it so that you can simulate result of all those moves
4) Choose cost function
3) Choose search function
4) Optimize