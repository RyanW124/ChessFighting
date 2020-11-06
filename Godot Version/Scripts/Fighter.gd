extends KinematicBody2D

export var gravity:float
export var speed:float
export var jumppower:float
var parent
var oppo
var direction
var player = true
var vel:Vector2
var animate:AnimatedSprite
var string
var hit =false
var rect:Rect2
signal win
func _ready():
	connect("win", get_parent().get_parent(), '_on_win')
	rect = Rect2(position-Vector2(19, 28)/2, Vector2(19, 28))
	if player:
		string = '1'
		animate = $player1
		$player2.hide()
	else:
		animate = $player2
		string = '2'
		$CollisionShape2D.position.y-=7
		$player1.hide()
	direction = false
	oppo = parent.oppo
	animate.play('Idle')
func _process(delta):
#	rect.size = Vector2(animate.frames.get_frame(animate.animation, animate.frame).get_size())
	if direction:
		if player:
			rect.position = position-Vector2(192, 76)
			rect.size = Vector2(226, 142)
		else:
			rect.position = position-Vector2(202, 28)
			rect.size = Vector2(250, 160)
	else:
		if player:
			rect.position = position-Vector2(30, 76)
			rect.size = Vector2(226, 142)
		else:
			rect.position = position-Vector2(48, 112)
			rect.size = Vector2(250, 160)
#	rect.size = Vector2(19, 28)
	rect.position = position-rect.size/2
func _physics_process(delta):
	vel.x=0
	if Input.is_action_pressed("left"+string):
		if not animate.animation in ['Right', 'Attack', 'Shoot']:
			animate.play('Right')
		vel.x-=speed
	elif Input.is_action_pressed("right"+string):
		if not animate.animation in ['Right', 'Attack', 'Shoot']:
			animate.play('Right')
		vel.x+=speed
	else:
		if not animate.animation in ['Idle', 'Attack', 'Shoot']:
			animate.play('Idle')
	if vel.x>0:
		direction = false
	elif vel.x<0:
		direction = true
	if vel.y>0:
		if not animate.animation in ['Fall', 'Attack', 'Shoot']:
			animate.play('Fall')
	elif vel.y<0:
		if not animate.animation in ['Jump', 'Attack', 'Shoot']:
			animate.play('Jump')
	animate.flip_h = direction
	
	vel.y+=gravity

	
	vel = move_and_slide(vel, Vector2.UP)
	if Input.is_action_just_pressed("shoot"+string) and $ShootCooldown.time_left==0:
		var temp = load('res://Scenes/Bullet.tscn').instance().duplicate()
		temp.parent = self
		animate.play('Shoot')
		$ShootCooldown.start(2)
		get_parent().add_child(temp)
	if Input.is_action_just_pressed("attack"+string) and $AttackCooldown.time_left==0:
		animate.play('Attack')
		$AttackCooldown.start(1)
		hit = true
	if animate.animation == 'Attack' and hit:
		if rect.has_point(oppo.fighter.position):
			oppo.consciousness-=5
			if oppo.consciousness<=0:
				var i = get_parent().get_node('p'+oppo.fighter.string)
				i.get_node('consciousness').text = 'Consciousness: 0'
				var bar:ColorRect = i.get_node('bar')
				bar.rect_size = Vector2(0,0)
				emit_signal("win", int(string))
			hit = false
	if is_on_floor():
		if Input.is_action_pressed("jump"+string):
			vel.y-=jumppower
func collide(obj)->bool:
	for i in get_slide_count():
		if get_slide_collision(i).collider == obj:
			return true
	return false

func _on_player1_animation_finished():
	animate.play('Idle')
	


func _on_player2_animation_finished():
	animate.play('Idle') # Replace with function body.
