extends Control


signal chose
func _ready():
	connect("chose", get_owner(), '_on_chose')
func _on_Queen_pressed():
	emit_signal("chose", 0) # Replace with function body.


func _on_Knight_button_up():
	emit_signal("chose", 1) # Replace with function body.


func _on_Bishop_button_up():
	emit_signal("chose", 2) # Replace with function body.


func _on_Rook_button_up():
	emit_signal("chose", 3) # Replace with function body.
