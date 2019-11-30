import arcade
import random

SCREEN_WIDTH = 1850
SCREEN_HEIGHT = 900
SPRITE_SCALING_PLAYER1 = 0.2
SPRITE_SCALING_PLAYER2 = 0.3
SPRITE_SCALING_COIN = 0.06
COIN_COUNT = 50
MOVEMENT_SPEED = 15

class Fred(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.PINK_LACE)
        self.set_mouse_visible(False)
        self.player_list = None
        self.coin_list = None
        self.score1 = 0
        self.score2 = 0
        self.player1_sprite = None
        self.player2_sprite = None
        self.sound_bg = None
        self.sound_collect_coin = None
        self.physics_engine1 = None
        self.physics_engine2 = None
        self.wall_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Score
        self.score1 = 0
        self.score2 = 0

        # Sound
        self.sound_bg = arcade.load_sound("sounds/jack_in_the_box_fast.wav")
        self.sound_collect_coin = arcade.load_sound("sounds/collect_coin.wav")
        arcade.play_sound(self.sound_bg)

        # Set up the players
        self.player1_sprite = arcade.Sprite("images/fish.png", SPRITE_SCALING_PLAYER1)
        self.player1_sprite.center_x = 50  # Starting position
        self.player1_sprite.center_y = 50
        self.player_list.append(self.player1_sprite)
        self.player2_sprite = arcade.Sprite("images/green mushroom.png", SPRITE_SCALING_PLAYER2)
        self.player2_sprite.center_x = SCREEN_WIDTH - 50  # Starting position
        self.player2_sprite.center_y = 50
        self.player_list.append(self.player2_sprite)
        self.physics_engine1 = arcade.PhysicsEngineSimple(self.player1_sprite, self.wall_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.player2_sprite, self.wall_list)

        # Create the coins
        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("images/heart.png", SPRITE_SCALING_COIN)
            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output1 = f"Score 1: {self.score1}"
        arcade.draw_text(output1, 10, 20, arcade.color.WHITE, 14)
        output2 = f"Score 2: {self.score2}"
        arcade.draw_text(output2, SCREEN_WIDTH - 140, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.W:
            self.player1_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player1_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player1_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player1_sprite.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.player2_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player2_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player2_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player2_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if (key == arcade.key.W or key == arcade.key.S) and not (
                arcade.key.W in self.pressed_keys and arcade.key.S in self.pressed_keys):
            self.player1_sprite.change_y = 0
        elif (key == arcade.key.A or key == arcade.key.D) and not (
                arcade.key.A in self.pressed_keys and arcade.key.D in self.pressed_keys):
            self.player1_sprite.change_x = 0
        if (key == arcade.key.UP or key == arcade.key.DOWN) and not (
                arcade.key.UP in self.pressed_keys and arcade.key.DOWN in self.pressed_keys):
            self.player2_sprite.change_y = 0
        elif (key == arcade.key.LEFT or key == arcade.key.RIGHT) and not (
                arcade.key.LEFT in self.pressed_keys and arcade.key.RIGHT in self.pressed_keys):
            self.player2_sprite.change_x = 0

    def update(self, delta_time):
        # Keep playing background music
        #if not arcade.is_queued(self.background_sound):
        #    arcade.play_sound(self.background_sound)
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.physics_engine1.update()
        self.physics_engine2.update()
        # Generate a list of all coin sprites that collided with the player.
        coins_hit_list1 = arcade.check_for_collision_with_list(self.player1_sprite, self.coin_list)
        coins_hit_list2 = arcade.check_for_collision_with_list(self.player2_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list1:
            arcade.play_sound(self.sound_collect_coin)
            coin.kill()
            self.score1 += 1
        for coin in coins_hit_list2:
            arcade.play_sound(self.sound_collect_coin)
            coin.kill()
            self.score2 += 1


def main():
    game = Fred(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
