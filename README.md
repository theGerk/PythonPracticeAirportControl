This program uses Python 2.7

-----------------

Input:

The program either can take it's input from standard input or takes a commdand line argument which is the file name of the program.
The input is to be formated in the following form:

ID, Submission Time, Requested Start, Requested Duration

ID is a string that can contain anything and is simply the name of the plane. There may not be any control characters or commas in this string. It should be unique but the program will work weather or not it is.
Submission Time is always a non-negitive integer and is never less than the previous entry's Submission Time. This number represents the time at which this plane made a request to take off. It is formated as the string representation of the number (human readable). If the number is not formated as an integer correctly then the program's behavior is undefined and may throw an error or exit. If the number is less then the previous entry's Submission Time, then it will throw an error.
Requested Start is always an integer. This number represents the time at which this plane would like to start The integer is formated as the string representation of the number (human readable). If the number is not formated as an integer correctly then the program's behavior is undefined and may throw an error or exit.
Requested Duration is always a non-negitive integer. This number represents the amount of time it takes this plane to take off, If this number is not a non-negitive integer, then the program's behavior is undefined and may throw an error or exit.

Example Input:

~~~
Delta 160, 0, 0, 4
UAL 120, 0, 5, 4
Made up airline PI^2, 3, 8, 10
~~~

Each of these entries are put on a single line and there may be no blank lines inbetween, or the behavior is undefined.


----------------------------------------------------------------------------------------------------


What it does:

The program starts with time at 0.

The program then adds each entry into a priority queue for which it's Submission Time is 0. The priority queue gives preference to putting in as many planes as quickly as possible, that means giving preference to wasting no time (no time where a plane is not on the runway if it can be avoided) and secondary preference to planes leaving sooner (if two planes are able to leave at the same time, then the one with less duration is given preference). If all these other things are the same then the preference is given to whichever plane made the request first, and after that any ordering is allowed.

Then the program increments the time by 1 and repeats, until there are no more entries, and all planes have taken off.


----------------------------------------------------------------------------------------------------


Output:

At every tick in which the priority queue changes the program outputs a human readable explanation of what is in the queue.

At the end a list of plane names and take off times will be printed.