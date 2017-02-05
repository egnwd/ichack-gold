-module(system).
-export([start/0]).


start() ->
	io:format('SPAWNING 100 INTERCONNECTED ERLANG NODES... ~n'),
	[TID|TIDS] = lists:map(fun(_) -> spawn(node, start, []) end, lists:seq(1, 100)),
	timer:sleep(2000),
	TID ! {next, TIDS, 100, self()},
	receive
		{continue} -> continue()
	end.
	
continue() ->
	io:format('SPAWNING ANOTHER 100000 ERLANG NODES... ~n'),
	[TID|TIDS] = lists:map(fun(_) -> spawn(node2, start, []) end, lists:seq(1, 100000)),
	TID ! {next, TIDS, 0}.
	