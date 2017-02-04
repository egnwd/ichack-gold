[
	Vigenere encryption in Brainfuck





% Read message

% Stop if '\n'
+[>,.
									% Read char into cell 1

									% Copy char to cells 2 and 3
	[>+>+<<-]

									% store in cell 4 '\n' == 10
	>>> +++++ +++++

									% Check if cell 3 == cell 4
	[-<->] 							% now cell 4 is 0
									% if cell 3 is also 0 stop reading from stdin
	< 
									% if not zero make cell 0 = 2
	[<<<+>>>]
									% else cell 0 = 0 
	<<<-


]
]

% Initialize key
++[
>				% cell 1 = 0
>+				% cell 2 = 1
>++				% cell 3 = 2

>[-]+		    % cell 4 = 1 (ensure its empty)


>,				% Read from stdin 3 chars into cells 5 6 7

>,
>,

<<<<<<			% back to cell 1

[->>>>+<<<<]	% encode cell 5 with key at cell 1

>>>>.<<<		% print cell 5 and go back to cell 2

[->>>>+<<<<]	% encode cell 6 with key at cell 2
>>>>.<<<		% print cell 6 and go back to cell 3
[->>>>+<<<<]	% encode cell 7 with key at cell 3
>>>>.			% print cell 7

<<<<<<<-		% decrement counter

]


>>>>>>>>
+++++ +++++.







