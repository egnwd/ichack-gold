-module(node).
-export([start/0]).


start() ->
	receive
		{next, TIDS, T, SystemTID} -> next(TIDS, T, SystemTID)
	end.

next([TID|TIDS], T, SystemTID) ->
	% T = 100,
	T2 = 0,
	if
		length(TIDS) rem 2 == 0 ->
			io:format('\\~n'),
			timer:sleep(T),
			io:format(' \\~n'),
			timer:sleep(T),
			io:format('  \\~n'),
			timer:sleep(T),
			io:format('   \\~n'),
			timer:sleep(T),
			io:format('    \\~n'),
			timer:sleep(T),
			io:format('     \\~n'),
			timer:sleep(T),
			io:format('      \\~n'),
			timer:sleep(T),
			io:format('       \\~n'),
			timer:sleep(T),
			io:format('        \\~n'),
			timer:sleep(T),
			io:format('         \\~n'),
			timer:sleep(T),
			io:format('          \\~n'),
			timer:sleep(T),
			io:format('            v~n'),
			timer:sleep(T),
			io:format('             ~p ~n', [self()]);
		true ->
			io:format('             /~n'),
			timer:sleep(T),
			io:format('            /~n'),
			timer:sleep(T),
			io:format('           /~n'),
			timer:sleep(T),
			io:format('          /~n'),
			timer:sleep(T),
			io:format('         /~n'),
			timer:sleep(T),
			io:format('        /~n'),
			timer:sleep(T),
			io:format('       /~n'),
			timer:sleep(T),
			io:format('      /~n'),
			timer:sleep(T),
			io:format('     /~n'),
			timer:sleep(T),
			io:format('    /~n'),
			timer:sleep(T),
			io:format('   /~n'),
			timer:sleep(T),
			io:format('  v~n'),
			timer:sleep(T),
			io:format('~p~n', [self()])
	end,
	timer:sleep(T2),
	%timer:sleep(100),
	NextT = round(T * 0.8),
	TID ! {next, TIDS, NextT, SystemTID};
next([], _, SystemTID) ->
	SystemTID ! {continue},
	io:format('DONE').

