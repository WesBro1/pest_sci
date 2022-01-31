#include "Graaf.h"

std::string fill_left_with_spaces(std::string original, int width) {
	std::string new_string;
	if (original.size() <= width) {
		int end = width - original.size();
		for (int i = 0; i < end; i++) {
			new_string += " ";
		}
		new_string += original;
	}
	else {
		new_string = original.substr(0, width);
	}
	return new_string;
}

Graaf::~Graaf()
{
	all_steps_between.clear();
	all_nodes.clear();
	group_names.clear();
	how_to_total.clear();
	node_names.clear();
}

void Graaf::change_how_to_total(std::vector<int> howto_total)
{
	how_to_total = howto_total;
}

void Graaf::change_all_group_names(std::vector<std::string> groupnames)
{
	group_names = groupnames;
}

void Graaf::add_node(Node& other_node, std::string name)
{
	all_nodes.push_back(other_node);
	node_names.push_back(name);
	n_nodes++;
}

void Graaf::add_node_like_first(std::string name)
{
	all_nodes.push_back(Node(all_nodes[0]));
	node_names.push_back(name);
	n_nodes++;
}

void Graaf::add_node_like_last(std::string name)
{
	all_nodes.push_back(Node(all_nodes.back()));
	node_names.push_back(name);
	n_nodes++;
}

void Graaf::create_node(int pop, std::string name, bool patient_zero)
{
	Node New_node = Node(group_names.size());
	New_node.change_group(1, (unsigned int)pop-5);
	if (patient_zero) {
		New_node.change_group(2, (unsigned int)5);
	}
	all_nodes.push_back(New_node);
	node_names.push_back(name);
	n_nodes++;
}

int Graaf::get_position(std::string name)
{
	for (int i = 0; i < n_nodes; i++) {
		if (node_names[i] == name) {
			return i;
		}
	}
	return -1;
}

void Graaf::change_name(int pos, std::string new_name)
{
	if (pos >= 0 && pos < n_nodes) {
		node_names[pos] = new_name;
	}
}

int Graaf::get_position_group(std::string name)
{
	for (int i = 0; i < group_names.size(); i++) {
		if (group_names[i] == name) {
			return i;
		}
	}
	return -1;
}

void Graaf::change_group(int pos, int gro, unsigned int new_pop)
{
	if (pos >= 0 && pos < n_nodes) {
		all_nodes[pos].change_group(gro, new_pop);
	}
}

void Graaf::change_group_custom(int pos, int gro, Custom_number new_pop)
{
	if (pos >= 0 && pos < n_nodes) {
		all_nodes[pos].change_group_custom(gro, new_pop);
	}
}

void Graaf::change_name_group(int pos, std::string new_name)
{
	if (pos >= 0 && pos < group_names.size()) {
		group_names[pos] = new_name;
	}
}

std::vector<std::string> Graaf::return_all_group_names()
{
	return group_names;
}

std::vector<std::string>  Graaf::return_all_node_names()
{
	return node_names;
}

void Graaf::change_name_by_name(std::string name, std::string new_name)
{
	change_name(get_position(name), new_name);
}

void Graaf::delete_node(int pos)
{
	if (pos >= 0 && pos < n_nodes) {
		node_names.erase(node_names.begin()+pos);
		all_nodes.erase(all_nodes.begin()+pos);
		n_nodes--;
	}
}

void Graaf::delete_all_nodes(bool also_steps)
{
	node_names.clear();
	all_nodes.clear();
	n_nodes = 0;
	if (also_steps) {
		all_steps_between.clear();
	}
}

void Graaf::add_step(Step st)
{
	all_steps_between.push_back(st);
}

void Graaf::change_how_to_total_python(PyObject* inv)
{
	change_how_to_total(int_vec_from_list(inv));
}

void Graaf::add_step_by_values(int from, int node1, int to, int node2, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide)
{
	all_steps_between.push_back(Step(from, node1, to, node2, both_ways, c, times, divide));
}

void Graaf::add_step_by_values_python(int from, int node1, int to, int node2, bool both_ways, double c, signed char expon, PyObject* times, PyObject* divide)
{
	add_step_by_values(from, node1, to, node2, both_ways, Custom_number(c, expon), int_vec_from_list(times), int_vec_from_list(divide));
}

