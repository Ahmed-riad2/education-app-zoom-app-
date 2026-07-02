# screens/classroom_screen.py
import flet as ft
from datetime import datetime
from components.session_recorder import SessionRecorder # NEW IMPORT

class ClassroomScreen(ft.Container):
    def __init__(self, on_leave_class):
        """
        Initialize the Virtual Classroom.
        :param on_leave_class: Function to call when the user clicks 'Leave'.
        """
        super().__init__()
        self.on_leave_class = on_leave_class
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 20 

        # Initialize our freshly engineered component component here
        self.ai_recorder = SessionRecorder(on_transcript_update=self.handle_incoming_transcript)

        # --- 1. Video / Presentation Area (Left Side) ---
        self.video_area = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK87,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SCREEN_SHARE, size=100, color=ft.Colors.WHITE54),
                    ft.Text("Teacher's Screen Sharing", size=24, color=ft.Colors.WHITE54)
                ]
            )
        )

        # Control Bar (Mute, Camera, Hand, Leave)
        self.control_bar = ft.Container(
            padding=10,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(icon=ft.Icons.MIC, tooltip="Mute/Unmute", icon_color=ft.Colors.WHITE),
                    ft.IconButton(icon=ft.Icons.VIDEOCAM, tooltip="Turn off Camera", icon_color=ft.Colors.WHITE),
                    ft.IconButton(icon=ft.Icons.BACK_HAND, tooltip="Raise Hand", icon_color=ft.Colors.AMBER_400),
                    ft.Container(width=20), 
                    ft.ElevatedButton(
                        content="Leave Class", 
                        bgcolor=ft.Colors.RED_600, 
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.on_leave_class()
                    )
                ]
            )
        )

        # Combine Video Area, Control Bar, and the new AI Recorder into Left Panel
        self.left_column = ft.Column(
            expand=3, 
            controls=[
                self.video_area, 
                self.ai_recorder, # INSTANTIATED RECORDER ADDED TO THE UI STEM
                self.control_bar
            ]
        )

        # --- 2. Chat Area (Right Side) ---
        self.chat_list = ft.ListView(
            expand=True, 
            spacing=10, 
            auto_scroll=True 
        )
        
        self.chat_input = ft.TextField(
            hint_text="Type a message...",
            expand=True,
            border_radius=20,
            filled=True,
            on_submit=self.send_message 
        )
        
        self.send_btn = ft.IconButton(
            icon=ft.Icons.SEND, 
            icon_color=ft.Colors.BLUE_400,
            on_click=self.send_message
        )

        self.right_column = ft.Container(
            expand=1, 
            bgcolor=ft.Colors.SURFACE,
            border_radius=10,
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Text("Class Chat", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(color=ft.Colors.OUTLINE_VARIANT),
                    self.chat_list,
                    ft.Row([self.chat_input, self.send_btn])
                ]
            )
        )

        # --- 3. Assemble the Screen ---
        self.content = ft.Row(
            expand=True,
            spacing=20,
            controls=[self.left_column, self.right_column]
        )

    def did_mount(self):
        """Fires automatically when the screen is actually added to the page."""
        self.add_chat_message("System", "Welcome to Advanced Physics!", is_system=True)

    def send_message(self, e):
        """Handles sending a message to the chat."""
        if self.chat_input.value:
            self.add_chat_message("You", self.chat_input.value)
            self.chat_input.value = "" 
            self.chat_input.focus()    
            self.update()

    def handle_incoming_transcript(self, transcript_text):
        """Callback engine processing incoming audio speech packets from background threads."""
        # Re-route the live transcript text straight into the classroom chat interface dynamically
        self.add_chat_message("AI Transcriber", transcript_text)

    def add_chat_message(self, sender, text, is_system=False):
        """Helper method to format and add a message to the ListView."""
        time_str = datetime.now().strftime("%H:%M")
        
        # Pick contrasting color schemes based on transmission origin
        if is_system:
            color = ft.Colors.GREEN_400
        elif sender == "AI Transcriber":
            color = ft.Colors.PURPLE_300
        else:
            color = ft.Colors.BLUE_200
        
        message_ui = ft.Column(
            spacing=2,
            controls=[
                ft.Row([
                    ft.Text(sender, weight=ft.FontWeight.BOLD, color=color, size=12),
                    ft.Text(time_str, size=10, color=ft.Colors.OUTLINE)
                ]),
                ft.Text(text, size=14)
            ]
        )
        self.chat_list.controls.append(message_ui)
        
        if self.page:
            self.update()