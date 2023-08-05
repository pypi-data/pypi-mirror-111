"""
Defines InfoBox class, an helper to draw any kind of popup (menu or informative message).
"""

from typing import Union, Sequence, List, Callable, Optional

import pygame

from ..configuration import default_sprites
from ..constants import (
    WHITE,
    CLOSE_BUTTON_MARGIN_TOP,
    MARGIN_BOX,
    DEFAULT_MARGIN_TOP,
    DEFAULT_CLOSE_BUTTON_SIZE,
    MARGIN_LINKED_ELEMENT,
    DEFAULT_POPUP_WIDTH,
)
from .box_element import BoxElement
from ..fonts import fonts
from .text_element import TextElement
from .button import Button
from ..types import Position


class InfoBox:
    """
    This class is defining any kind of popup that can be found in the app.
    It can be used to represent the interface of a menu, or a simple text message.
    Some elements can be buttons, that will react to user clicks (see the button component
    for more information).


    Keyword arguments:
    title -- the title of the infoBox
    element_grid -- a grid containing the components that should be rendered by the infoBox
    width -- the width of the infoBox, DEFAULT_POPUP_WIDTH will be assigned if none is given
    element_linked -- the pygame Rect of the element linked to this infoBox if any,
    the infoBox will be displayed beside the element if provided
    has_close_button -- a boolean indicating whether a close button should be added
    at the bottom or not
    title_color -- the color of the title
    background -- the pygame Surface corresponding to the image that will be the sprite of
    the infoBox
    close_button_sprite -- the pygame Surface corresponding to the sprite of the close button if there should be one
    close_button_sprite_hover -- the pygame Surface corresponding to the sprite of the close button when it is hovered if there should be one
    visible_on_background -- a boolean indicating whether the popup is visible on background or not

    Attributes:
    title -- the title of the infoBox
    element_linked -- the pygame Rect of the element linked to this infoBox if there is one
    close_button -- the callback to run when pressing the close button if there should be one
    has_close_button -- whether the infoBox has a close button or not
    title_color -- the color of the title
    element_grid -- the grid containing the components that should be rendered by the infoBox
    elements -- the 2D structure containing all the computed visual elements of the infoBox
    buttons -- the sequence of buttons of the infoBox, including the close button if present
    size -- the size of the infoBox following the format (width, height)
    position -- the position of the infoBox. Will be beside the linked element if present,
    or only computed at display time otherwise
    sprite -- the pygame Surface corresponding to the sprite of the infoBox
    close_button_sprite -- the pygame Surface corresponding to the sprite of the close button if there should be one
    close_button_sprite_hover -- the pygame Surface corresponding to the sprite of the close button when it is hovered if there should be one
    visible_on_background -- whether the popup is visible on background or not
    """

    def __init__(
        self,
        title: str,
        element_grid: List[List[BoxElement]],
        width: int = DEFAULT_POPUP_WIDTH,
        element_linked: pygame.Rect = None,
        has_close_button: bool = True,
        title_color: pygame.Color = WHITE,
        background: pygame.Surface = None,
        close_button_sprite: pygame.Surface = None,
        close_button_sprite_hover: pygame.Surface = None,
        visible_on_background: bool = True,
    ) -> None:
        self.title: str = title
        self.element_linked: pygame.Rect = element_linked
        self.has_close_button: bool = has_close_button
        self.title_color: pygame.Color = title_color
        self.element_grid: List[List[BoxElement]] = element_grid
        self.__elements: List[List[Union[BoxElement, int]]] = self.init_elements(width)
        self.buttons: Sequence[Button] = []
        self.__size: tuple[int, int] = (width, 0)
        self.__position: Position = pygame.Vector2(0, 0)
        if not background:
            background = pygame.image.load(default_sprites["info_box_background"])
        self.sprite: pygame.Surface = background
        self.close_button_sprite = close_button_sprite
        self.close_button_sprite_hover = close_button_sprite_hover
        self.visible_on_background: bool = visible_on_background

    def init_render(
        self, screen: pygame.Surface, close_button_callback: Callable = None
    ) -> None:
        """
        Initialize the rendering of the popup.
        Compute it size and its position according to the given screen.
        Determine the position of each component.

        Keyword arguments:
        screen -- the screen on which the popup is
        close_button_callback -- the callback that should be executed when clicking on
        the close button if there is any
        """
        height: int = self.determine_height(close_button_callback)
        self.__size = (self.__size[0], height)
        self.__position = self.determine_position(screen)
        if self.__position:
            self.determine_elements_position()
        self.buttons: Sequence[Button] = self.find_buttons()
        self.sprite = pygame.transform.scale(self.sprite.convert_alpha(), self.__size)

    def init_elements(self, width: int) -> List[List[BoxElement]]:
        """
        Initialize the graphical elements associated to the formal data that the infoBox should
        represent.

        Return the elements in a 2D structure to know the relative position of each element.

        Keyword arguments:
        width -- the width of the infoBox
        """
        elements: List[List[BoxElement]] = []
        for row in self.element_grid:
            element: List[BoxElement] = []
            for entry in row:
                element.append(entry)
            elements.append(element)
        title = TextElement(
            self.title,
            width,
            pygame.Vector2(0, 0),
            fonts["MENU_TITLE_FONT"],
            (20, 0, 20, 0),
            self.title_color,
        )
        elements.insert(0, [title])
        return elements

    def determine_height(self, close_button_action: Callable) -> int:
        """
        Compute the total height of the infoBox, defined according
        to the height of each element in it.
        Return the computed height.

        Keyword arguments:
        close_button_action -- the callback to run when pressing the close button
        if there should be one
        """
        # Margin to be add at begin and at end
        height: int = MARGIN_BOX * 2
        for row in self.__elements:
            max_height: int = 0
            for element in row:
                el_height = element.get_height() + DEFAULT_MARGIN_TOP
                if el_height > max_height:
                    max_height = el_height
            height += max_height
            row.insert(0, max_height)
        if self.has_close_button:
            close_button_height: int = (
                DEFAULT_CLOSE_BUTTON_SIZE[1]
                + DEFAULT_MARGIN_TOP
                + CLOSE_BUTTON_MARGIN_TOP
            )
            height += close_button_height

            self.__elements.append(
                [
                    close_button_height,
                    Button(
                        close_button_action,
                        DEFAULT_CLOSE_BUTTON_SIZE,
                        "Close",
                        sprite=self.close_button_sprite,
                        sprite_hover=self.close_button_sprite_hover,
                        margin=(CLOSE_BUTTON_MARGIN_TOP, 0, 0, 0),
                    ),
                ]
            )
        return height

    def determine_position(self, screen: pygame.Surface) -> Optional[Position]:
        """
        Compute the position of the infoBox to be beside the linked element.
        If no element is linked to the infoBox, the position will be determine at display time
        according to the screen.
        Return the computed position.
        """
        if self.element_linked:
            position: Position = pygame.Vector2(
                self.element_linked.x
                + self.element_linked.width
                + MARGIN_LINKED_ELEMENT,
                self.element_linked.y
                + self.element_linked.height // 2
                - self.__size[1] // 2,
            )
            if position.y < 0:
                position.y = 0
            elif position.y + self.__size[1] > screen.get_height():
                position.y = screen.get_height() - self.__size[1]
            if position.x + self.__size[0] > screen.get_width():
                position.x = self.element_linked.x - self.__size[0]
            return position
        return None

    def find_buttons(self) -> Sequence[Button]:
        """
        Search in all elements for buttons.
        Return the sequence of buttons.
        """
        buttons: List[Button] = []
        for row in self.__elements:
            for element in row[1:]:
                if isinstance(element, Button):
                    buttons.append(element)
        return buttons

    def determine_elements_position(self):
        """
        Compute the position of each element and update it if needed.
        """
        y_coordinate: int = self.__position[1] + MARGIN_BOX
        # Memorize mouse position in case it is over a button
        mouse_pos = pygame.mouse.get_pos()
        # A row begins by a value identifying its height, followed by its elements
        for row in self.__elements:
            nb_elements = len(row) - 1
            i = 1
            for element in row[1:]:
                base_x = self.__position.x + (self.__size[0] // (2 * nb_elements)) * i
                x_coordinate = base_x - element.get_width() // 2
                element.position = pygame.Vector2(
                    x_coordinate,
                    y_coordinate + element.get_margin_top(),
                )
                if isinstance(element, Button):
                    element.set_hover(element.get_rect().collidepoint(mouse_pos))
                i += 2
            y_coordinate += row[0]

    def display(self, screen: pygame.Surface) -> None:
        """
        Display the infoBox and all its elements.

        Keyword arguments:
        screen -- the screen on which the displaying should be done
        """
        if self.__position:
            screen.blit(self.sprite, self.__position)
        else:
            win_size = screen.get_size()
            self.__position = pygame.Vector2(
                win_size[0] // 2 - self.__size[0] // 2,
                win_size[1] // 2 - self.__size[1] // 2,
            )
            screen.blit(self.sprite, self.__position)
            self.determine_elements_position()

        for row in self.__elements:
            for element in row[1:]:
                element.display(screen)

    def motion(self, position: Position) -> None:
        """
        Handle the triggering of a motion event.
        Test if the mouse entered in a button or quited one.

        Keyword arguments:
        position -- the position of the mouse
        """
        for button in self.buttons:
            mouse_is_on_button: bool = button.get_rect().collidepoint(position)
            button.set_hover(mouse_is_on_button and not button.disabled)

    def click(self, position: Position) -> Callable:
        """
        Handle the triggering of a click event.
        Return the data corresponding of the action that should be done if the click was done
        on a button, else False.

        Keyword arguments:
        position -- the position of the mouse
        """
        for button in self.buttons:
            if button.get_rect().collidepoint(position):
                return button.action_triggered()
        # Return a " do nothing " callable when clicking on empty space
        return lambda: None
