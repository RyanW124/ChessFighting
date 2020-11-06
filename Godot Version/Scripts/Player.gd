

class Player:
	var consciousness = 100
	var time = 300
	var fighter
	var move_time
	var oppo
	func _init(fighter):
		self.fighter = fighter
		self.fighter.parent = self
		self.update_time()
	func update_time():
		self.move_time = int(self.consciousness*0.3)
		if self.move_time<5:
			self.move_time=5
		if self.move_time>self.time:
			self.move_time = self.time
