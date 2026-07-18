# screens/settings_screen.py
import flet as ft

class SettingsScreen(ft.Container):
    def __init__(self, on_back_to_dashboard):
        """
        Initialize the Settings & Theme Configuration Screen.
        :param on_back_to_dashboard: Function to route back to the main dashboard.
        """
        super().__init__()
        self.on_back_to_dashboard = on_back_to_dashboard
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 40

        # --- UI Sub-Elements ---
        self.header = ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=self.go_back),
                ft.Text("Account & Preferences", size=32, weight=ft.FontWeight.BOLD)
            ]
        )

        # Dynamic Switch Elements
        self.theme_switch = ft.Switch(
            label="Enable Dark Mode Workspace",
            value=True, # Starts in dark mode as specified in main.py
            on_change=self.handle_theme_toggle
        )

        self.notification_switch = ft.Switch(
            label="Push Alerts for Upcoming Classes",
            value=True
        )

        # Profile Information Section
        self.profile_card = ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.CircleAvatar(
                                    content=ft.Text("AB", color=ft.Colors.WHITE),
                                    bgcolor=ft.Colors.BLUE_600,
                                    radius=30
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Alex Bradley", size=20, weight=ft.FontWeight.BOLD),
                                        ft.Text("Role Profile: Advanced Student Tier", color=ft.Colors.OUTLINE)
                                    ]
                                )
                            ],
                            spacing=15
                        ),
                        ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=20),
                        ft.TextField(label="Registered Email Address", value="alex.bradley@eduverse.ai", disabled=True),
                        ft.TextField(label="Classroom Key Signature", value="EDUV-982X-2026", password=True, can_reveal_password=True)
                    ],
                    spacing=12
                )
            )
        )

        # System Settings Section
        self.preferences_card = ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text("Application Environment Preferences", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300),
                        ft.Divider(color=ft.Colors.TRANSPARENT, height=5),
                        self.theme_switch,
                        self.notification_switch,
                        ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                        # FIXED: Swapped 'text' parameter for the required 'content' parameter and ft.Text block
                        ft.ElevatedButton(
                            content=ft.Text("Apply Configuration Changes"),
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            on_click=self.handle_save_confirmation
                        )
                    ],
                    spacing=10
                )
            )
        )

        # Master Layout Assembly
        self.content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self.header,
                ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=20),
                ft.Text("User Profile Ledger", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                self.profile_card,
                ft.Divider(color=ft.Colors.TRANSPARENT, height=20),
                ft.Text("System Adjustments", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                self.preferences_card
            ]
        )

    def go_back(self, e):
        """Safely triggers navigation pipeline backwards."""
        self.on_back_to_dashboard()

    def handle_theme_toggle(self, e):
        """Modifies Flet global system theme modes programmatically on the fly."""
        if self.page:
            # Swap window property state mappings
            if e.control.value:
                self.page.theme_mode = ft.ThemeMode.DARK
                self.theme_switch.label = "Enable Dark Mode Workspace"
            else:
                self.page.theme_mode = ft.ThemeMode.LIGHT
                self.theme_switch.label = "Enable Light Mode Workspace"
            
            # Force the engine to sync color mappings across active page contexts
            self.page.update()

    def handle_save_confirmation(self, e):
        """Displays visual snackbar sheets verification notifications."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("System configuration matrices updated successfully!"),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.page.update()