void Graaf::add_step_to_node(int node, int from, int to, bool both_ways, Custom_number c, std::vector<int> times, std::vector<int> divide)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].add_step_by_values(from, to, both_ways, c, times, divide);
	}
}

void Graaf::add_step_to_node_python(int node, int from, int to, bool both_ways, double c, signed char expon, PyObject* times, PyObject* divide)
{
	add_step_to_node(node, from, to, both_ways, Custom_number(c, expon), int_vec_from_list(times), int_vec_from_list(divide));
}

void Graaf::change_step_constant_custom(Custom_number c, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].c_val = c;
	}
}

void Graaf::change_step_constant(double c, signed char ex, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].c_val = Custom_number(c,ex);
	}
}

void Graaf::change_times_step(std::vector<int> times, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].times = times;
	}
}

void Graaf::change_divide_step(std::vector<int> divide, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].divide = divide;
	}
}

void Graaf::change_both_ways_step(bool both_ways, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].both_ways = both_ways;
	}
}

void Graaf::change_from_step(int from, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].from = from;
	}
}

void Graaf::change_to_step(int to, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].to = to;
	}
}

void Graaf::change_first_step_node(int node1, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].node1 = node1;
	}
}

void Graaf::change_second_step_node(int node2, int pos)
{
	if (pos >= 0 && pos < all_steps_between.size()) {
		all_steps_between[pos].node2 = node2;
	}
}

int Graaf::get_position_step(int from, int to, int node1, int node2)
{
	for (int i = 0; i < all_steps_between.size(); i++) {
		if (all_steps_between[i].from == from) {
			if (all_steps_between[i].to == to) {
				if (all_steps_between[i].node1 == node1) {
					if (all_steps_between[i].node2 == node2) {
						return i;
					}
				}
			}
		}
	}
	return -1;
}

void Graaf::delete_step(int loc)
{
	if (loc >= 0 && loc < all_steps_between.size()) {
		all_steps_between.erase(all_steps_between.begin() + loc);
	}
}

void Graaf::delete_step_by_groups(int from, int to, int node1, int node2)
{
	delete_step(get_position_step(from, to, node1, node2));
}

void Graaf::delete_all_steps()
{
	all_steps_between.clear();
}

std::vector<unsigned int> Graaf::get_groups(int pos)
{
	if (pos >= 0 && pos < n_nodes) {
		return all_nodes[pos].get_groups();
	}
	std::vector<unsigned int> a;
	return a;
}

void Graaf::update_all_total()
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].update_total(how_to_total);
	}
}

int Graaf::get_n_node()
{
	return n_nodes;
}

