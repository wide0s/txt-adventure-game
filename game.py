from __future__ import annotations
import os
import random
from pathlib import Path
import pygame


def clear_screen():
    _ = os.system('cls' if os.name == 'nt' else 'clear')


class SceneAudio:
    def __init__(self, wav_file: Path):
        self._wav = Path(__file__).parent / 'sounds' / wav_file \
            if wav_file is not None else None

    def play(self):
        self.stop()
        if self._wav is not None:
            pygame.mixer.music.load(self._wav)
            pygame.mixer.music.play(loops=-1)

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

NoAudio = SceneAudio(None)

class Scene:
    def __init__(self,
                 name: str,
                 description: str = None,
                 north: Scene = None,
                 south: Scene = None,
                 west: Scene = None,
                 east: Scene = None,
                 audio: SceneAudio = None):
        self.name:str = name
        self._scenes: dict[str, Scene] = {
            'north': north,
            'south': south,
            'west': west,
            'east': east
        }
        self._description: str = description
        self._audio: SceneAudio = \
            audio if audio is not None else NoAudio

    @property
    def north(self) -> Scene:
        return self._scenes['north']

    @north.setter
    def north(self, location: Scene) -> None:
        self._scenes['north'] = location

    @property
    def west(self) -> Scene:
        return self._scenes['west']

    @west.setter
    def west(self, location: Scene) -> None:
        self._scenes['west'] = location

    @property
    def east(self) -> Scene:
        return self._scenes['east']

    @east.setter
    def east(self, location: Scene) -> None:
        self._scenes['east'] = location

    @property
    def south(self) -> Scene:
        return self._scenes['south']

    @south.setter
    def south(self, location: Scene) -> None:
        self._scenes['south'] = location

    def enter(self, clear=True) -> Scene:
        if clear:
            clear_screen()
        self._audio.play()
        print(f'You are entering {self.name}')
        if self._description is not None:
            print(self._description)
        print(f"You look around and see that you can go "
              f"{', '.join(self.directions())}.\n")
        return self

    def directions(self) -> list[str]:
        return [k for k, v in self._scenes.items()
                if v is not None]

    def leave(self, to: str, clear=True) -> Scene:
        location = self._scenes.get(to)
        if location is not None:
            location.enter(clear)
        else:
            location = self
            print('No, I can not go that way.')
        return location


beautiful_forest = Scene(
    name = 'Beautiful forest',
    audio=SceneAudio('beautiful-forest.wav'),
    description= """
                   .
       ^     .          ^
            ^      .
       /\\            /\\          /\\
      /**\\     ^    /**\\        /**\\
     /****\\        /****\\      /****\\
       ||            ||         ||||
       ||||          ||||       ||||
  |||||||||||    |||||||||||  ||||||||||
  |||||||||||    |||||||||||  |||||||||||

      ~      .      ~        .
          ~        .     ~

  Strange flowers glow faintly beneath the trees.
  The forest feels ancient… and aware.

  Whoa! It is so beautiful here. There are so many
  trees and everything is blooming.
"""
)


dark_forest = Scene(
    name = 'Dark forest',
    audio=SceneAudio('dark-forest.wav'),
    description="""
           ☾
         .          .
      ^       .           ^
        /\\       /\\       /\\
      _/**\\_   _/**\\_   _/**\\_
     /######\\ /######\\ /######\\
      ||||||   ||||||   ||||||
   |||||||||||||||||||||||||||||
   |||||||||||||||||||||||||||||

      ~~~        ~~~
   .        .          .

  The shadows cling to the trees. You feel an ominous
  presence watching...

  Oh no! It is so dark and scary here!
"""
)

scary_forest = Scene(
    name = 'Scary forest',
    audio=SceneAudio('scary-forest.wav'),
    description="""
               .
        .               .
      ^      ^      ^       ^
              /\\      /\\
       /\\    /**\\   _/**\\_   /\\
      /**\\  /****\\ /######\\ /**\\
     /****\\  ||||   |||||| /****\\
      |||| ||||||||||||||||||||||||
  |||||||||||||||||||||||||||||||||
  |||||||||||||||||||||||||||||||||

           /\\  \\/  /\\
          //\\\\ .. //\\\\
          //\\((  ))/\\\\
          /  < `' >  \\

      ~~~   ~~~~    ~~~
   .      .     .       .

  Dark spiders crawl across the trees and ground.
  Their presence makes the forest truly terrifying.

  Ew I hate it here... it is time to get out of here!
"""
)

rotten_swamp = Scene(
    name = 'Rotten swap',
    audio=SceneAudio('rotten-swamp.wav'),
    description="""
       ~    ~  ~      ~
    ~      ~      ~   ~
       ~     ~  ~
    ~    ___     ~    ~
       /     \\     ~
      | () () |    ~
       \\  ^  /   ~
        |||||      ~
    ~   |||||   ~      ~
  ~      |||     ~
       ~  |||    ~
   ~       |||   ~    ~

  The swamp is thick with rotting trees and murky water.
  A foul smell fills the air, and strange sounds echo around.

  I want to go back immediately!
"""
)

beautiful_forest.east = dark_forest
beautiful_forest.south = rotten_swamp
dark_forest.west = beautiful_forest
dark_forest.south = scary_forest
scary_forest.north = dark_forest
scary_forest.west = rotten_swamp
rotten_swamp.north = beautiful_forest
rotten_swamp.east = scary_forest

random_lines = ["I do not think so.", "Let's try something different.",
                "Something seems wrong.", "Wait! What am I doing?",
                "Wait, that doesn't add up.", "That wasn't in the plan.",
                "Something feels off here.", "I have a bad feeling about this.",
                "This is definitely not right", "Dumb f@#$."]

pygame.mixer.init()

# set starting location
location = beautiful_forest.enter()
try:
    message = ""
    while message != 'quit':
        message = input('What will you do next (or type help)? ')
        if message == 'quit':
            pass
        elif message in location.directions():
            location = location.leave(message)
        elif message == 'help':
            for direction in location.directions():
                print(f"{direction:<5} if you want to go {direction}")
            print("quit  if you want to quit this amazing game")
        elif len(message.strip()) > 0:
            line = random.choice(random_lines)
            print(line)
except KeyboardInterrupt:
    pass
print("\nYou slowly open your eyes and realize that it was all just a dream. Just a strange dream.")

pygame.mixer.quit()