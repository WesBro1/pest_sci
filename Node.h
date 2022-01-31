#pragma once
#include "Step.h"

class Node 
{
public:
	Node(int length);
	~Node();
	void copy_steps(const Node& oth_nod);
	void copy_groups(const Node& oth_nod);
	void add_steps(std::vector<Step> steps);
	void change_groups(std::vector<unsigned int> groups, int start_at = 0);
	void change_groups_custom(std::vector<Custom_number> groups, int start_at = 0);
	Node(const Node& oth_nod);
	void add_step(Step st);
	void add_step_by_values(int from, int to, bool both_ways, Custom_number c_val, std::vector<int> times, std::vector<int> divide);
	void change_step_constant(Custom_number c, int pos);
	void change_times_step(std::vector<int> times, int pos);
	void change_divide_step(std::vector<int> divide, int pos);
	void change_both_ways_step(bool both_ways, int pos);
	void change_from_step(int from, int pos);
	void change_to_step(int to, int pos);
	int get_position_step(int from, int to);
	void delete_step(int loc);
	void delete_step_by_groups(int from, int to);
	void change_group(int pos, unsigned int value);
	void change_group_custom(int pos, Custom_number value);
	unsigned int get_group_value(int pos);
	Custom_number get_group_value_custom(int pos);
	Custom_number get_dt_group_value(int pos);
	std::vector<unsigned int> get_groups();
	std::vector<Custom_number> get_groups_custom();
	void update_total(std::vector<int> how_to_total, int start_at = 0);
	void update_groups_dt(bool ignore_if_under = true);
	void add_dt_to_groups();
	void add_to_dt(int pos, Custom_number value);
	void remove_from_dt(int pos, Custom_number value);
	int get_steps();

public:
	int length;

private:
	std::vector<Custom_number> groups;
	std::vector<Custom_number> dgroups_dt;
	std::vector<Step> all_steps;
};