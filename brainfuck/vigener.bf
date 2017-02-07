[
	Vigenere encryption in Brainfuck
]


% Read message

% Stop if '\n'
+[>,.
	% Read char into cell 1

	% Copy char to cells 2 and 3
	[>+>+<<-]

	% store in cell 4 '\n' == 10
	>>>++++++++++

	% Check if cell 3 == cell 4
	[-<->] % now cell 4 is 0
	% if cell 3 is also 0, stop reading from stdin
	< 
		% if not zero make cell 0 = 2
		[<<<+>>>]
		% else cell 0 = 0 
		<<<-


]

% Read key