void Graaf::all_steps_between_nodes()
{
	for (int i = 0; i < all_steps_between.size(); i++) {
		Custom_number trans = all_steps_between[i].c_val;
		int l1 = all_nodes[all_steps_between[i].node1].length;
		int l2 = all_nodes[all_steps_between[i].node2].length;
		for (int j = 0; j < all_steps_between[i].times.size(); j++) {
			int k = all_steps_between[i].times[j];
			if (k >= 0 && k < l1 + l2) {
				if (k < l1) {
					trans *= all_nodes[all_steps_between[i].node1].get_group_value_custom(k);
				}
				else {
					trans *= all_nodes[all_steps_between[i].node2].get_group_value_custom(k-l1);
				}
			}
		}
		for (int j = 0; j < all_steps_between[i].divide.size(); j++) {
			int k = all_steps_between[i].divide[j];
			if (k >= 0 && k < l1 + l2) {
				if (k < l1) {
					trans /= all_nodes[all_steps_between[i].node1].get_group_value(k);
				}
				else {
					trans /= all_nodes[all_steps_between[i].node2].get_group_value(k - l1);
				}
			}
		}
		int k1 = all_steps_between[i].to;
		int k2 = all_steps_between[i].from;
		int node1 = all_steps_between[i].node1;
		int node2 = all_steps_between[i].node1;
		if (k1 >= 0 && k1 < l1 + l2) {
			if (k1 >= l1) {
				k1 -= l1;
				node1 = all_steps_between[i].node2;
			}
		}
		if (k2 >= 0 && k1 < l1 + l2) {
			if (k2 >= l1) {
				k2 -= l1;
				node2 = all_steps_between[i].node2;
			}
		}
		Custom_number sum_of = all_nodes[node2].get_group_value_custom(k2);
		sum_of += all_nodes[node2].get_dt_group_value(k2);
		if (sum_of < trans) {
			trans = sum_of;
		}
		all_nodes[node1].add_to_dt(k1, trans);
		all_nodes[node2].remove_from_dt(k2, trans);
		if (all_steps_between[i].both_ways) {
			if (node1 == all_steps_between[i].node1) {
				node1 = all_steps_between[i].node2;
			}
			else {
				node1 = all_steps_between[i].node1;
			}
			if (node2 == all_steps_between[i].node1) {
				node2 = all_steps_between[i].node2;
			}
			else {
				node2 = all_steps_between[i].node1;
			}
			trans = all_steps_between[i].c_val;
			for (int j = 0; j < all_steps_between[i].times.size(); j++) {
				int k = all_steps_between[i].times[j];
				if (k >= 0 && k < l1 + l2) {
					if (k < l2) {
						trans *= all_nodes[all_steps_between[i].node2].get_group_value_custom(k);
					}
					else {
						trans *= all_nodes[all_steps_between[i].node1].get_group_value_custom(k - l2);
					}
				}
			}
			for (int j = 0; j < all_steps_between[i].divide.size(); j++) {
				int k = all_steps_between[i].divide[j];
				if (k >= 0 && k < l1 + l2) {
					if (k < l2) {
						trans /= all_nodes[all_steps_between[i].node2].get_group_value_custom(k);
					}
					else {
						trans /= all_nodes[all_steps_between[i].node1].get_group_value_custom(k - l2);
					}
				}
			}
			sum_of = all_nodes[node1].get_group_value_custom(k2);
			sum_of += all_nodes[node1].get_dt_group_value(k2);
			if (sum_of < trans) {
				trans = sum_of;
			}
			all_nodes[node1].add_to_dt(k1, trans);
			all_nodes[node2].remove_from_dt(k2, trans);
		}
	}
}

void Graaf::all_update_dt()
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].update_groups_dt();
	}
}

void Graaf::all_add_dt_to_groups()
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].add_dt_to_groups();
	}
}

void Graaf::time_step() 
{
	all_steps_between_nodes();
	all_update_dt();
	all_add_dt_to_groups();
	update_all_total();
}

