

class Board:
	var squares = []
	var winner
	var turn := true
	var scene
	var p1_king
	var moves = []
	var p2_king
	
	func _init(scene):
		self.scene = scene
		for i in range(64):
			
			var piece = load('res://Scripts/Pieces.gd').new_piece(null, i, scene)
			var square = load('res://Scripts/Squares.gd').Square.new(self, i, piece)
			
			if piece:
				piece.square = square
			if i ==4:
				p1_king = piece
			if i ==60:
				p2_king = piece
			self.squares.append(square)
		p1_king.long = self.get_square_at(0).piece
		p1_king.short = self.get_square_at(7).piece
		p2_king.long = self.get_square_at(56).piece
		p2_king.short = self.get_square_at(63).piece
	func king_legal(color:bool):
		pass
	func total_legal_moves(color):
		var l = []
		for i in self.squares:
			if i.piece:
				if i.piece.color==color:
					l+=i.piece.attacking()
		return l
	func threefold_rep():
		if self.moves.size()<2:
			return
		var final = self.moves[self.moves.size()-1]
		var index = self.moves.slice(0, self.moves.size()-2).find_last(final)
		if index!=-1:
			var rep = self.moves.slice(index+1, self.moves.size()-1)
			var rep3 = []
			for i in range(2):
				rep3+=rep
			for i in range(len(self.moves)-len(rep)*2):
				if self.moves.slice(i, i+len(rep)*2-1) == rep3:
					return true
		return false
			
	func move(piece, square):
		var prev_index = piece.square.index
		if piece is load('res://Scripts/Pieces.gd').Pawn:
			if abs(square.index-prev_index) in [7, 9] and not square.piece:
				var sq = self.get_square_at(square.index-(square.index-prev_index)/abs(square.index-prev_index)*8)
				for i in sq.piece.node:
					i.queue_free()
				sq.piece = null
			if piece.color:
				if prev_index/8 == 7:
					return 1
			else:
				if prev_index/8 == 0:
					return 1
		if square.piece:
			
			for i in square.piece.node:
				i.queue_free()
			square.piece = null
		if piece is load('res://Scripts/Pieces.gd').King:
			if piece.square.index-square.index==2:
				self.get_square_at(piece.square.index-1).piece = self.get_square_at(piece.square.index-4).piece
				self.get_square_at(piece.square.index-4).piece = null
				self.get_square_at(piece.square.index-1).piece.square = self.get_square_at(piece.square.index-1)
			elif piece.square.index-square.index==-2:
				self.get_square_at(piece.square.index+1).piece = self.get_square_at(piece.square.index+3).piece
				self.get_square_at(piece.square.index+3).piece = null
				self.get_square_at(piece.square.index+1).piece.square = self.get_square_at(piece.square.index+1)
		
		piece.square.piece = null
		square.piece = piece
		piece.square = square
		
		if piece is load('res://Scripts/Pieces.gd').Pawn and not piece.moved:
			piece.moved = true
		elif piece is load('res://Scripts/Pieces.gd').King and not piece.moved:
			piece.moved = true
		elif piece is load('res://Scripts/Pieces.gd').Rook and not piece.moved:
			piece.moved = true
		self.turn=!self.turn
		
		if self.p1_king.legal_moves() ==[] and self.p1_king.square in self.total_legal_moves(false):
			self.winner = false
			return true
		if self.p2_king.legal_moves() ==[] and self.p2_king.square in self.total_legal_moves(true):
			self.winner = true
			return true
		
		
		var stale = true
		for i in self.squares:
			if i.piece:
				if i.piece.color:
					if i.piece.legal_moves()!=[]:
						stale = false
						break
		if stale:
			self.winner = 0.5
			return true
		stale = true
		for i in self.squares:
			if i.piece:
				if not i.piece.color:
					if i.piece.legal_moves()!=[]:
						stale = false
						break
		if stale:
			self.winner = 0.5
			return true
		self.moves.append([prev_index,square.index, piece])
		if self.threefold_rep():
			return 0.5
		if piece is load('res://Scripts/Pieces.gd').Pawn:
			
			if piece.color:
				if piece.square.index/8 == 7:
					return piece
			else:
				if piece.square.index/8 == 0:
					return piece
		if self.p2_king.square in self.total_legal_moves(true) or self.p1_king.square in self.total_legal_moves(false):
			return 2
		return false
	func get_square_at(num):
		if 0<=num and num<=63:
			return self.squares[num]
		return null
