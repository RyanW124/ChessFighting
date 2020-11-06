
static func new_piece(square, num, scene):
	var image_size = 50
	var color:bool
	if 0<=num and num <= 15:
		color = true
	elif 48<=num and num <= 63:
		color = false
	else:
		return null
	var piece
	var node = load('res://Scenes/Piece.tscn').instance().duplicate()
	var temp
	if num in [0, 7, 56, 63]:
		piece = Rook.new(square, color)
		temp = 4
	elif num in [1, 6, 57, 62]:
		piece = Knight.new(square, color)
		temp = 3
	elif num in [2, 5, 58, 61]:
		piece = Bishop.new(square, color)
		temp = 2
	elif (8<=num and num <= 15) or (48<=num and num <= 55):
		piece = Pawn.new(square, color)
		temp = 1
	elif num in [3, 59]:
		piece = Queen.new(square, color)
		temp = 5
	elif num in [4, 60]:
		piece = King.new(square, color)
		temp = 6
	if not color:
		temp+=6
	if temp<10:
		node.img = '0'+str(temp)
	else:
		node.img = str(temp)
	var temp_array = []
	node.position = Vector2(num%8*image_size+image_size/2-200, 7.5*image_size-num/8*image_size-200)+scene.get_node('board1').position
	scene.add_child(node)
	temp_array.append(node)
	node = load('res://Scenes/Piece.tscn').instance().duplicate()
	node.position = Vector2(7.5*image_size-num%8*image_size-200, num/8*image_size+image_size/2-200)+scene.get_node('board2').position
	if temp<10:
		node.img = '0'+str(temp)
	else:
		node.img = str(temp)
	scene.add_child(node)
	temp_array.append(node)
	piece.node = temp_array
	return piece
class Piece:
	var square
	var color
	var image
	var node
	
	func _init(square, color):
		self.square = square
		self.color = color
	
class King extends Piece:
	var moved = false
	var short
	var long
	var type = 0
	func _init(square, color).(square, color):
		pass
	func get_checks():
		return square.board.total_legal_moves(!self.color)

	func attacking():
		var legal = []
		var index = self.square.index
		for i in [-1, 1, 8, 7, 9, -8, -7, -9]:
			var square = self.square.board.get_square_at(self.square.index+i)
			var cont = false
			
			if not square:
				continue
			if ((self.square.index+i%8)/8==self.square.index/8 and abs(i)!=7) or (i==7 and index%8!=0) or (i==-7 and index%8!=7):
				legal.append(square)
		
		return legal
	func legal_moves():
		var legal = []
		var index = self.square.index
		for i in [-1, 1, 8, 7, 9, -8, -7, -9]:
			var square = self.square.board.get_square_at(self.square.index+i)
			var cont = false
			
			if not square:
				continue
			if ((self.square.index+i%8)/8==self.square.index/8 and abs(i)!=7) or (i==7 and index%8!=0) or (i==-7 and index%8!=7):
				if not square.piece:
					legal.append(square)
				else:
					if square.piece.color!=self.color:
						legal.append(square)
		if not self.moved and not self.short.moved:
			if not self.square.board.get_square_at(index+1).piece and not self.square.board.get_square_at(index+2).piece:
				if not self.square.board.get_square_at(index+1) in self.square.board.total_legal_moves(!self.color) and not self.square.board.get_square_at(index+2) in self.square.board.total_legal_moves(!self.color):
					legal.append(self.square.board.get_square_at(index+2))
		if not self.moved and not self.long.moved:
			if not self.square.board.get_square_at(index-1).piece and not self.square.board.get_square_at(index-2).piece:
				if not self.square.board.get_square_at(index-1) in self.square.board.total_legal_moves(!self.color) and not self.square.board.get_square_at(index-2) in self.square.board.total_legal_moves(!self.color):
					legal.append(self.square.board.get_square_at(index-2))
		var l = legal.duplicate()
		for sq in l:
			
			var holder
			if sq.piece:
				holder = sq.piece
				sq.piece = null
				
			self.square.piece = null
			sq.piece = self
			self.square = sq
			
			if self.color:
				if self.square.board.p1_king.square in self.square.board.total_legal_moves(false):
					legal.erase(sq)
			else:
				if self.square.board.p2_king.square in self.square.board.total_legal_moves(true):
					legal.erase(sq)
			
			self.square = self.square.board.get_square_at(index)
			sq.piece = holder
			self.square.piece = self
		return legal
		
