-module(node2).
-export([start/0]).


start() ->
	receive
		{next, TIDS, Count} -> next(TIDS, Count)
	end.

next([TID|TIDS], Count) ->
	if
		Count rem 10000 == 0->
			io:format('~p~n', [Count]);
		true -> ok
	end,
	TID ! {next, TIDS, Count + 1};
next([], _) ->
	io:format('DONE~n').

