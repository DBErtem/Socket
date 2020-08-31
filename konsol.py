import pygame

pygame.init()

j = pygame.joystick.Joystick(0)
j.init()


try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                #print("Button Pressed")
                if j.get_button(0):
                    print("'e bastın")
                    #ON OFF

                if j.get_button(1):
                    print("Yuvarlak'a bastın")
                if j.get_button(2):
                    print("Üçgen'e bastın")
                if j.get_button(3):
                    print("Kare'ye bastın")
                if j.get_button(4):
                    print("L1'ye bastın")
                if j.get_button(5):
                    print("R1'ye bastın")
                if j.get_button(6):
                    print("L2'e bastın")
                if j.get_button(7):
                    print("R2'e bastın")
                if j.get_button(8):
                    print("Select'e bastın")
                if j.get_button(9):
                    print("Start'a bastın")
                if j.get_button(10):
                    print("Sol analog'a bastın")
                if j.get_button(11):
                    print("Sağ analog'a bastın")

            if event.type == pygame.JOYAXISMOTION:
                print(event.dict)
            #     print(event.value)
            #     print(event.axis)
            #     #print(event.dict) = print(event.joy, event.axis, event.value)
                
            # if event.type == pygame.JOYBALLMOTION:
            #     print(event.dict, event.joy, event.ball, event.rel)
            # if event.type == pygame.JOYBUTTONDOWN:
            #     print(event.dict, event.joy, event.button, 'pressed')
            # if event.type == pygame.JOYBUTTONUP:
            #     print(event.dict, event.joy, event.button, 'released')
            
            if event.type == pygame.JOYHATMOTION:
                print(event.dict)
                #print(event.dict) = print(event.joy, event.hat, event.value)

            # elif event.type == pygame.JOYBUTTONUP:
            #     print("Button Released")

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()