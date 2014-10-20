
class FieldWeight:
	def __init__(self, field_n, field_b, weight, upperbound = None):
		self.field_n = field_n
		self.field_b = field_b
		self.weight = weight
		if upperbound is not None:
			self.upperbound = upperbound

def diff_fields(all_fields, fields_weights):
	repeated_fields = []
	for field_weight in fields_weights:
		repeated_fields.append(field_weight.field_b)
	return list(set(all_fields) - set(repeated_fields))