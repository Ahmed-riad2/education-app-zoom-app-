# screens/splash_screen.py
import flet as ft
import time
import threading

class SplashScreen(ft.Container):
    def __init__(self, on_loading_complete):
        """
        Initialize the Splash Screen.
        :param on_loading_complete: A function to call when loading is finished.
        """
        super().__init__()
        self.on_loading_complete = on_loading_complete
        
        # Configure the container to take up the whole screen
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.alignment = ft.Alignment.CENTER

        # UI Elements
        self.logo_text = ft.Text(
            value="EduVerse AI",
            size=50,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_500,
        )
        
        self.subtitle = ft.Text(
            value="Learn together, from anywhere.",
            size=18,
            color=ft.Colors.OUTLINE,
        )
        
        self.loading_ring = ft.ProgressRing(
            width=40, 
            height=40, 
            stroke_width=4, 
            color=ft.Colors.BLUE_500
        )

        # Layout: Arrange elements vertically
        self.content = ft.Column(
            controls=[
                self.logo_text,
                self.subtitle,
                ft.Container(height=30), # Adds vertical space
                self.loading_ring
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def did_mount(self):
        """This Flet lifecycle method runs automatically when the screen appears."""
        # Start a background thread so the UI animation doesn't freeze
        threading.Thread(target=self._simulate_loading, daemon=True).start()

    def _simulate_loading(self):
        """Simulate loading backend resources."""
        time.sleep(3) # Wait for 3 seconds
        self.on_loading_complete() # Tell main.py to move to the next screen