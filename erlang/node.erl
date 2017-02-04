-module(node).
-export([start/0]).


start() ->
	receive
		{next, TIDS, T} -> next(TIDS, T)
	end.

next([TID|TIDS], T) ->
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
	TID ! {next, TIDS, NextT};
next([], _) ->
	io:format('DONE').

