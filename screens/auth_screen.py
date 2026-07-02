# screens/auth_screen.py
import flet as ft

class AuthScreen(ft.Container):
    def __init__(self, on_auth_success):
        """
        Initialize the Authentication Screen (Login/Signup).
        :param on_auth_success: Function to call when login is successful.
        """
        super().__init__()
        self.on_auth_success = on_auth_success
        self.expand = True
        self.alignment = ft.Alignment.CENTER
        self.bgcolor = ft.Colors.SURFACE

        # State variable to track if we are in "Login" or "Signup" mode
        self.is_login = True

        # --- UI Components ---
        self.title = ft.Text("Welcome Back", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
        self.subtitle = ft.Text("Login to continue your learning journey.", color=ft.Colors.OUTLINE)

        # Input Fields
        self.name_field = ft.TextField(label="Full Name", prefix_icon=ft.Icons.PERSON, visible=False)
        self.email_field = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL)
        self.password_field = ft.TextField(
            label="Password", 
            prefix_icon=ft.Icons.LOCK, 
            password=True, 
            can_reveal_password=True
        )
        
        # Extras
        self.remember_me = ft.Checkbox(label="Remember Me", value=False)
        self.forgot_password = ft.TextButton(content="Forgot Password?") 
        
        # Main Action Button
        self.submit_btn = ft.ElevatedButton(
            content="Login", 
            width=300, 
            bgcolor=ft.Colors.BLUE_600, 
            color=ft.Colors.WHITE,
            on_click=self.handle_submit
        )

        # Toggle Action (Switch between Login and Signup)
        self.toggle_btn = ft.TextButton(
            content="Don't have an account? Sign up here.",
            on_click=self.toggle_mode
        )

        # Assemble the UI inside a Card for a clean, floating look
        self.content = ft.Card(
            elevation=10,
            # FIXED: Removed color=ft.Colors.SURFACE_VARIANT. 
            # The Card will now automatically theme itself based on elevation.
            content=ft.Container(
                padding=40,
                width=400,
                content=ft.Column(
                    controls=[
                        self.title,
                        self.subtitle,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Spacer
                        self.name_field,
                        self.email_field,
                        self.password_field,
                        ft.Row([self.remember_me, self.forgot_password], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=10),
                        self.submit_btn,
                        self.toggle_btn
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        )

    def toggle_mode(self, e):
        """Switches the UI between Login and Signup modes."""
        self.is_login = not self.is_login
        
        if self.is_login:
            self.title.value = "Welcome Back"
            self.subtitle.value = "Login to continue your learning journey."
            self.name_field.visible = False
            self.remember_me.visible = True
            self.forgot_password.visible = True
            self.submit_btn.content = "Login"
            self.toggle_btn.content = "Don't have an account? Sign up here."
        else:
            self.title.value = "Join EduVerse"
            self.subtitle.value = "Create an account to start learning."
            self.name_field.visible = True
            self.remember_me.visible = False
            self.forgot_password.visible = False
            self.submit_btn.content = "Sign Up"
            self.toggle_btn.content = "Already have an account? Login here."
            
        self.update()

    def handle_submit(self, e):
        """Handle the login/signup logic (Mocked for now)."""
        if not self.email_field.value or not self.password_field.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields!"), bgcolor=ft.Colors.RED_500)
            self.page.snack_bar.open = True
            self.page.update()
            return
            
        # Proceed to next screen
        self.on_auth_success()