# screens/meeting_hub_screen.py
import flet as ft
from services.network_manager import NetworkManager

class MeetingHubScreen(ft.Container):
    def __init__(self, on_enter_classroom, on_back):
        """
        Initialize the Meeting Hub Screen.
        :param on_enter_classroom: Route to classroom UI after successful connection.
        :param on_back: Route back to the dashboard.
        """
        super().__init__()
        self.on_enter_classroom = on_enter_classroom
        self.on_back = on_back
        
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 40

        # --- UI Sub-Elements ---
        self.header = ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.on_back()),
                ft.Text("Virtual Classroom Hub", size=32, weight=ft.FontWeight.BOLD)
            ]
        )

        # --- Student Controls (Join Meeting) ---
        self.host_ip_input = ft.TextField(
            label="Host IP Address",
            hint_text="e.g., 192.168.1.10",
            prefix_icon=ft.Icons.WIFI,
            border_radius=8,
            width=300
        )

        self.meeting_code_input = ft.TextField(
            label="Meeting Code",
            hint_text="e.g., A1B2C3",
            prefix_icon=ft.Icons.LOCK,
            border_radius=8,
            width=300
        )

        self.join_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=30,
                width=400,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Icon(ft.Icons.GROUP_ADD, size=40, color=ft.Colors.BLUE_400),
                        ft.Text("Join a Class", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Enter the teacher's IP and meeting code to connect.", color=ft.Colors.OUTLINE),
                        self.host_ip_input,
                        self.meeting_code_input,
                        ft.ElevatedButton(
                            content=ft.Text("Join Meeting"),
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            width=300,
                            height=45,
                            on_click=self.handle_join_meeting
                        )
                    ]
                )
            )
        )

        # --- Teacher Controls (Create Meeting) ---
        self.create_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=30,
                width=400,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Icon(ft.Icons.CAST_FOR_EDUCATION, size=40, color=ft.Colors.GREEN_400),
                        ft.Text("Start a Class", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Launch a local server for your students to join.", color=ft.Colors.OUTLINE),
                        ft.Divider(height=80, color=ft.Colors.TRANSPARENT), # Spacing to match heights
                        ft.ElevatedButton(
                            content=ft.Text("Create Meeting"),
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            width=300,
                            height=45,
                            on_click=self.handle_create_meeting
                        )
                    ]
                )
            )
        )

        # Master Layout Assembly
        self.content = ft.Column(
            expand=True,
            controls=[
                self.header,
                ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=20),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=50,
                    controls=[
                        self.join_card,
                        self.create_card
                    ]
                )
            ]
        )

    # ==========================================
    # NETWORK LOGIC & ROUTING
    # ==========================================
    
    def handle_create_meeting(self, e):
        """Teacher clicks Create Meeting: Starts the Local Socket Server."""
        # Ensure session_data exists
        if not hasattr(self.page, 'session_data'):
            self.page.session_data = {}

        if "network" not in self.page.session_data:
            self.page.session_data["network"] = NetworkManager()
            
        network = self.page.session_data["network"]
        meeting_code, local_ip = network.start_server()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Server Started! IP: {local_ip} | Code: {meeting_code}"),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        self.on_enter_classroom()


    def handle_join_meeting(self, e):
        """Student clicks Join Meeting: Connects to the Teacher's Server via TCP."""
        ip_address = self.host_ip_input.value.strip() if self.host_ip_input.value else ""
        meeting_code = self.meeting_code_input.value.strip() if self.meeting_code_input.value else ""
        
        if not ip_address or not meeting_code:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Please enter IP and Meeting Code."), bgcolor=ft.Colors.RED_600)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Ensure session_data exists
        if not hasattr(self.page, 'session_data'):
            self.page.session_data = {}

        if "network" not in self.page.session_data:
            self.page.session_data["network"] = NetworkManager()
            
        network = self.page.session_data["network"]
        
        # Read user data stored during login
        user_name = self.page.session_data.get("user_name", "Student")
        user_role = self.page.session_data.get("user_role", "Student")
        
        success = network.connect_to_meeting(ip_address, meeting_code, user_name, user_role)
        
        if success:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Connected successfully!"), bgcolor=ft.Colors.GREEN_600)
            self.page.snack_bar.open = True
            self.page.update()
            self.on_enter_classroom()
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Connection failed. Check IP and Teacher Server."), bgcolor=ft.Colors.RED_600)
            self.page.snack_bar.open = True
            self.page.update()