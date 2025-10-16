class Player:
name = "Guest"
def greet() { print("Hello,", self.name) }
+++

def main() {
    print("Creating player instance...")
    player = Player()
    print("Player created successfully")
    
    print("Calling greet method...")
    player.greet()
    
    print("Setting new name...")
    player.name = "Alice"
    print("Name set")
    
    print("Calling greet again...")
    player.greet()
}
