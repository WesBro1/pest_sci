#pragma once
#include <vector>
#include "Custom_number.h"

class Step
{
public:
	Step(int from, int node1, int to, int node2, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide);
	~Step() = default;
	Step(const Step& st);

public:
	int from; //from group
	int to; //to group
	int node1; //using groups of node 
	int node2; //and node (This can also be a transfer from two groups of one node using a group of a second node)
	bool both_ways; //transfer or addition
	Custom_number c_val;
	std::vector<int> times; //times groups
	std::vector<int> divide; //divided by groups
};