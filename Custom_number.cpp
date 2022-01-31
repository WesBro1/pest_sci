#include "Custom_number.h"

Custom_number::Custom_number()
	:
	value(0.0),
	exponent(0)
{
}

Custom_number::Custom_number(double val, signed char ex)
	:
	value(val),
	exponent(ex)
{
	adjust();
}

Custom_number::Custom_number(long long int val)
{
	value = (double)val;
	exponent = 0;
	adjust();
}

Custom_number::Custom_number(unsigned int val)
{
	value = (double)val;
	exponent = 0;
	adjust();
}

Custom_number::Custom_number(const Custom_number& oth)
{
	value = oth.value;
	exponent = oth.exponent;
}

void Custom_number::adjust()
{
	if (value == 0.0) {
		exponent = 0;
	}
	else {
		while (abs(value) >= 10.0) {
			value /= 10.0;
			exponent++;
		}
		while (abs(value) <= 1.0) {
			value *= 10.0;
			exponent--;
		}
	}
}

void Custom_number::check()
{
	if (exponent < -10) {
		exponent = 0;
		value = 0.0;
	}
}

void Custom_number::change_val(double val)
{
	value = val;
	adjust();
}

void Custom_number::change_exp(signed char ex)
{
	exponent = ex;
}

double Custom_number::get_value() const
{
	return value;
}

signed char Custom_number::get_exp() const
{
	return exponent;
}

double Custom_number::get_val_with_exp(signed char ex) const
{
	double val = value;
	signed char x = exponent;
	while (ex < x) {
		val *= 10.0;
		x--;
	}
	while (ex > x) {
		val /= 10.0;
		x++;
	}
	return val;
}

unsigned int Custom_number::get_value_as_unsignedint() const
{
	return (unsigned int)abs(get_val_with_exp(0));
}

Custom_number Custom_number::operator+(const Custom_number oth) const
{
	signed char ex = oth.exponent;
	Custom_number a = Custom_number(oth.value + get_val_with_exp(ex), ex);
	a.check();
	return a;
}

Custom_number& Custom_number::operator+=(const Custom_number oth)
{
	value += oth.get_val_with_exp(exponent);
	adjust();
	check();
	return *this;
}

Custom_number Custom_number::operator-(const Custom_number oth) const
{
	signed char ex = oth.exponent;
	return Custom_number(oth.value - get_val_with_exp(ex), ex);
}

Custom_number& Custom_number::operator-=(const Custom_number oth)
{
	value -= oth.get_val_with_exp(exponent);
	adjust();
	return *this;
}

Custom_number Custom_number::operator*(const Custom_number oth) const
{
	return Custom_number(oth.value * value, oth.exponent + exponent);
}

Custom_number& Custom_number::operator*=(const Custom_number oth)
{
	value *= oth.value;
	exponent += oth.exponent;
	adjust();
	return *this;
}

Custom_number Custom_number::operator/(const Custom_number oth) const
{
	if (oth.value != 0) {
		return Custom_number(value / oth.value, exponent - oth.exponent);
	}
	else {
		return Custom_number(value, exponent);
	}
}

Custom_number& Custom_number::operator/=(const Custom_number oth)
{
	if (oth.value != 0) {
		value /= oth.value;
		exponent -= oth.exponent;
	}
	adjust();
	return *this;
}

bool Custom_number::operator<(const Custom_number oth) const
{
	return (get_val_with_exp(0) < oth.get_val_with_exp(0));
}

bool Custom_number::operator<=(const Custom_number oth) const
{
	return (get_val_with_exp(0) <= oth.get_val_with_exp(0));
}

bool Custom_number::operator>(const Custom_number oth) const
{
	return (get_val_with_exp(0) > oth.get_val_with_exp(0));
}

bool Custom_number::operator>=(const Custom_number oth) const
{
	return (get_val_with_exp(0) >= oth.get_val_with_exp(0));
}

bool Custom_number::operator==(const Custom_number oth) const
{
	return (exponent == oth.exponent && value == oth.value);
}

std::string Custom_number::to_string() const
{
	std::string val = std::to_string(value);
	val += "E";
	val += std::to_string(exponent);
	return val;
}

std::string Custom_number::to_string_with_exp(signed char ex) const
{
	std::string val = std::to_string(get_val_with_exp(ex));
	val += "E";
	val += std::to_string(ex);
	return val;
}

bool Custom_number::get_sign() const
{
	return (value >= 0);
}