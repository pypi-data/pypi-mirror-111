"""
Defines DynamicButton class, a special Button iterating through a list of values
on each click.
Generally use as a parameter button.
"""

from typing import Sequence, Callable

import pygame

from ..constants import WHITE
from ..types import Position, Margin
from ..fonts import fonts
from .button import Button


class DynamicButton(Button):
    """
    This class is representing a special button with an inner value changing after each click.
    A DynamicButton has a sequence of values given at initialization, and a initial value.
    The sequence will be iterated to determine the next inner value after a click.
    This fluctuating value is the one that will be send has the first argument of
    the method called on click, and a different label will be displayed on the button for
    each different value of the sequence.

    Keyword arguments:
    callback -- the reference to the function that should be call after a click
    size -- the size of the button following the format "(width, height)"
    values -- the sequence of values that will be iterated to determine the next inner value
    current_value_index -- the index of the initial value of the button
    base_title -- the common prefix of all the different labels
    (it could be the name of the dynamic button in a way)
    position -- the position of the element on the screen
    sprite -- the pygame Surface corresponding to the sprite of the element
    sprite_hover -- the pygame Surface corresponding to the sprite of the element
    when it has the focus
    margin -- a tuple containing the margins of the box,
    should be in the form "(top_margin, right_margin, bottom_margin, left_margin)"
    linked_object -- the game entity linked to the button if there is one
    disabled -- a boolean indicating if it is not possible to interact with the button

    Attributes:
    values -- the sequence of values that will be iterated to determine the next inner value
    current_value_index -- the index of the current value of the button
    base_title -- the common prefix of all the different labels
    (it could be the name of the dynamic button in a way)
    """

    def __init__(
        self,
        callback: Callable,
        size: tuple[int, int],
        values: Sequence[any],
        current_value_index: int,
        base_title: str,
        position: Position = pygame.Vector2(0, 0),
        sprite: pygame.Surface = None,
        sprite_hover: pygame.Surface = None,
        margin: Margin = (10, 0, 10, 0),
        linked_object: any = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            callback,
            size,
            "",
            position,
            sprite,
            sprite_hover,
            margin,
            linked_object,
            disabled,
        )
        self.values: Sequence[any] = values
        self.current_value_index: int = current_value_index
        self.base_title: str = base_title
        self.__base_sprite: pygame.Surface = self.sprite
        self.__base_sprite_hover: pygame.Surface = self.sprite_hover
        self.__update_sprite()

    def __update_sprite(self) -> None:
        """
        Update the render of the button to display the updated dynamic value.
        Should be called after the current value changed.
        """
        rendered_name: pygame.Surface = fonts["DEFAULT_FONT"].render(
            f'{self.base_title} {self.values[self.current_value_index]["label"]}',
            True,
            WHITE,
        )

        temporary_sprite: pygame.Surface = self.__base_sprite.copy()
        temporary_sprite.blit(
            rendered_name,
            (
                temporary_sprite.get_width() // 2 - rendered_name.get_width() // 2,
                temporary_sprite.get_height() // 2 - rendered_name.get_height() // 2,
            ),
        )
        self.sprite = temporary_sprite

        temporary_sprite_hover: pygame.Surface = self.__base_sprite_hover.copy()
        temporary_sprite_hover.blit(
            rendered_name,
            (
                temporary_sprite_hover.get_width() // 2
                - rendered_name.get_width() // 2,
                temporary_sprite_hover.get_height() // 2
                - rendered_name.get_height() // 2,
            ),
        )
        self.sprite_hover = temporary_sprite_hover

        # Force display update
        self.set_hover(True)

    def action_triggered(self) -> Callable:
        """
        Method that should be called after a click.
        Change the current value of the button to the next one in the sequence of values.
        If the end of the sequence is reach, the iteration restarts at the first value.

        Return a lambda containing the function that should be called with the current value of the
        dynamic button as an argument.
        """
        # Search for next value
        self.current_value_index += 1
        if self.current_value_index == len(self.values):
            self.current_value_index = 0
        self.__update_sprite()
        current_value = self.values[self.current_value_index]["value"]
        function_to_call: Callable = super().action_triggered()
        return lambda: function_to_call(current_value)
