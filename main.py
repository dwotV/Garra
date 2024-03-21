from Robot.Garra import Garra

rb= Garra()
rb.conecta()
#rb.agarra()
# rb.suelta()
# rb.mover(10,5)
# rb.agarra()
# rb.resetPosition()
# rb.mover(3,1)
# rb.suelta()
rb.saludar()
rb.mover(6,1)
rb.agarra()
rb.resetPosition()
rb.mover(6,4)
rb.suelta()

# for i in range(9):
#     rb.mover(i+1,3)
#     rb.agarra()
#     rb.resetPosition()
#     rb.mover(i+2,3)
#     rb.suelta()
#     rb.resetPosition