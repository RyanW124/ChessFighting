
class Game:
	var board
	var rounds = 1
	
	var p1
	var p2
	var winner = null
	var fight_time = 30
	var chess_time = 60
	func _init(board):
		p1 = load('res://Scripts/Player.gd').Player.new(load('res://Scenes/Fighter.tscn').instance().duplicate())
		p2 = load('res://Scripts/Player.gd').Player.new(load('res://Scenes/Fighter.tscn').instance().duplicate())
		p1.oppo = p2
		p2.oppo = p1
		p2.fighter.player = false
		self.board = board
	func new_fighters():
		p1.fighter = load('res://Scenes/Fighter.tscn').instance().duplicate()
		p2.fighter = load('res://Scenes/Fighter.tscn').instance().duplicate()
		p2.fighter.player = false
		p1.fighter.parent = p1
		p2.fighter.parent = p2
