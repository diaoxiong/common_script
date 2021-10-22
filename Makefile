.PHONY: cp
cp:
	rm -f ~/Pictures/Lark*.png; \
	rm -f ~/Pictures/WX*.png

.PHONY: son
son:
	sudo pmset -b sleep 0; sudo pmset -b disablesleep 1

.PHONY: soff
soff:
	sudo pmset -b sleep 15; sudo pmset -b disablesleep 0