#include "Node.h"

Node::Node(int length)
	:
	length(length)
{
	for (int i = 0; i < length; i++) {
		groups.push_back(Custom_number());
		dgroups_dt.push_back(Custom_number());
	}
}

Node::~Node()
{
	groups.clear();
	dgroups_dt.clear();
	all_steps.clear();
}

void Node::copy_steps(const Node& oth_nod)
{
	if (oth_nod.length == length) {
		all_steps.clear();
		for (int i = 0; i < oth_nod.all_steps.size(); i++) {
			all_steps.push_back(Step(oth_nod.all_steps[i]));
		}
	}
}

void Node::copy_groups(const Node& oth_nod)
{
	if (oth_nod.length == length) {
		for (int i = 0; i < length; i++) {
			groups[i] = oth_nod.groups[i];
		}
	}
}

void Node::add_steps(std::vector<Step> steps)
{
	for (int i = 0; i < steps.size(); i++) {
		all_steps.push_back(steps[i]);
	}
}

void Node::change_groups(std::vector<unsigned int> new_groups, int start_at)
{
	for (int i = start_at; i < new_groups.size() && i < length; i++) {
		groups[i] = Custom_number(new_groups[i]);
	}
}

void Node::change_groups_custom(std::vector<Custom_number> new_groups, int start_at)
{
	for (int i = start_at; i < new_groups.size() && i < length; i++) {
		groups[i] = new_groups[i];
	}
}

Node::Node(const Node& oth_nod)
	:
	Node(oth_nod.length)
{
	copy_steps(oth_nod);
	copy_groups(oth_nod);
}

void Node::add_step(Step st)
{
	all_steps.push_back(st);
}

void Node::add_step_by_values(int from, int to, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide)
{
	all_steps.push_back(Step(from, 0, to, 0, both_ways, c, times, divide));
}

void Node::change_step_constant(Custom_number c, int pos)
{
	if (pos >= 0 && pos < all_steps.size()) {
		all_steps[pos].c_val = c;
	}
}

void Node::change_times_step(std::vector<int> times, int pos)
{
	if (pos >= 0 && pos < all_steps.size()) {
		all_steps[pos].times = times;
	}
}

void Node::change_divide_step(std::vector<int> divide, int pos)
{
	if (pos >= 0 && pos < all_steps.size()) {
		all_steps[pos].divide = divide;
	}
}

void Node::change_both_ways_step(bool both_ways, int pos)
{
	if (pos >= 0 && pos < all_steps.size()) {
		all_steps[pos].both_ways = both_ways;
	}
}

void Node::change_from_step(int from, int pos)
{
	if (pos >= 0 && pos < all_steps.size()) {
		all_steps[pos].from = from;
	}
}

void Node::change_to_step(int to, int pos)
{
	if (pos >= 0 && pos < all_steps.size()) {
		all_steps[pos].to = to;
	}
}

int Node::get_position_step(int from, int to)
{
	for (int i = 0; i < all_steps.size(); i++) {
		if (all_steps[i].from == from) {
			if (all_steps[i].to == to) {
				return i;
			}
		}
	}
	return -1;
}

void Node::delete_step(int loc)
{
	if (loc >= 0 && loc < all_steps.size()) {
		all_steps.erase(all_steps.begin() + loc);
	}
}

void Node::delete_step_by_groups(int from, int to)
{
	delete_step(get_position_step(from, to));
}

void Node::change_group(int pos, unsigned int value)
{
	if (pos >= 0 && pos < length) {
		groups[pos] = Custom_number(value);
	}
}


void Node::change_group_custom(int pos, Custom_number value)
{
	if (pos >= 0 && pos < length) {
		groups[pos] = value;
	}
}

unsigned int Node::get_group_value(int pos)
{
	return groups[pos].get_value_as_unsignedint();
}

Custom_number  Node::get_group_value_custom(int pos)
{
	return groups[pos];
}

Custom_number Node::get_dt_group_value(int pos)
{
	return dgroups_dt[pos];
}

std::vector<unsigned int> Node::get_groups()
{
	std::vector<unsigned int> gro;
	for (int i = 0; i < length; i++) {
		gro.push_back(groups[i].get_value_as_unsignedint());
	}
	return gro;
}

std::vector<Custom_number> Node::get_groups_custom()
{
	return groups;
}

void Node::update_total(std::vector<int> how_to_total, int start_at)
{
	if (start_at >= 0 && start_at < how_to_total.size()) {
		int tot_index = how_to_total[start_at];
		if (tot_index >= 0 && tot_index < length) {
			groups[tot_index] = Custom_number();
			for (int i = start_at + 1; i < how_to_total.size(); i++) {
				int j = how_to_total[i];
				if (j >= 0 && j < length) {
					groups[tot_index] += groups[j];
				}
				else {
					if (j == -1) {
						update_total(how_to_total, i + 1);
						break;
					}
				}
			}
		}
	}
}

void Node::update_groups_dt(bool ignore_if_under)
{
	for (int i = 0; i < all_steps.size(); i++) {
		Custom_number trans = all_steps[i].c_val;
		for (int j = 0; j < all_steps[i].times.size(); j++) {
			int k = all_steps[i].times[j];
			if (k >= 0 && k < length) {
				if (k == 2 && ignore_if_under){
					if (groups[2].get_exp() < 0) {
						trans = Custom_number();
					}
				}
				trans *= groups[k];
			}
		}
		for (int j = 0; j < all_steps[i].divide.size(); j++) {
			int k = all_steps[i].divide[j];
			if (k >= 0 && k < length) {
				trans /= groups[k];
			}
		}
		if (all_steps[i].both_ways) {
			Custom_number sum_of = groups[all_steps[i].from];
			sum_of += dgroups_dt[all_steps[i].from];
			if (sum_of  < trans) {
				trans = sum_of;
			}
			dgroups_dt[all_steps[i].from] -= trans;
			dgroups_dt[all_steps[i].to] += trans;
		}
		else {
			dgroups_dt[all_steps[i].to] += trans;
		}
	}
}

void Node::add_dt_to_groups()
{
	for (int i = 0; i < length; i++) {
		groups[i] += dgroups_dt[i];
		dgroups_dt[i] = Custom_number();
	}
}

void Node::add_to_dt(int pos, Custom_number value)
{
	if (pos >= 0 && pos < length) {
		dgroups_dt[pos] += value;
	}
}

void Node::remove_from_dt(int pos, Custom_number value)
{
	if (pos >= 0 && pos < length) {
		dgroups_dt[pos] -= value;
	}
}

int Node::get_steps()
{
	return all_steps.size();
}