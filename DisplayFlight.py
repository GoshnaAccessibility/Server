class DisplayFlight:
	def __init__(self, id, airline, airline_short, dest_short, number, gate, departure):
		self.id = id
		self.airline = airline
		self.airline_short = airline_short
		self.dest_short = dest_short
		self.number = number
		self.gate = gate
		self.departure = departure

	def to_json(self):
		return {
			'id': self.id,
			'airline': self.airline,
			'airline_short': self.airline_short,
			'dest_short': self.dest_short,
			'number': self.number,
			'gate': self.gate,
			'departure': self.departure
		}
