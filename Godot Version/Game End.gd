extends Control

var result
var col

func _ready():
	if result == 0:
		col = Color(0,0,255)
		$Label.text = 'Blue Won'
	elif result == 0.5:
		col = Color(255,0,255)
		$Label.text = 'Tie'
	elif result == 1:
		col = Color(255,0,0)
		$Label.text = 'Red Won'
	$Border.color = col
	$Label.set("custom_colors/font_color", col)
