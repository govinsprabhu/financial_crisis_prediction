from flask import Flask, render_template, request
import math
import tkinter as tk
from tkinter import ttk

print("Indirect Fire Calculator")
shell = "OCC105F1"
def gun_elevation(distance, velocity=1000):
    g = 9.81
    try:
        angle_rad = 0.5 * math.asin((g * distance) / (velocity ** 2))
    except ValueError:
        return "Target out of range for this muzzle velocity."
    angle_deg = math.degrees(angle_rad)
    return round(angle_deg, 2)


distance_to_target = float(input("Enter distance to target in meters: "))
elevation_angle = gun_elevation(distance_to_target)
print(f"Required gun elevation: {elevation_angle}°")
