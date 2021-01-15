from typing import Tuple


class Color:
    """Provides functionality for creating and managing colors."""

    @staticmethod
    def from_rgb(red: int, green: int, blue: int) -> int:
        """Set color-value based on rgb input."""
        return (red << 16) | (green << 8) | blue

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

    @staticmethod
    def to_rgb(color: int) -> Tuple[int]:
        """Get rgb color-value."""
        return (
            color >> 16 & 0xFF,
            color >> 8 & 0xFF,
            color & 0xFF,
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
