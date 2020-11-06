extends Area2D

var parent
var dir
export var speed:float
signal win
func _ready():
	connect("win", get_parent().get_parent(), '_on_win')
	dir = parent.direction
	$'1'.flip_h = dir
	$'2'.flip_h = dir
	position = parent.position
	if parent.player:
		$"1".show()
		$"2".hide()
	else:
		$"2".show()
		$"1".hide()
func _process(delta):
	if dir:
		position.x -= speed
	else:
		position.x += speed

func _on_Bullet_body_entered(body):
	if body.is_in_group('Wall'):
		queue_free()
	if body == parent.oppo.fighter:
		parent.oppo.consciousness-=3
		if parent.oppo.consciousness<=0:
			var i = get_parent().get_node('p'+parent.oppo.fighter.string)
			i.get_node('consciousness').text = 'Consciousness: 0'
			var bar:ColorRect = i.get_node('bar')
			bar.rect_size = Vector2(0,0)
			emit_signal("win", int(parent.string))
		queue_free()
