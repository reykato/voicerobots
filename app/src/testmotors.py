from motors import Motors
import time
m = Motors(21, 20, 12, 16)

while True:
    m.set_stepper_speed(1,1)
    time.sleep(1)
    m.set_stepper_speed(0,0)
