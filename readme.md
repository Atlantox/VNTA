Visual Novel Technical Assistant

Version 1.1

VNTA is a software with one single objective: Help authors to balance their visual novels.

Remember that a visual novel is a game with many decisions, each decision is branch the history and gives the player a unique experience.
But if you don't to it right, you can create a very difficult or very easy visual novel, of course that based in good and bad ending.
For that reason, VNTA will travel all possible roads of your visual novel and gives you a valuable information, how many roads axists and the statistics of each possible ending.
Knowing that statistics you can balance and change numbers to made your visual novel more easy or difficult, that depends exclusively of you.

How to use it?

Exists two ways, the easy (spanish) or the difficult

If you speak spanish just look at that video and enjoy: 

But if you are english speaker, don't worry, just follow the pattern of the example.xlsx, anyway I leave the rules here:

1. Use the correct decision type: Exists 4 types of Decision, they are Decision (D), Consecuence (C), If condition (I) and Ending (E-)
    The Decisions must have the same name to relate him and are these decisions that branch the visual novel history
    To know the total combinations, just multiply all the number of options of each decision, example: if you have 3 Decisions with 2, 2, and 3 options, then you will have (2 * 2 * 3) = 12 combinations
2. Make sure of each Decision has a different and unique id: Because if a id repeats, will generate duplicates or missing of roads. You can use text as id but I recommend use numbers
3. In Excel you can combine the name cell to relate Options and also not, just make sure that the related options has the same name
4. DO NOT LEAVE BLANK ROWS
5. Use the correct decision type ('D', 'C', 'I', 'E-')
6. 'I' and 'E-' decisions will require a condtion, just put the operator in the option field (<, >, <= ,>=, =) and the field to compare in the points column, for example if you want a bad ending if the frienship points are 4 or less, then put <= on the option field and 4 in the friendship column
7. Of course if you visual novel not contains points, you can do it using dependencies, a dependecy happens when a decision depends of a previous decision, you can add many dependencies in a self decision as you need, you can add negative dependencies too, just write the decision id in the dependency column, separate with commas if the decision has multiple dependencies and use - to do negative dependencies (a option with negative dependency just will taked if the path hasn't taked the written decision)
8. After the dependencies column just add a column for each point in you visual novel, it are limitless.
9. If you place numbers in the points columns in a D type decision, that points will be add (or subtract if are negative) if the path take that decision
10. Once you have finished your excel file, make sure that the excel sheet names 'decisions' then execute VNTA.exe and select the excel file, and BE CAREFUL WITH DEACTIVATE LITE MODE, if you only want to know the total combinations and/or the endings statistics, use the lite mode, but if you want to explore between the roads and decisions, deactivate the lite mode BUT I strongly recommend not do that if you visual novel has really many possible paths, deactivating the lite mode, the program will save each road in a .vnta file, once the roads are travelled, the roads are loaded in RAM memory and you will search and navigate between. WARNING: one million of roads are approximately 200MB so BE CAREFULL WITH YOUR DISK SPACE PLEASE, as advantaje, once created the .vnta file, you can open it with VNTA.exe and the decisions will be loaded from the file without travel all the roads again.

Being english or spanish speaker, I hope that VNTA helps you so much!

1.1 Version notes:
* Fixed an error that prevent to save a excel file until you close the .exe, the excel file is opened for getting the rows and after it is closed
