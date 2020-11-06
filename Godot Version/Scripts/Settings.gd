extends Control

var can_change_key = false
var action_string
enum ACTIONS {jump1, left1, right1, attack1, shoot1}
enum ACTIONS2 {jump2, left2, right2, attack2, shoot2}
func _ready():
	_set_keys()  
  
func _set_keys():
#	for i in ACTIONS:
#		print(str(i))
	for j in ACTIONS:
		get_node("Panel/VBoxContainer/" + str(j) + "/Button").set_pressed(false)
		if !InputMap.get_action_list(j).empty():
			get_node("Panel/VBoxContainer/" + str(j) + "/Button").set_text(InputMap.get_action_list(j)[0].as_text())
		else:
			get_node("Panel/VBoxContainer/" + str(j) + "/Button").set_text("Null")
	for j in ACTIONS2:
		get_node("Panel/VBoxContainer2/" + str(j) + "/Button").set_pressed(false)
		if !InputMap.get_action_list(j).empty():
			get_node("Panel/VBoxContainer2/" + str(j) + "/Button").set_text(InputMap.get_action_list(j)[0].as_text())
		else:
			get_node("Panel/VBoxContainer2/" + str(j) + "/Button").set_text("Null")

func _mark_button(string):
	can_change_key = true
	action_string = string
	
	for j in ACTIONS:
		if j != string:
			get_node("Panel/VBoxContainer/" + str(j) + "/Button").set_pressed(false)
func _mark_button2(string):
	can_change_key = true
	action_string = string
	
	for j in ACTIONS2:
		if j != string:
			get_node("Panel/VBoxContainer2/" + str(j) + "/Button").set_pressed(false)

func _input(event):
	if event is InputEventKey: 
		if can_change_key:
			_change_key(event)
			can_change_key = false
			
func _change_key(new_key):
	#Delete key of pressed button
	if !InputMap.get_action_list(action_string).empty():
		InputMap.action_erase_event(action_string, InputMap.get_action_list(action_string)[0])
	
	#Check if new key was assigned somewhere
	for i in ACTIONS:
		if InputMap.action_has_event(i, new_key):
			InputMap.action_erase_event(i, new_key)
	for i in ACTIONS2:
		if InputMap.action_has_event(i, new_key):
			InputMap.action_erase_event(i, new_key)
	#Add new Key
	InputMap.action_add_event(action_string, new_key)
	
	_set_keys()
	


func _on_jump1_button_up():
	_mark_button2("jump1") # Replace with function body.


func _on_left1():
	_mark_button2("left1") # Replace with function body.


func _on_right1():
	_mark_button2("right1") # Replace with function body.


func _on_shoot1():
	_mark_button2("shoot1") # Replace with function body.


func _on_attack1():
	_mark_button2("attack1") # Replace with function body.


func _on_Button_button_up():
	get_tree().change_scene("res://Scenes/StartScene.tscn") # Replace with function body.


func _on_attack2():
	_mark_button("attack2") # Replace with function body.


func _on_shoot2():
	_mark_button("shoot2") # Replace with function body.


func _on_right2():
	_mark_button("right2") # Replace with function body.


func _on_left2():
	_mark_button("left2") # Replace with function body.


func _on_jump2_button_up():
	_mark_button("jump2") # Replace with function body.
