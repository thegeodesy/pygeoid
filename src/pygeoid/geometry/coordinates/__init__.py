"""Lightweight containers for common geodetic coordinate systems."""

from .base import BaseCoordinates
from .cartesian import CartesianCoordinates
from .ellipsoidal import (
    EllipsoidalCoordinates,
    EllipsoidalHarmonicCoordinates,
    GeodeticCoordinates,
)
from .local import LocalCoordinates, LocalTangentPlane
from .spherical import SphericalCoordinates

__all__ = [
    "BaseCoordinates",
    "EllipsoidalCoordinates",
    "CartesianCoordinates",
    "SphericalCoordinates",
    "GeodeticCoordinates",
    "EllipsoidalHarmonicCoordinates",
    "LocalCoordinates",
    "LocalTangentPlane",
]
