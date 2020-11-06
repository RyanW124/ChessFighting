extends Node2D

var rng = RandomNumberGenerator.new()
var background_pre = 'res://Images/Background/'
var game
func _ready():
	rng.randomize()
	game.p1.fighter.position = Vector2(720, 700)
	add_child(game.p1.fighter)
	game.p2.fighter.position = Vector2(1000, 700)
	add_child(game.p2.fighter)
	$Background.texture = load(background_pre+str(rng.randi_range(2, 5))+'.png')
func _process(delta):
	$Show/ColorRect/ShowTime.text = 'Time Left:\n'+str(int(get_parent().get_node('FightTime').time_left))+'s'
	var p = game.p1
	for i in [$p1, $p2]:
		i.get_node('consciousness').text = 'Consciousness: '+str(p.consciousness)
		var bk:ColorRect = i.get_node('bkgrnd')
		var bar:ColorRect = i.get_node('bar')
		bar.rect_position = Vector2(bk.rect_position.x+5, bk.rect_position.y+5)
		bar.rect_size = Vector2((bk.rect_size.x-10)*p.consciousness/100,5)
		
		var bk2:ColorRect = i.get_node('bkgrnd2')
		var bar2:ColorRect = i.get_node('bar2')
		bar2.rect_position = Vector2(bk2.rect_position.x+5, bk2.rect_position.y+5)
		bar2.rect_size = Vector2((bk2.rect_size.x-10)*(1-p.fighter.get_node('AttackCooldown').time_left),5)
		
		var bk3:ColorRect = i.get_node('bkgrnd3')
		var bar3:ColorRect = i.get_node('bar3')
		bar3.rect_position = Vector2(bk3.rect_position.x+5, bk3.rect_position.y+5)
		bar3.rect_size = Vector2((bk3.rect_size.x-10)*(2-p.fighter.get_node('ShootCooldown').time_left)/2.0,5)
		p = game.p2

