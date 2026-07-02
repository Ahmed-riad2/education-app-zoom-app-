# screens/meeting_hub_screen.py
import flet as ft
import random
import string

class MeetingHubScreen(ft.Container):
    def __init__(self, on_enter_classroom, on_back):
        """
        Initialize the Meeting Management Hub.
        :param on_enter_classroom: Function to route into the actual virtual classroom.
        :param on_back: Function to route back to the dashboard.
        """
        super().__init__()
        self.on_enter_classroom = on_enter_classroom
        self.on_back = on_back
        
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 40 # Padding applied directly to the Container

        # Generate a random 6-character code on load
        self.generated_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # --- UI Components ---
        self.code_display = ft.Text(
            f"Code: {self.generated_code}", 
            size=28, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.BLUE_400
        )
        self.record_switch = ft.Switch(label="Record Meeting (AI Summarizer)", value=False)
        self.join_input = ft.TextField(label="Meeting Code", hint_text="Enter 6-digit code", width=300)

        # Card 1: Create Meeting
        self.create_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=30,
                width=400,
                content=ft.Column(
                    controls=[
                        # FIXED: Changed ADD_VIDEO_CALL to VIDEO_CALL
                        ft.Icon(ft.Icons.VIDEO_CALL, size=50, color=ft.Colors.BLUE_500),
                        ft.Text("Start a New Meeting", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Create a secure virtual classroom.", color=ft.Colors.OUTLINE),
                        ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                        self.code_display,
                        self.record_switch,
                        ft.ElevatedButton(
                            content=ft.Text("Start Meeting"),
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            on_click=lambda _: self.on_enter_classroom()
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )

        # Card 2: Join Meeting
        self.join_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=30,
                width=400,
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.LOGIN, size=50, color=ft.Colors.GREEN_500),
                        ft.Text("Join via Code", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Enter a meeting code provided by your teacher.", color=ft.Colors.OUTLINE),
                        ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                        self.join_input,
                        ft.ElevatedButton(
                            content=ft.Text("Join Meeting"),
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            on_click=self.handle_join
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )

        # --- Assemble the Screen ---
        self.content = ft.Column(
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.on_back()),
                    ft.Text("Meeting Management", size=32, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                
                ft.Row(
                    controls=[self.create_card, self.join_card],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=40,
                    wrap=True
                )
            ]
        )

    def handle_join(self, e):
        """Validate the entered code before joining."""
        code = self.join_input.value.strip()
        if len(code) < 5:
            # Show an error notification if the code is invalid
            self.page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid meeting code!"), bgcolor=ft.Colors.RED_500)
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.on_enter_classroom() 