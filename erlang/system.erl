-module(system).
-export([start/0]).


start() ->
	io:format('Spawning 100 erlang nodes... ~n'),
	[TID|TIDS] = lists:map(fun(_) -> spawn(node, start, []) end, lists:seq(1, 100)),
	TID ! {next, TIDS, 100}.
	