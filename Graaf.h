#pragma once

#include "Node.h"
#include <fstream>
#include "PyConversion.h"

class Graaf
{
public:
	Graaf() = default;
	~Graaf();
	Graaf(const Graaf& g) = delete;
	void add_node(Node& other_node, std::string name);
	void add_node_like_first(std::string name);
	void add_node_like_last(std::string name);
	void create_node(int pop, std::string name, bool patient_zero = false);
	int get_position(std::string name);
	void change_how_to_total(std::vector<int> howto_total);
	void change_how_to_total_python(PyObject* inv);
	void change_all_group_names(std::vector<std::string> groupnames);
	void change_all_group_names_python(PyObject*);
	void change_name(int pos, std::string new_name);
	int get_position_group(std::string name);
	void change_group(int pos, int gro, unsigned int new_pop);
	void change_group_custom(int pos, int gro, Custom_number new_pop);
	void change_name_group(int pos, std::string new_name);
	std::vector<std::string> return_all_group_names();
	PyObject* return_all_groups_names_python();
	std::vector<std::string>  return_all_node_names();
	PyObject* return_all_node_names_python();
	void change_name_by_name(std::string name, std::string new_name);
	void delete_node(int pos);
	void delete_all_nodes(bool also_steps);
	void add_step(Step st);
	void add_step_by_values(int from, int node1, int to, int node2, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide);
	void add_step_by_values_python(int from, int node1, int to, int node2, bool both_ways, double c, signed char expon, PyObject* times, PyObject* divide);
	void add_step_to_node(int node, int from, int to, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide);
	void add_step_to_node_python(int node, int from, int to, bool both_ways, double c, signed char expon, PyObject* times, PyObject* divide);
	void change_step_constant_custom(Custom_number c, int pos);
	void change_step_constant(double c, signed char expon, int pos);
	void change_times_step(std::vector<int> times, int pos);
	void change_divide_step(std::vector<int> divide, int pos);
	void change_both_ways_step(bool both_ways, int pos);
	void change_from_step(int from, int pos);
	void change_to_step(int to, int pos);
	void change_first_step_node(int node1, int pos);
	void change_second_step_node(int node2, int pos);
	int get_position_step(int from, int to, int node1, int node2);
	void delete_step(int loc);
	void delete_step_by_groups(int from, int to, int node1, int node2);
	void delete_all_steps();
	std::vector<unsigned int> get_groups(int pos);
	std::vector<std::string> get_groups_custom(int pos);
	PyObject* get_groups_custom_python(int pos);
	std::vector<std::string> get_group_all_nodes_custom(int group);
	PyObject* get_group_all_nodes_custom_python(int group);
	PyObject* get_groups_python(int pos);
	std::vector<unsigned int> get_group_all_nodes(int group);
	PyObject* get_groups_all_nodes_python(int group);
	std::vector<std::string> get_group_dt_all_nodes_custom(int group);
	PyObject* get_group_dt_all_nodes_custom_python(int group);
	std::vector<int> get_group_dt_all_nodes(int group);
	PyObject* get_group_dt_all_nodes_python(int group);
	bool get_dt_sign(int node, int group);
	void update_all_total();
	void all_steps_between_nodes();
	void all_update_dt();
	void all_add_dt_to_groups();
	void time_step();
	void node_change_step_constant_custom(Custom_number c, int node, int group_from, int group_to);
	void node_change_step_constant(double c, signed char expon, int node, int group_from, int group_to);
	void node_change_times_step(std::vector<int> times, int node, int group_from, int group_to);
	void node_change_divide_step(std::vector<int> divide, int node, int group_from, int group_to);
	void node_change_dividetimes(PyObject*, bool divi, int node, int group_from, int group_to);
	void node_change_both_ways_step(bool both_ways, int node, int group_from, int group_to);
	void node_change_from_step(int from, int node, int group_from, int group_to);
	void node_change_to_step(int to, int node, int group_from, int group_to);
	void allnodes_change_step_constant_custom(Custom_number c, int group_from, int group_to);
	void allnodes_change_step_constant(double c, signed char expon, int group_from, int group_to);
	void allnodes_change_times_step(std::vector<int> times, int group_from, int group_to);
	void allnodes_change_divide_step(std::vector<int> divide, int group_from, int group_to);
	void allnodes_change_timesdivide_step(PyObject*, bool divi, int group_from, int group_to);
	void allnodes_change_both_ways_step(bool both_ways, int group_from, int group_to);
	void allnodes_change_from_step(int from, int group_from, int group_to);
	void allnodes_change_to_step(int to, int group_from, int group_to);
	void output_node_file_add_header(std::string path_to_output_file, int width = 20);
	void output_node_file_add_current_groups(int node, std::string path_to_output_file, int width = 20);
	void run_and_output_to_txt_per_node(std::string name_prefix, std::string path_to_output_directory, int run_before, int steps_between_record, int how_many_to_record);
	int get_n_node();
	bool check_if_zero(int group);
	std::string get_group_name(int pos);
	int n_steps();
	bool node_steps();

public:
	int n_nodes = 0;

private:
	std::vector<Step> all_steps_between;
	std::vector<Node> all_nodes;
	std::vector<std::string> node_names;
	std::vector<std::string> group_names;
	std::vector<int> how_to_total;
};

std::string fill_left_with_spaces(std::string original, int width);
void to_txt_file(std::vector<unsigned long long int> values, std::string output_path, int width = 20);
Node from_txt_file(std::string path_to_file, int length, std::vector<std::string> group_names);
int pos_from_string_value_or_name(std::string current, std::vector<std::string> group_names);

