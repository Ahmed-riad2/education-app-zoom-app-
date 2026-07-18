# screens/auth_screen.py
import flet as ft
from services.auth_service import AuthService

class AuthScreen(ft.Container):
    def __init__(self, on_auth_success):
        """
        Initialize the Authentication Screen.
        :param on_auth_success: Function to route to the main dashboard upon successful login.
        """
        super().__init__()
        self.on_auth_success = on_auth_success
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        
        # FIXED: Using ft.Alignment(0, 0) instead of the deprecated ft.alignment.center constant
        self.alignment = ft.Alignment(0, 0)

        # --- Inputs (Bound to 'self' so the backend can read them) ---
        self.email_input = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=8,
            width=350,
            autofocus=True
        )

        self.password_input = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_radius=8,
            width=350,
            on_submit=self.handle_submit # Allows hitting 'Enter' to login
        )

        self.remember_me = ft.Checkbox(label="Remember Me", value=False)

        # --- UI Assembly ---
        self.content = ft.Card(
            elevation=8,
            content=ft.Container(
                padding=40,
                width=450,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL, size=60, color=ft.Colors.BLUE_500),
                        ft.Text("EduVerse AI", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Sign in to your account", color=ft.Colors.OUTLINE),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        
                        # Add the bound inputs to the UI
                        self.email_input,
                        self.password_input,
                        
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                self.remember_me,
                                ft.TextButton(
                                    content=ft.Text("Forgot Password?"), 
                                    on_click=self.handle_forgot_password
                                )
                            ]
                        ),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            content=ft.Text("Login"),
                            width=350,
                            height=45,
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            on_click=self.handle_submit
                        )
                    ]
                )
            )
        )

    def handle_forgot_password(self, e):
        """Mock functionality for password reset."""
        email = self.email_input.value.strip() if self.email_input.value else ""
        if not email:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter your email to reset the password."),
                bgcolor=ft.Colors.ORANGE_600
            )
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Password reset link sent to {email}."),
                bgcolor=ft.Colors.GREEN_600
            )
        
        self.page.snack_bar.open = True
        self.page.update()

    def handle_submit(self, e):
        """Processes authentication via SQLite backend."""
        email = self.email_input.value.strip() if self.email_input.value else ""
        password = self.password_input.value.strip() if self.password_input.value else ""

        if not email or not password:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Please enter both email and password."),
                bgcolor=ft.Colors.RED_600
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Backend Verification
        user_data = AuthService.authenticate_user(email, password)

        if user_data:
            # FIXED: Bypass Flet's volatile storage API and use a native Python dictionary
            if not hasattr(self.page, 'session_data'):
                self.page.session_data = {}
                
            self.page.session_data["user_id"] = user_data["id"]
            self.page.session_data["user_name"] = user_data["name"]
            self.page.session_data["user_email"] = user_data["email"]
            self.page.session_data["user_role"] = user_data["role"]
            
            # Navigate to Dashboard
            self.on_auth_success()
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid credentials. Please try again."),
                bgcolor=ft.Colors.RED_600
            )
            self.page.snack_bar.open = True
            self.page.update()