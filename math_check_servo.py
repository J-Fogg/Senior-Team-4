from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
servo_channel = 7
center_of_cones = 320
servo = 90

def servo_control(center_of_cones):
    global servo
    max_step_size = 15
    center_scaled = (center_of_cones-320) # -320 to 320
    
    normalized_scale = (center_scaled)/320 # scale -1 to 1
    step_p = (normalized_scale* -max_step_size)
    servo += step_p
    kit.servo[servo_channel].angle = servo
    print(servo)

def main():
    servo_control(center_of_cones)

if __name__=="__main__":
    main()


        