-module(node2).
-export([start/0]).


start() ->
	receive
		{next, TIDS, Count, Secret} -> next(TIDS, Count, Secret)
	end.

next([TID|TIDS], Count, Secret) ->
	if
		Count rem 10000 == 0 ->
			io:format('~p~n', [Count]);
		true -> ok
	end,
	TID ! {next, TIDS, Count + 1};
next([], _, Secret) ->
	io:format('Received Secret: ~p~n', [Secret]).