class Queen extends Piece:
	var type = 1
	func _init(square, color).(square, color):
		pass
	func attacking():
		var legal = []
		var pos = Vector2(self.square.index/8, self.square.index%8)
		var index = self.square.index
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+8*i*sig)
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+9*i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+7*i*sig)
				if (index-i*sig)/8 != index/8 or index<i*sig:
					break
				if square:

					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		return legal
	func legal_moves():
		var legal = []
		var pos = Vector2(self.square.index/8, self.square.index%8)
		var index = self.square.index
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+8*i*sig)
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+9*i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+7*i*sig)
				if (index-i*sig)/8 != index/8 or index<i*sig:
					break
				if square:

					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		var l = legal.duplicate()
		for sq in l:
			
			var holder
			if sq.piece:
				holder = sq.piece
				sq.piece = null
				
			self.square.piece = null
			sq.piece = self
			self.square = sq
			
			if self.color:
				if self.square.board.p1_king.square in self.square.board.total_legal_moves(false):
					legal.erase(sq)
			else:
				if self.square.board.p2_king.square in self.square.board.total_legal_moves(true):
					legal.erase(sq)
			
			self.square = self.square.board.get_square_at(index)
			sq.piece = holder
			self.square.piece = self
			
		return legal
	
class Pawn extends Piece:
	var moved = false
	var type = 2
	func _init(square, color).(square, color):
		pass
	func attacking():
		var legal = []
		var moves = [7, 9]
		var index = self.square.index
		for x in moves:
			var i = x
			if not self.color:
				i = -i
			
			var square = self.square.board.get_square_at(self.square.index+i)
			if not square:
				continue
			if i >0:
				if (x==7 and index%8==0) or (x==9 and index%8==7):
					continue
			else:
				if (x==9 and index%8==0) or (x==7 and index%8==7):
					continue
			legal.append(square)
		return legal
	func legal_moves():
		var legal = []
		var moves = [8, 7, 9]
		var index = self.square.index
		if not moved:
			moves.append(16)
		var skip = false
		for x in moves:
			var i = x
			if not self.color:
				i = -i
			
			var square = self.square.board.get_square_at(self.square.index+i)
			if not square:
				continue
			if x==16 and skip:
				continue
			if x in [8, 16] and square.piece:
				if x==8:
					skip = true
				continue
			if x in [7,9]:
				if square.piece:
					if square.piece.color==self.color:
						continue
				else:
					continue
			if i >0:
				if (x==7 and index%8==0) or (x==9 and index%8==7):
					continue
			else:
				if (x==9 and index%8==0) or (x==7 and index%8==7):
					continue
			if not square.piece:
				legal.append(square)
			else:
				if square.piece.color!=self.color:
					legal.append(square)
		var l = legal.duplicate()
		for sq in l:
			
			var holder
			if sq.piece:
				holder = sq.piece
				sq.piece = null
				
			self.square.piece = null
			sq.piece = self
			self.square = sq
			
			if self.color:
				if self.square.board.p1_king.square in self.square.board.total_legal_moves(false):
					legal.erase(sq)
			else:
				if self.square.board.p2_king.square in self.square.board.total_legal_moves(true):
					legal.erase(sq)
			
			self.square = self.square.board.get_square_at(index)
			sq.piece = holder
			self.square.piece = self
		moves = self.square.board.moves
		if len(moves)>2:
			
			if abs(moves[-1][1]-moves[-1][0])==16:
				
				if self.square.index/8 == moves[-1][1]/8 and moves[-1][-1].type == 2:
					if abs(self.square.index%8-moves[-1][1]%8)==1:
						if not self.color:
							if not self.square.board.get_square_at(moves[-1][1]%8+16).piece:
								legal.append(self.square.board.get_square_at(moves[-1][1]%8+16))
						else:
							if not self.square.board.get_square_at(moves[-1][1]%8+40).piece:
								legal.append(self.square.board.get_square_at(moves[-1][1]%8+40))
		return legal
	
