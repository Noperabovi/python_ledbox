from typing import Tuple


class Color:
    """Provides functionality for creating and managing colors."""

    _value: int = 0

    # setter
    @staticmethod
    def set_rgb(red: int, green: int, blue: int) -> None:
        """Set color-value based on rgb input."""
        Color._value = (red << 16) | (green << 8) | blue

    # @staticmethod
    # def set_hsv(hue: int, saturation: int, value: int) -> None:
    #     """Set color-value based on hsv input."""
    #     pass

    # @staticmethod
    # def set_hsl(hue: int, saturation: int, lightness: int) -> None:
    #     """Set color-value based on hsl input."""
    #     pass

    # @staticmethod
    # def set_hex(hexString: str) -> None:
    #     """Set color-value based on hex-string input."""
    #     pass

    # getter
    @staticmethod
    def get_rgb() -> Tuple[int]:
        """Get rgb color-value."""
        return (
            Color._value >> 16 & 0xFF,
            Color._value >> 8 & 0xFF,
            Color._value & 0xFF,
        )

    # @staticmethod
    # def get_hsv() -> Tuple[int]:
    #     """Get hsv color-value"""
    #     pass

    # @staticmethod
    # def get_hsl() -> Tuple[int]:
    #     """Get hsl color-value"""
    #     pass

    # @staticmethod
    # def get_hex(prependHash=False) -> str:
    #     """Get hex color string."""
    #     pass
