from suction import suction_test1
import time


#initialization
suction_test1.init()



suction_test1.control_motor("h")
suction_test1.control_motor("r")
time.sleep(5.00)


suction_test1.control_motor("s")

