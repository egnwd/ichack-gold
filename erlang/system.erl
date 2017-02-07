-module(system).
-export([start/1]).


start([Arg|_]) ->
	io:format('DECODING -------> ~p~n', [Arg]),
	io:format('SPAWNING 100 INTERCONNECTED ERLANG NODES... ~n'),
	[TID|TIDS] = lists:map(fun(_) -> spawn(node, start, []) end, lists:seq(1, 100)),
	timer:sleep(2000),
	TID ! {next, TIDS, 100, self()},
	receive
		{continue} -> continue(Arg)
	end.
	
continue(SECRET) ->
	io:format("Relay message to Mario"),
	Fifo = open_port("mario", [eof]),
	port_command(Fifo, <<"it's a go!\n">>),
	init:stop().
	