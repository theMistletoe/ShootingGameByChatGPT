import pyxel
import random

class MyGame:
    def __init__(self):
        pyxel.init(160, 120, title="My Pyxel Game")
        pyxel.load("my_resource.pyxres")  # Load your game assets
        self.x = 0
        self.y = 20
        self.direction = 1  # 1 for right, -1 for left
        self.move_speed = 2
        self.beams = []  # List to store active beams
        pyxel.run(self.update, self.draw)

    def update(self):
        # Move character in the current direction
        self.x += self.direction * self.move_speed
        
        # Change direction if the character reaches the edge of the screen
        if self.x > pyxel.width - 16:  # Assuming the character sprite is 16 pixels wide
            self.direction = -1
        elif self.x < 0:
            self.direction = 1

        # Randomly emit a beam
        if random.randint(0, 20) == 0:  # Adjust the probability as needed
            self.emit_beam()

        # Update beams
        for beam in self.beams[:]:
            beam['y'] += 2  # Move the beam downwards
            if beam['y'] > pyxel.height:  # Remove the beam if it goes off-screen
                self.beams.remove(beam)

    def emit_beam(self):
        # Add a new beam to the list
        self.beams.append({'x': self.x + 8, 'y': self.y})

    def draw(self):
        pyxel.cls(0)
        # Draw the character
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)

        # Draw all beams
        for beam in self.beams:
            pyxel.line(beam['x'], beam['y'], beam['x'], beam['y'] + 10, 7)  # Draw a line for the beam

MyGame()