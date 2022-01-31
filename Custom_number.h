#pragma once
#include <string>

class Custom_number
{
public:
	Custom_number();
	Custom_number(double val, signed char ex);
	Custom_number(long long int val);
	Custom_number(unsigned int val);
	Custom_number(const Custom_number& oth);
	~Custom_number() = default;
	void adjust();
	void change_val(double val);
	void change_exp(signed char ex);
	double get_value() const;
	signed char get_exp() const;
	double get_val_with_exp(signed char ex) const;
	unsigned int get_value_as_unsignedint() const;
	bool get_sign() const;
	void check();
	Custom_number operator+(const Custom_number) const;
	Custom_number& operator+=(const Custom_number);
	Custom_number operator-(const Custom_number) const;
	Custom_number& operator-=(const Custom_number);
	Custom_number operator*(const Custom_number) const;
	Custom_number& operator*=(const Custom_number);
	Custom_number operator/(const Custom_number) const;
	Custom_number& operator/=(const Custom_number);
	bool operator<(const Custom_number) const;
	bool operator<=(const Custom_number) const;
	bool operator>(const Custom_number) const;
	bool operator>=(const Custom_number) const;
	bool operator==(const Custom_number) const;
	std::string to_string() const;
	std::string to_string_with_exp(signed char ex) const;


private:
	double value;
	signed char exponent;
};