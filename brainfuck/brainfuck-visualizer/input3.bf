Vigenere encryption in Brainfuck

++[                             % Initialize key
>++++++++++ ++++++++++          % cell 1 = 20
>+++ +++                        % cell 2 = 6
>++++++++++ ++++++++++ ++++     % cell 3 = 24

>[-]+                           % cell 4 = 1
>,>,>,                          % STDIN
<<<<<<[->>>>+<<<<]>>>>          % Encode cell 5
---------- ---------- ------    % Subtract 26
.<<<[->>>>+<<<<]>>>>            % Encode cell 6
---------- ---------- ------    % Subtract 26
.<<<[->>>>+<<<<]>>>>            % Encode cell 7
---------- ---------- ------    % Subtract 26
.<<<<<<<-                       % Decrement counter
]
>>>>>>>>+++++ +++++.



