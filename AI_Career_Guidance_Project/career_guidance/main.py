"""
==============================================================================
AI-Based Expert System for Career Guidance
Main Application Entry Point
==============================================================================
Author      : AI Expert System Project
Version     : 1.0
Description : Launches the Career Guidance Expert System GUI
==============================================================================
"""

import tkinter as tk
from gui import CareerGuidanceApp


def main():
    """Main function to launch the Career Guidance Expert System."""
    root = tk.Tk()
    app = CareerGuidanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