void Graaf::node_change_step_constant(double c, signed char expon, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_step_constant(Custom_number(c,expon), all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::node_change_step_constant_custom(Custom_number c, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_step_constant(c, all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::node_change_times_step(std::vector<int> times, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_times_step(times, all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::node_change_divide_step(std::vector<int> divide, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_divide_step(divide, all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::node_change_both_ways_step(bool both_ways, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_both_ways_step(both_ways, all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::node_change_from_step(int from, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_from_step(from, all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::node_change_to_step(int to, int node, int group_from, int group_to)
{
	if (node >= 0 && node < n_nodes) {
		all_nodes[node].change_to_step(to, all_nodes[node].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_step_constant_custom(Custom_number c, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_step_constant(c, all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_step_constant(double c, signed char ex, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_step_constant(Custom_number(c, ex), all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_times_step(std::vector<int> times, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_times_step(times, all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_divide_step(std::vector<int> divide, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_divide_step(divide, all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_both_ways_step(bool both_ways, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_both_ways_step(both_ways, all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_from_step(int from, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_from_step(from, all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::allnodes_change_to_step(int to, int group_from, int group_to)
{
	for (int i = 0; i < n_nodes; i++) {
		all_nodes[i].change_to_step(to, all_nodes[i].get_position_step(group_from, group_to));
	}
}

void Graaf::output_node_file_add_header(std::string path_to_output_file, int width)
{
	std::ofstream myfile(path_to_output_file);
	if (myfile.is_open()) {
		for (int i = 0; i < group_names.size(); i++) {
			myfile << fill_left_with_spaces(group_names[i], width);
		}
	}
}

void Graaf::output_node_file_add_current_groups(int node, std::string path_to_output_file, int width)
{
	std::ofstream myfile(path_to_output_file);
	if (myfile.is_open()) {
		if (node >= 0 && node < node_names.size()) {
			std::vector<unsigned int> groups = get_groups(node);
			for (int i = 0; i < groups.size(); i++) {
				myfile << fill_left_with_spaces(std::to_string(groups[i]), width);
			}
		}
	}
}

void Graaf::run_and_output_to_txt_per_node(std::string name_prefix, std::string path_to_output_directory, int run_before, int steps_between_record, int how_many_to_record)
{
	for (int i = 0; i < run_before; i++) {
		time_step();
	}
	std::vector<std::string> file_names;
	std::string fin = ".txt";
	for (int node_i = 0; node_names.size(); node_i++) {
		std::string file_name = path_to_output_directory + name_prefix + node_names[node_i] + fin;
		file_names.push_back(file_name);
		output_node_file_add_header(file_name);
	}
	for (int i = 0; i < how_many_to_record; i++) {
		output_node_file_add_current_groups(i, file_names[i]);
		for (int j = 0; j < steps_between_record; j++) {
			time_step();
		}
	}
}

void Graaf::change_all_group_names_python(PyObject* inc)
{
	change_all_group_names(string_vec_from_list(inc));
}

PyObject* Graaf::return_all_groups_names_python()
{
	return to_list_vec_string(return_all_group_names());
}

PyObject* Graaf::return_all_node_names_python()
{
	return to_list_vec_string(return_all_node_names());
}

PyObject* Graaf::get_groups_python(int pos)
{
	return to_list_vec_unsinged_int(get_groups(pos));
}


std::vector<std::string> Graaf::get_groups_custom(int pos)
{
	std::vector<std::string> a;
	if (pos >= 0 && pos < n_nodes) {
		std::vector<Custom_number> b =  all_nodes[pos].get_groups_custom();
		for (int i = 0; i < b.size(); i++) {
			a.push_back(b[i].to_string());
		}
	}
	return a;
}

PyObject* Graaf::get_groups_custom_python(int pos)
{
	return to_list_vec_string(get_groups_custom(pos));
}

std::vector<std::string> Graaf::get_group_all_nodes_custom(int group)
{
	std::vector<std::string> a;
	if (group >= 0 && group < group_names.size()) {
		for (int i = 0; i < n_nodes; i++) {
			a.push_back(all_nodes[i].get_group_value_custom(group).to_string());
		}
	}
	return a;
}

PyObject* Graaf::get_group_all_nodes_custom_python(int group)
{
	return to_list_vec_string(get_group_all_nodes_custom(group));
}

void Graaf::node_change_dividetimes(PyObject* inc, bool divi, int node, int group_from, int group_to)
{
	if (divi) {
		node_change_divide_step(int_vec_from_list(inc), node, group_from, group_to);
	}
	else {
		node_change_times_step(int_vec_from_list(inc), node, group_from, group_to);
	}
}

void Graaf::allnodes_change_timesdivide_step(PyObject* inc, bool divi, int group_from, int group_to)
{
	if (divi) {
		allnodes_change_divide_step(int_vec_from_list(inc), group_from, group_to);
	}
	else {
		allnodes_change_times_step(int_vec_from_list(inc), group_from, group_to);
	}
}

bool Graaf::check_if_zero(int group)
{
	bool stat = true;
	for (int j = 0; j < n_nodes; j++) {
		if (all_nodes[j].get_group_value(group) != 0) {
			stat = false;
		}
	}
	return stat;
}

std::vector<unsigned int> Graaf::get_group_all_nodes(int group)
{
	std::vector<unsigned int> a;
	if (group >= 0 && group < group_names.size()) {
		for (int i = 0; i < n_nodes; i++) {
			a.push_back(all_nodes[i].get_group_value(group));
		}
	}
	return a;
}

PyObject* Graaf::get_groups_all_nodes_python(int group)
{
	return to_list_vec_unsinged_int(get_group_all_nodes(group));
}

std::string Graaf::get_group_name(int pos)
{
	return group_names[pos];
}

int Graaf::n_steps()
{
	return all_steps_between.size();
}

bool Graaf::node_steps()
{
	int s = all_nodes[0].get_steps();
	bool same = true;
	for (int i = 1; i < n_nodes; i++) {
		if (s != all_nodes[i].get_steps()) {
			same = false;
		}
	}
	return same;
}

std::vector<std::string> Graaf::get_group_dt_all_nodes_custom(int group)
{
	std::vector<std::string> a;
	if (group >= 0 && group < group_names.size()) {
		for (int i = 0; i < n_nodes; i++) {
			a.push_back(all_nodes[i].get_dt_group_value(group).to_string());
		}
	}
	return a;
}

PyObject* Graaf::get_group_dt_all_nodes_custom_python(int group)
{
	return to_list_vec_string(get_group_dt_all_nodes_custom(group));
}

std::vector<int> Graaf::get_group_dt_all_nodes(int group)
{
	std::vector<int> a;
	if (group >= 0 && group < group_names.size()) {
		for (int i = 0; i < n_nodes; i++) {
			a.push_back((int)all_nodes[i].get_dt_group_value(group).get_val_with_exp(0));
		}
	}
	return a;
}

PyObject* Graaf::get_group_dt_all_nodes_python(int group)
{
	return to_list_vec_int(get_group_dt_all_nodes(group));
}

bool Graaf::get_dt_sign(int node, int group)
{
	if (group >= 0 && group < group_names.size()) {
		if (node >= 0 && node < n_nodes) {
			return all_nodes[node].get_dt_group_value(group).get_sign();
		}
	}
	return true;
}

void to_txt_file(std::vector<unsigned long long int> values, std::string output_path, int width)
{
	std::ofstream myfile(output_path);
	if (myfile.is_open()) {
		for (int i = 0; i < values.size(); i++) {
			myfile << fill_left_with_spaces(std::to_string(values[i]), width);
		}
	}
}

int pos_from_string_value_or_name(std::string current, std::vector<std::string> group_names)
{
	for (int i = 0; i < group_names.size(); i++) {
		if (group_names[i] == current) {
			return i;
		}
	}
	return std::stoi(current);
}

Node from_txt_file(std::string path_to_file, int length, std::vector<std::string> group_names)
{
	Node the_node = Node(length);
	std::string line;
	std::ifstream myfile_node(path_to_file);
	if (myfile_node.is_open())
	{
		getline(myfile_node, line);
		while (getline(myfile_node, line))
		{
			std::string current_values;
			std::size_t position_of_begin = 0;
			std::size_t position_of = line.find("/");
			current_values = line.substr(position_of_begin, position_of - position_of_begin);
			int group1 = pos_from_string_value_or_name(current_values, group_names);

			position_of_begin = position_of + 1;
			position_of = line.find("/", position_of_begin);
			int group2 = pos_from_string_value_or_name(current_values, group_names);

			position_of_begin = position_of + 1;
			position_of = line.find("/", position_of_begin);
			int c_up = std::stoi(line.substr(position_of_begin, position_of - position_of_begin));

			position_of_begin = position_of + 1;
			position_of = line.find("/", position_of_begin);
			int c_down = std::stoi(line.substr(position_of_begin, position_of - position_of_begin));

			position_of_begin = position_of + 1;
			position_of = line.find("/", position_of_begin);
			bool trans = (line.substr(position_of_begin, position_of - position_of_begin)[0] == 'T');

			position_of_begin = position_of + 2;
			position_of = line.find(">", position_of_begin);
			std::size_t position_of_komma = line.find(",", position_of_begin);
			std::vector<int> times;

			if (position_of_begin != position_of) {
				while (position_of > position_of_komma) {
					current_values = line.substr(position_of_begin, position_of_komma - position_of_begin);
					times.push_back(pos_from_string_value_or_name(current_values, group_names));
					position_of_begin = position_of_komma + 1;
					position_of_komma = line.find(",", position_of_begin);
				}
				current_values = line.substr(position_of_begin, position_of - position_of_begin);
				times.push_back(pos_from_string_value_or_name(current_values, group_names));
			}

			position_of_begin = position_of + 3;
			position_of = line.find(">", position_of_begin);
			position_of_komma = line.find(",", position_of_begin);
			std::vector<int> divide;
			if (position_of_begin != position_of) {
				while (position_of > position_of_komma) {
					current_values = line.substr(position_of_begin, position_of_komma - position_of_begin);
					divide.push_back(pos_from_string_value_or_name(current_values, group_names));
					position_of_begin = position_of_komma + 1;
					position_of_komma = line.find(",", position_of_begin);
				}
				current_values = line.substr(position_of_begin, position_of - position_of_begin);
				divide.push_back(pos_from_string_value_or_name(current_values, group_names));
			}
			the_node.add_step_by_values(group1, group2, trans, Custom_number(c_up, c_down), times, divide);
		}
		myfile_node.close();
	}
	return the_node;
}