class Knight extends Piece:
	var type = 3
	func _init(square, color).(square, color):
		pass
	func attacking():
		var index = self.square.index
		var legal = []
		for sig in [-1, 1]:
			for i in [6, 10, 15, 17]:
				var square = self.square.board.get_square_at(index+i*sig)
				if sig ==1:
					if (i==15 and index%8==0) or (i==17 and index%8==7) or (i==6 and index%8<=1) or (i==10 and index%8>=6):
						continue
				else:
					if (i==17 and index%8==0) or (i==15 and index%8==7) or (i==10 and index%8<=1) or (i==6 and index%8>=6):
						continue
				if square:
					legal.append(square)
		return legal
	func legal_moves():
		var index = self.square.index
		var legal = []
		for sig in [-1, 1]:
			for i in [6, 10, 15, 17]:
				var square = self.square.board.get_square_at(index+i*sig)
				if sig ==1:
					if (i==15 and index%8==0) or (i==17 and index%8==7) or (i==6 and index%8<=1) or (i==10 and index%8>=6):
						continue
				else:
					if (i==17 and index%8==0) or (i==15 and index%8==7) or (i==10 and index%8<=1) or (i==6 and index%8>=6):
						continue
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
		var l = legal.duplicate()
		for sq in l:
			
			var holder
			if sq.piece:
				holder = sq.piece
				sq.piece = null
				
			self.square.piece = null
			sq.piece = self
			self.square = sq
			
			if self.color:
				if self.square.board.p1_king.square in self.square.board.total_legal_moves(false):
					legal.erase(sq)
			else:
				if self.square.board.p2_king.square in self.square.board.total_legal_moves(true):
					legal.erase(sq)
			
			self.square = self.square.board.get_square_at(index)
			sq.piece = holder
			self.square.piece = self
		return legal
class Bishop extends Piece:
	var type = 4
	func _init(square, color).(square, color):
		pass
	func attacking():
		var legal = []
		var pos = Vector2(self.square.index/8, self.square.index%8)
		var index = self.square.index
		
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+9*i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+7*i*sig)
				if (index-i*sig)/8 != index/8 or index<i*sig:
					break
				if square:

					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		return legal
	func legal_moves():
		var legal = []
		var pos = Vector2(self.square.index/8, self.square.index%8)
		var index = self.square.index
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+9*i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+7*i*sig)
				if (index-i*sig)/8 != index/8 or index<i*sig:
					break
				if square:

					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		var l = legal.duplicate()
		for sq in l:
			
			var holder
			if sq.piece:
				holder = sq.piece
				sq.piece = null
				
			self.square.piece = null
			sq.piece = self
			self.square = sq
			
			if self.color:
				if self.square.board.p1_king.square in self.square.board.total_legal_moves(false):
					legal.erase(sq)
			else:
				if self.square.board.p2_king.square in self.square.board.total_legal_moves(true):
					legal.erase(sq)
			
			self.square = self.square.board.get_square_at(index)
			sq.piece = holder
			self.square.piece = self
		return legal
	
class Rook extends Piece:
	var moved = false
	var type = 5
	func _init(square, color).(square, color):
		pass
	func attacking():
		var legal = []
		var pos = Vector2(self.square.index/8, self.square.index%8)
		var index = self.square.index
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+8*i*sig)
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						legal.append(square)
						break
				else:
					break
		
		return legal
	func legal_moves():
		var legal = []
		var pos = Vector2(self.square.index/8, self.square.index%8)
		var index = self.square.index
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+8*i*sig)
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		for sig in [-1, 1]:
			for i in range(1, 8):
				var square = self.square.board.get_square_at(index+i*sig)
				if (index+i*sig)/8 != index/8:
					break
				if square:
					
					if not square.piece:
						legal.append(square)
					else:
						if square.piece.color!=self.color:
							legal.append(square)
						break
				else:
					break
		var l = legal.duplicate()
		for sq in l:
			
			var holder
			if sq.piece:
				holder = sq.piece
				sq.piece = null
				
			self.square.piece = null
			sq.piece = self
			self.square = sq
			
			if self.color:
				if self.square.board.p1_king.square in self.square.board.total_legal_moves(false):
					legal.erase(sq)
			else:
				if self.square.board.p2_king.square in self.square.board.total_legal_moves(true):
					legal.erase(sq)
			
			self.square = self.square.board.get_square_at(index)
			sq.piece = holder
			self.square.piece = self
		return legal
	
