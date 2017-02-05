# distributed algorithms, n.dulay, 4 jan 17
# simple build and run makefile, v1

.SUFFIXES: .erl .beam

MODULES  = system node node2

# BUILD =======================================================

ERLC	= erlc -o ebin

ebin/%.beam: %.erl
	$(ERLC) $<

all:	ebin ${MODULES:%=ebin/%.beam}

ebin:
	mkdir ebin

debug:
	erl -s crashdump_viewer start

.PHONY: clean
clean:
	rm -f ebin/* erl_crash.dump

# LOCAL RUN ===================================================

SYSTEM    = system


L_HOST    = localhost.localdomain
L_ERL     = erl -noshell -pa ebin -setcookie pass
L_ERLNODE = node

run:	all
	$(L_ERL) -s $(SYSTEM) start



# to run manually, run make node1 and make node2 in separate windows
# then make man2, remove manually
#node1:	all
#	$(L_ERL) -name $(L_ERLNODE)1@$(L_HOST)
#
#node2:	all
#	$(L_ERL) -name $(L_ERLNODE)2@$(L_HOST)
#
#man2:	all
#	$(L_ERL) -name $(L_ERLNODE)3@$(L_HOST) -s $(L_SYSTEM) start

# to run and clean up automatically
#run2:	all
#	for k in $$(seq 1 1 $(HOSTSm1)); do \
#	  ( $(L_ERL) -name $(L_ERLNODE)$$k@$(L_HOST) & ) ; \
#	done
#	sleep 1
#	$(L_ERL) -name $(L_ERLNODE)$(HOSTS)@$(L_HOST) -s $(L_SYSTEM) start

# DOCKER RUN ===================================================


#D_SUBNET   = 172.19.0
#D_HOSTNAME = host
#D_HOST_DIR = /code
#D_ERL      = erl -noshell -pa $(D_HOST_DIR)/ebin -setcookie pass
#D_ERLNODE  = node
#
#run3:
#	for k in $$(seq 1 1 $(HOSTSm1)); do \
#	  docker exec -itd $(D_HOSTNAME)$$k \
#	     $(D_ERL) -name $(D_ERLNODE)@$(D_SUBNET).$$k ; \
#	done
#
#	docker exec -it $(D_HOSTNAME)$(HOSTS) \
#	  $(D_ERL) -name $(D_ERLNODE)@$(D_SUBNET).3 -s $(D_SYSTEM) start
#