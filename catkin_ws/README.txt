DAFT PUNKS MASTER DOCUMENTATION

Packages:
	limit_switch_feedback - DEPRECATED, package to read digital signals from Raspberry Pi GPIO ports
		msg:
			LimitSwitchStates.msg - message with a boolean associated with each limit switch, indicating whether they are pressed
		scripts:
			limit_switch_state_publisher.py - script which takes in the state of each limit switch and publishes them as LimitSwitchStates messages on the 'limit_switch_states_pub' topic 
	locomotion_algorithm - DEPRECATED, package to synthsize limit switch input and user input to determine the next motor commands
		msg:
			MotorCommands.msg - message with a string associated with each linear actuator and stepper motor which will be interpeted by a motor control node to command the corresponding motor
		scripts:
			motor_commands_publisher.py - script which subscribes to the 'limit_switch_states_pub' and 'user_input_pub' topics and uses their data to determine the next motion for the robot to take, which is published on the 'motor_command_pub' topic
	motor_control - package which communcates with the motor control arduinos over serial to command the motors, based on user input
		scripts:
			motor_control_open_loop.py - script which subscribes to the user_input_pub topic and uses its data to determine the actions to be taken by the motors. Each message is processed as a "step," that is, the robot will return to a stable configuration before accepting new input
	user_input - package which reads in the user input device state from the ROS Joy package translates it into a command for the robot
		msg:
			UserInput.msg - message consisting of two fields. The dir string indicates whether the robot will step forwards, backwards, or turn left or right. The speed float indicates whether the step will be completed with a large or short step angle
		scripts:
			user_input_pub_analog_input.py - script which subscribes to the ROS joy topic and interprets its data on the left analog joystick to publish the user_input_pub topic.
			user_input_pub_digital_input.py - script which subscribes to the ROS joy topic and interprets its data on the d-pad and A and B buttons to publish the user_input_pub topic.
			
HOW TO RUN
	1) In the terminal, in the ~/catkin_ws/ directory, run 'catkin_make', then 'source ./devel/setup.bash', then 'roscore'.
	2) Open a new terminal in the ~/catkin_ws/ directory, run 'source ./devel/setup.bash', then 'rosrun joy joy_node _autorepeat_rate:=1.0' to begin publishing the joystick state.
	3) Open a new terminal in the ~/catkin_ws/ directory, run 'source ./devel/setup.bash', then 'rosrun user_input user_input_pub_digital_input.py' or 'rosrun user_input user_input_pub_analog_input.py' to control the robot with the d-pad or left joystick.
	4) With power disconnected from the motors, ensure all legs are perpendicular to the robot frame.
	5) Open a new terminal in the ~/catkin_ws/ directory, run 'source ./devel/setup.bash', then rosrun motor_control motor_control_open_loop.py to begin communication with the Arduinos. When the motor are powered, they will begin to respond to user input.
