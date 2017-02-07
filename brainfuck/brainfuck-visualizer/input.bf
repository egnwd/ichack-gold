Vigenere encryption in Brainfuck

% Initialize key
++[
>++++++			% cell 1 = 0
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







