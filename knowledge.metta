;PROPERTY GROUNDING:

;What it means to set the table:
!(AddBeliefEvent (((table --> (IntSet prepared)) <=> ((u x T) --> up)) (1.0 0.9)))

;What it means to deliver coffee:
!(AddBeliefEvent (((coffee --> (IntSet made)) <=> ((u x G) --> up)) (1.0 0.9)))

;What it means to store cup
!(AddBeliefEvent (((cup --> (IntSet stored)) <=> ((H x u) --> up)) (1.0 0.9)))

;What it means to for bird to go to sit at table
!(AddBeliefEvent ((((bird x table) --> sit) <=> ((x x T) --> right)) (1.0 0.9)))

;CATEGORICAL INFORMATION

;Cups are containers
!(AddBeliefEvent ((cup --> container) (1.0 0.9)))

;Tables are furniture
!(AddBeliefEvent ((table --> furniture) (1.0 0.9)))

;Coffee is a drink
!(AddBeliefEvent ((coffee --> drink) (1.0 0.9)))

;Coffee is black
!(AddBeliefEvent ((coffee --> (IntSet black)) (1.0 0.9)))

;table is brown
!(AddBeliefEvent ((table --> (IntSet brown)) (1.0 0.9)))
