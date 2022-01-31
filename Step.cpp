#include "Step.h" 

Step::Step(int from, int node1, int to, int node2, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide)
	:
	from(from),
	node1(node1),
	to(to),
	node2(node2),
	both_ways(both_ways),
	c_val(c),
	times(times),
	divide(divide)
{}

Step::Step(const Step& st)
	:
	from(st.from),
	node1(st.node1),
	to(st.to),
	node2(st.node2),
	both_ways(st.both_ways),
	c_val(st.c_val),
	times(st.times),
	divide(st.divide)
{}