# RILEY MILLER BGP Router 

## High Level Approach
I decided to seperate out the packet fowarding and route managment in the `Router` class seperate. When the main event loop in `run` routes a message to `update` or `withdraw` it modifies `self.table` and calls my `_contact_neightbors` helper to broadcast the message. It also checks `self.relations` to make sure we dont transmit messages to unwanted parties like peers or providers. When data hits the `data` method the router goes through an if/else tie breaker using the rules to choose a path. The biggest and best design choice I made was keeping the permanent table untouched and creating a temp table that gets `condense_table` called on it which does the math and triggers when `dump` is triggered. 

## Challenges Faced:
* Bitwise math in Python: It took me a while to research how to do the netmask math for aggregation. In the end it was just a one liner. I initially just wanted to use << 1 to leftshift the netmask bit by 1. But I had to add the 32 bit ceiling to prevent python from creating a 33 bit number. 
* Modifying lists during iteration: In the `condense_table` I ahd to merge routes and delete two old routes to append the new ones. I realized that modifying the list while iterating through it shifts the indicies and crashes. I solved this by popping j from the list before popping i. This is becuase j is always larger then i so always further to the right on the list.
* Handeling withdrawls: When peer sent an updated version of a route to my router it alr knew about some of the info but my update method would just blindly append it. This caused my routing tables to get full quickly with dups. To fix this I implemented a block in my `update` method where I loop over the table and filter out dups.
* Small things: I ran into a few accidental infinite loops and wrong indenetation as well as plently of typos and other small erorrs. 

## Testing: 
I tested the code iteritivly through `./test`. I made sure I understand the intent behind the tests before developing my code and got the tests to pass in order as I went through coding it. I used 1-1 and 1-2 to verify the basics with JSON and routing table appending. I used level 4 testing to test peer rules adn ensure my router properly dropped packets when providers tried to route through me to other providers. I finally used the error logs a bunch with the level 6 tests which helped me realize I needed to run my aggregation logic on a copy of the table instead of the real thing. 
