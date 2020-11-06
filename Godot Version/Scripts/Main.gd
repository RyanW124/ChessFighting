extends Node2D
export(String, FILE) var promotion_file
export(String, FILE) var board_file
export(String, FILE) var game_file
export(String, FILE) var fight_file
var size = 50
var board
var game
var legal
var promoting = null
var chess = true
var moving = null
func _ready():
	board = load(board_file).Board.new(self)
	game = load(game_file).Game.new(board)
	$ChessTime.start(game.chess_time)
	$p1/Stats/Timer.start(game.p1.move_time)
func update_board():
	for i in board.squares:
		if i.piece:
			i.piece.node[0].position = Vector2(i.index%8*size+size/2-200, 7.5*size-i.index/8*size-200)+get_node('board1').position
			i.piece.node[1].position = Vector2(7.5*size-i.index%8*size-200, i.index/8*size+size/2-200)+get_node('board2').position
func move(moving, index):
	if moving:
		if index in legal:
			var win = board.move(moving, board.get_square_at(index))
			if win is float or win is int:
				if win == 2:
					$CanvasLayer/check.show()
				elif win == 0.5:
					var temp = load('res://Scenes/UI/Game End.tscn').instance().duplicate()
				
					if game.p1.consciousness>game.p1.consciousness:
						temp.result = 0
					else:
						temp.result = 1
					$CanvasLayer.add_child(temp)
					get_tree().paused = true
			elif win is bool:
				if win:
					var temp = load('res://Scenes/UI/Game End.tscn').instance().duplicate()
				
					if board.winner:
						temp.result = 0
					else:
						temp.result = 1
					$CanvasLayer.add_child(temp)
					get_tree().paused = true
				else:
					pass
			else:
				promoting = win
				$CanvasLayer/ColorRect.show()
			update_board()
			if board.turn:
				$p1/Stats/Timer.start(game.p1.move_time)
				$p2/Stats/Timer.stop()
				game.p2.update_time()
			else:
				$p2/Stats/Timer.start(game.p2.move_time)
				$p1/Stats/Timer.stop()
				game.p1.update_time()
		moving = null
func _process(delta):
	$ShowTime/Label.text = 'Time Left:\n'+str(int($ChessTime.time_left))+'s'
	var p = game.p1
	for i in [$p1/Stats, $p2/Stats]:
		i.get_node('consciousness').text = 'Consciousness: '+str(p.consciousness)
		var bk:ColorRect = i.get_node('Back')
		var bar:ColorRect = i.get_node('Con')
		bar.rect_position = Vector2(bk.rect_position.x+5, bk.rect_position.y+5)
		bar.rect_size = Vector2((bk.rect_size.x-10)*p.consciousness/100,5)
		if i.get_node('Timer').time_left==0:
			i.get_node('time').text = 'Time: '+str(int(p.move_time)/60)+'m '+str(int(p.move_time)%60)+'s'
		else:
			i.get_node('time').text = 'Time: '+str(int(i.get_node('Timer').time_left)/60)+'m '+str(int(i.get_node('Timer').time_left)%60)+'s'
		p = game.p2
	if not chess:
		return
	if Input.is_action_just_pressed("Click") and promoting == null:
		for i in get_tree().get_nodes_in_group('moves'):
			i.queue_free()
		var pos
		var index
		if board.turn:
			
			pos = get_viewport().get_mouse_position()-Vector2(160, 215)
			if pos.x>400 or pos.x<0 or pos.y>400 or pos.y<0:
				return
			index = int(pos.x/50)+(7-int(pos.y/50))*8
		else:
			
			pos = get_viewport().get_mouse_position()-Vector2(880, 215)
			if pos.x>400 or pos.x<0 or pos.y>400 or pos.y<0:
				return
			index = 7-int(pos.x/50)+(int(pos.y/50))*8
		if not board.get_square_at(index):
			return
		if board.get_square_at(index).piece:
			if board.get_square_at(index).piece.color == board.turn:
				legal = []
				for i in board.get_square_at(index).piece.legal_moves():
					var temp := ColorRect.new()
					if board.turn:
						temp.rect_position = Vector2(i.index%8*size+size/2-205, 7.5*size-i.index/8*size-205)+get_node('board1').position
					else:
						temp.rect_position = Vector2(7.5*size-i.index%8*size+515, 0.5*size+i.index/8*size-205)+get_node('board1').position
					temp.rect_size = Vector2(10, 10)
					temp.color = Color(255,0,0)
					add_child(temp)
					temp.add_to_group('moves')
					moving = board.get_square_at(index).piece
					legal.append(i.index)
					
			else:
				move(moving, index)
		else:
			move(moving, index)
				
