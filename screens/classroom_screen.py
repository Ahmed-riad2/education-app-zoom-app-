# screens/classroom_screen.py
import flet as ft
from datetime import datetime
import cv2
import base64
import threading
import time

class ClassroomScreen(ft.Container):
    def __init__(self, on_leave_class):
        super().__init__()
        self.on_leave_class = on_leave_class
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 15

        # --- State Management ---
        self.network = None
        self.user_name = "User"
        self.user_role = "Student"
        
        # Camera State
        self.is_running = False 
        self.is_camera_on = False

        # --- UI: Left Column (Video & Controls) ---
        # 1. Main Video Area 
        # FIXED: Initialize with a valid transparent base64 pixel directly in 'src'
        empty_pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        self.video_image = ft.Image(src=empty_pixel, visible=False, expand=True, fit="contain")
        
        self.video_area = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            border_radius=10,
            alignment=ft.Alignment(0, 0),
            content=ft.Stack(
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.SCREEN_SHARE, size=64, color=ft.Colors.WHITE54),
                            ft.Text("Teacher's Screen Sharing", size=24, color=ft.Colors.WHITE54)
                        ]
                    ),
                    self.video_image
                ]
            )
        )

        # 2. AI Recorder Bar
        self.recorder_bar = ft.Card(
            elevation=2,
            content=ft.Container(
                padding=15,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=15,
                            controls=[
                                ft.Icon(ft.Icons.RADIO_BUTTON_CHECKED, color=ft.Colors.OUTLINE),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("AI Recorder Idle", size=12, color=ft.Colors.OUTLINE),
                                        ft.Text("00:00:00", weight=ft.FontWeight.BOLD, size=16)
                                    ]
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(icon=ft.Icons.PLAY_ARROW, bgcolor=ft.Colors.BLUE_600, icon_color=ft.Colors.WHITE),
                                ft.IconButton(icon=ft.Icons.STOP, bgcolor=ft.Colors.RED_600, icon_color=ft.Colors.WHITE)
                            ]
                        )
                    ]
                )
            )
        )

        # 3. Bottom Control Bar
        self.camera_button = ft.IconButton(
            icon=ft.Icons.VIDEOCAM, 
            icon_color=ft.Colors.WHITE,
            on_click=self.toggle_camera
        )

        self.control_bar = ft.Card(
            elevation=2,
            content=ft.Container(
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.IconButton(icon=ft.Icons.MIC, icon_color=ft.Colors.WHITE),
                        self.camera_button,
                        ft.IconButton(icon=ft.Icons.BACK_HAND, icon_color=ft.Colors.AMBER_400),
                        ft.ElevatedButton(
                            content=ft.Text("Leave Class", weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.RED_600,
                            color=ft.Colors.WHITE,
                            on_click=self.handle_leave_class
                        )
                    ]
                )
            )
        )

        self.left_column = ft.Column(
            expand=7,
            spacing=15,
            controls=[
                self.video_area,
                self.recorder_bar,
                self.control_bar
            ]
        )

        # --- UI: Right Column (Chat Panel) ---
        self.chat_list = ft.ListView(expand=True, spacing=15, auto_scroll=True)
        
        self.chat_input = ft.TextField(
            hint_text="Type a message...",
            expand=True,
            border_radius=20,
            content_padding=15,
            filled=True,
            border_color=ft.Colors.TRANSPARENT,
            on_submit=self.handle_send_message
        )

        self.chat_panel = ft.Container(
            expand=3,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Class Chat", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.Colors.OUTLINE_VARIANT),
                    self.chat_list,
                    ft.Row(
                        controls=[
                            self.chat_input,
                            ft.IconButton(
                                icon=ft.Icons.SEND, 
                                icon_color=ft.Colors.BLUE_500,
                                on_click=self.handle_send_message
                            )
                        ]
                    )
                ]
            )
        )

        self.content = ft.Row(
            expand=True,
            controls=[self.left_column, self.chat_panel]
        )

    # ==========================================
    # LIFECYCLE & NETWORK BINDINGS
    # ==========================================
    
    def did_mount(self):
        if hasattr(self.page, 'session_data'):
            self.network = self.page.session_data.get("network")
            self.user_name = self.page.session_data.get("user_name", "User")
            self.user_role = self.page.session_data.get("user_role", "Student")

        if self.network:
            self.network.on_message_received = self.process_incoming_network_data
            
        self.append_chat_message("System", f"Welcome {self.user_name}! You are connected.", is_system=True)

    # ==========================================
    # VIDEO STREAMING LOGIC
    # ==========================================

    def toggle_camera(self, e):
        if self.user_role != "Teacher":
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Only the Teacher can broadcast video."), bgcolor=ft.Colors.RED_600)
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not self.is_camera_on:
            self.is_camera_on = True
            self.is_running = True
            self.camera_button.icon_color = ft.Colors.GREEN_400
            threading.Thread(target=self.camera_loop, daemon=True).start()
            self.append_chat_message("System", "Webcam broadcast started.", is_system=True)
        else:
            self.is_camera_on = False
            self.is_running = False
            self.camera_button.icon_color = ft.Colors.WHITE
            self.video_image.visible = False
            
            if self.network and self.network.is_server:
                self.network.send_message({"type": "video_stop"})
                
            self.append_chat_message("System", "Webcam broadcast stopped.", is_system=True)
            
        self.update()

    def camera_loop(self):
        # We are forcing it to use Index 1 or 2 to bypass the Iriun virtual driver
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) 
        
        # If index 1 doesn't work, you can change the number above to 2 or 0 until it grabs the right one!

        if cap is None:
            self.append_chat_message("System", "Error: No active webcam found.", is_system=True)
            self.is_running = False
            self.is_camera_on = False
            self.camera_button.icon_color = ft.Colors.WHITE
            if self.page:
                self.update()
            return

        while self.is_running and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                frame_b64 = base64.b64encode(buffer).decode('utf-8')
                
                # FIXED: Assign the base64 string directly to 'src'
                self.video_image.src = frame_b64
                self.video_image.visible = True
                
                try:
                    if self.page:
                        self.video_image.update() 
                except Exception:
                    pass
                
                if self.network and self.network.is_server:
                    self.network.send_message({
                        "type": "video",
                        "frame": frame_b64
                    })
                    
            time.sleep(0.05) 
            
        if cap:
            cap.release()

    # ==========================================
    # DATA PROCESSING
    # ==========================================

    def process_incoming_network_data(self, data):
        msg_type = data.get("type")
        
        if msg_type == "video" and self.user_role == "Student":
            # FIXED: Assign the base64 string directly to 'src'
            self.video_image.src = data.get("frame")
            self.video_image.visible = True
            try:
                if self.page:
                    self.video_image.update()
            except Exception:
                pass
                
        elif msg_type == "video_stop" and self.user_role == "Student":
            self.video_image.visible = False
            if self.page:
                self.update()
                
        elif msg_type == "chat":
            sender = data.get("sender", "Unknown")
            text = data.get("text", "")
            self.append_chat_message(sender, text)
            
        elif msg_type == "system" and data.get("action") == "join":
            sender = data.get("sender", "Unknown")
            self.append_chat_message("System", f"{sender} has joined the session.", is_system=True)

    def handle_send_message(self, e):
        text = self.chat_input.value.strip() if self.chat_input.value else ""
        if not text: return
        self.chat_input.value = ""
        self.update()

        if self.network:
            packet = {
                "type": "chat",
                "sender": self.user_name,
                "text": text,
                "timestamp": datetime.now().strftime("%H:%M")
            }
            self.network.send_message(packet)
            self.append_chat_message("You", text)
        else:
            self.append_chat_message("System", "Network offline. Message not sent.", is_system=True)

    def append_chat_message(self, sender, text, is_system=False):
        time_str = datetime.now().strftime("%H:%M")
        
        if is_system: name_color = ft.Colors.GREEN_400
        elif sender == "You": name_color = ft.Colors.BLUE_400
        else: name_color = ft.Colors.WHITE

        msg_block = ft.Column(
            spacing=2,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Text(sender, weight=ft.FontWeight.BOLD, color=name_color),
                        ft.Text(time_str, size=10, color=ft.Colors.OUTLINE)
                    ]
                ),
                ft.Text(text, selectable=True)
            ]
        )
        self.chat_list.controls.append(msg_block)
        if self.page: self.page.update()

    def handle_leave_class(self, e):
        self.is_running = False
        time.sleep(0.1)
        
        if self.network:
            self.network.disconnect()
            self.page.session_data["network"] = None
            
        self.on_leave_class()