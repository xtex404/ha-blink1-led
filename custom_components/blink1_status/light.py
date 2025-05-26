"""
Blink(1) Status Light integration for Home Assistant.

This module provides a LightEntity platform for controlling a Blink(1) USB RGB LED device
using Home Assistant. It supports brightness and color control.

Author: Justin Matlock
Date: 2025-05-25
"""

import logging
from typing import Callable

import homeassistant.util.color as color_util
from blink1.blink1 import Blink1, Blink1ConnectionFailed

# Import the device class from the component that you want to support
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    LightEntity,
)
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: Callable[[list], None],
    discovery_info: dict | None = None,
) -> None:
    """Set up the Blink(1) light platform.

    Args:
        hass (HomeAssistant): Home Assistant instance.
        config (dict): Configuration dictionary.
        async_add_entities (callable): Function to add entities.
        discovery_info (dict, optional): Discovery info.

    This function initializes the Blink(1) device and adds it as a light entity.

    """

    # Blink1 is a sync library, so instantiate in executor
    b1 = await hass.async_add_executor_job(
        Blink1,
        None,
        None,
        None,
    )
    async_add_entities([Blink1LED(light=b1)])


class Blink1LED(LightEntity):
    """Representation of a Blink(1) Light entity."""

    def __init__(self, light: "Blink1") -> None:
        """Initialize the Blink(1) light entity.

        Args:
            light (Blink1): An instance of the Blink1 device.

        """
        # Store the Blink1 device instance
        self._light = light
        # Name of the entity
        self._name = "Blink1"
        # State of the light (on/off)
        self._state = None
        # Current HS color value
        self._hs_color = [0, 0]
        # Current brightness value (0-255)
        self._brightness = 0

    @property
    def brightness(self):
        """int: Return the brightness of the light (0-255)."""
        return self._brightness

    @property
    def supported_features(self):
        """int: Return the supported features (brightness and color)."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR

    @property
    def name(self):
        """str: Return the display name of this light."""
        return self._name

    @property
    def hs_color(self):
        """list: Return the HS color of this light."""
        return self._hs_color

    @property
    def is_on(self):
        """bool: Return True if the light is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the light on.

        Args:
            **kwargs: Arbitrary keyword arguments. May include ATTR_HS_COLOR and ATTR_BRIGHTNESS.

        This method sets the color and brightness of the Blink(1) device and turns it on.

        """
        # Update HS color if provided
        if ATTR_HS_COLOR in kwargs:
            self._hs_color = kwargs[ATTR_HS_COLOR]
        # Update brightness if provided
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
        # Set the state to on
        self._state = True
        # Convert HS color and brightness to RGB
        rgb_color = color_util.color_hsv_to_RGB(
            iH=self._hs_color[0],
            iS=self._hs_color[1],
            iV=self._brightness / 255 * 100,
        )
        # Fade the Blink1 device to the new RGB color (run in executor)
        try:
            await self.hass.async_add_executor_job(
                self._light.fade_to_rgb,
                100,
                int(rgb_color[0]),
                int(rgb_color[1]),
                int(rgb_color[2]),
                None,
            )
        except Blink1ConnectionFailed as e:
            _LOGGER.error("Failed to turn on Blink(1): %s", e)
            # If the connection fails, set the state to off
            self._state = False
            raise

    async def async_turn_off(self, **kwargs):
        """Turn the light off.

        Args:
            **kwargs: Arbitrary keyword arguments (unused).

        This method turns off the Blink(1) device

        """
        # Set the state to off
        self._state = False
        # Turn off the Blink1 device (run in executor)
        try:
            await self.hass.async_add_executor_job(
                self._light.off,
            )
        except Blink1ConnectionFailed as e:
            _LOGGER.error("Failed to turn off Blink(1): %s", e)
            self._state = False
            raise

    async def async_update(self):
        """Update the state of the light.

        There is no data to fetch from the device, as we use an assumed state.
        """
        # No operation needed; state is assumed