func _on_chose(type):
	var sq = promoting.square
	for i in promoting.node:
		i.queue_free()
	var temp:int
	
	var node = load('res://Scenes/Piece.tscn').instance().duplicate()
	
	if type == 0:
		promoting = load('res://Scripts/Pieces.gd').Queen.new(promoting.square, promoting.color)
		temp = 5
	elif type == 1:
		promoting = load('res://Scripts/Pieces.gd').Knight.new(promoting.square, promoting.color)
		temp = 3
	elif type == 2:
		promoting = load('res://Scripts/Pieces.gd').Bishop.new(promoting.square, promoting.color)
		temp = 2
	elif type == 3:
		promoting = load('res://Scripts/Pieces.gd').Rook.new(promoting.square, promoting.color)
		promoting.moved = true
		temp = 4
	if not promoting.color:
		temp+=6
	if temp<10:
		node.img = '0'+str(temp)
	else:
		node.img = str(temp)
	var temp_array = []
	node.position = Vector2(promoting.square.index%8*size+size/2-200, 7.5*size-promoting.square.index/8*size-200)+get_node('board1').position
	add_child(node)
	temp_array.append(node)
	node = load('res://Scenes/Piece.tscn').instance().duplicate()
	node.position = Vector2(7.5*size-promoting.square.index%8*size-200, promoting.square.index/8*size+size/2-200)+get_node('board2').position
	if temp<10:
		node.img = '0'+str(temp)
	else:
		node.img = str(temp)
	add_child(node)
	temp_array.append(node)
	$CanvasLayer/ColorRect.hide()
	sq.piece = promoting
	promoting.node = temp_array
	promoting = null
	
func _on_win(winner):
	var temp = load('res://Scenes/UI/Game End.tscn').instance().duplicate()
	temp.result = winner-1
	$CanvasLayer.add_child(temp)
	get_tree().paused = true


func _on_ChessTime_timeout():
	if chess:
		chess = false
		var temp = load(fight_file).instance().duplicate()
		temp.game = game
		$FightTime.start(game.fight_time)
		game.new_fighters()
		$p1/Stats/Timer.stop()
		$p2/Stats/Timer.stop()
		add_child(temp) # Replace with function body.


func _on_Timer1_timeout():
	var temp = load('res://Scenes/UI/Game End.tscn').instance().duplicate()
	temp.result = 1
	$CanvasLayer.add_child(temp)
	get_tree().paused = true # Replace with function body.


func _on_Timer2_timeout():
	var temp = load('res://Scenes/UI/Game End.tscn').instance().duplicate()
	temp.result = 0
	$CanvasLayer.add_child(temp)
	get_tree().paused = true # Replace with function body.


func _on_FightTime_timeout():
	if !chess:
		chess = true
		
		game.p1.update_time()
		game.p2.update_time()
		$ChessTime.start(game.chess_time)
		if board.turn:
			$p1/Stats/Timer.start(game.p1.move_time)
		else:
			$p2/Stats/Timer.start(game.p2.move_time)
		get_node('FightScene').queue_free() # Replace with function body. # Replace with function body.
