# screens/dashboard_screen.py
import flet as ft

class DashboardScreen(ft.Container):
    def __init__(self, on_join_class, on_open_meeting_hub, on_open_assignments):
        """
        Initialize the main Dashboard interface.
        :param on_join_class: Function to route directly to a classroom.
        :param on_open_meeting_hub: Function to route to the Meeting Management screen.
        :param on_open_assignments: Function to route to the Assignment management screen.
        """
        super().__init__()
        self.on_join_class = on_join_class
        self.on_open_meeting_hub = on_open_meeting_hub
        self.on_open_assignments = on_open_assignments  # FIXED: Now explicitly stored
        
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        
        # --- Sidebar Navigation Rail ---
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.VIDEO_CAMERA_FRONT_OUTLINED, selected_icon=ft.Icons.VIDEO_CAMERA_FRONT, label="Classroom"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ASSIGNMENT_OUTLINED, selected_icon=ft.Icons.ASSIGNMENT, label="Assignments"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.QUIZ_OUTLINED, selected_icon=ft.Icons.QUIZ, label="Quizzes"
                ),
            ],
            on_change=self.handle_nav_change,
        )

        # --- Main Content Area ---
        self.main_content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Dashboard Overview", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Top Statistics Row
                self.create_stats_row(),
                
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                
                # Upcoming Classes Section
                ft.Text("Upcoming Classes", size=24, weight=ft.FontWeight.BOLD),
                self.create_upcoming_class_card("Advanced Physics", "Today at 10:00 AM - Dr. Smith", ft.Icons.SCIENCE),
                self.create_upcoming_class_card("Computer Science", "Tomorrow at 2:00 PM - Mrs. Lovelace", ft.Icons.COMPUTER),
            ]
        )

        # --- Assemble the Screen ---
        self.content = ft.Row(
            expand=True,
            controls=[
                self.rail,
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=self.main_content,
                    expand=True,
                    padding=40
                )
            ]
        )

    def create_stats_row(self):
        """Helper method to generate a row of statistic cards."""
        return ft.Row(
            controls=[
                self.create_stat_card("Active Courses", "4", ft.Icons.BOOK, ft.Colors.BLUE_400),
                self.create_stat_card("Pending Assignments", "2", ft.Icons.ASSIGNMENT_LATE, ft.Colors.ORANGE_400),
                self.create_stat_card("Average Score", "92%", ft.Icons.STARS, ft.Colors.GREEN_400),
            ],
            alignment=ft.MainAxisAlignment.START,
            wrap=True
        )

    def create_stat_card(self, title, value, icon_name, icon_color):
        """Helper method to build an individual statistic card."""
        return ft.Card(
            elevation=4,
            content=ft.Container(
                padding=20,
                width=250,
                content=ft.Column(
                    controls=[
                        ft.Icon(icon_name, color=icon_color, size=40),
                        ft.Text(value, size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(title, color=ft.Colors.OUTLINE)
                    ]
                )
            )
        )

    def create_upcoming_class_card(self, title, subtitle, icon_name):
        """Helper method to build a row for an upcoming class."""
        return ft.Card(
            elevation=2,
            margin=ft.Margin.only(bottom=10), 
            content=ft.Container(
                padding=10,
                content=ft.ListTile(
                    leading=ft.Icon(icon_name, size=40, color=ft.Colors.BLUE_300),
                    title=ft.Text(title, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(subtitle),
                    trailing=ft.ElevatedButton(
                        content="Join", 
                        bgcolor=ft.Colors.BLUE_600, 
                        color=ft.Colors.WHITE,
                        on_click=lambda _: self.on_join_class()
                    )
                )
            )
        )

    def handle_nav_change(self, e):
        """Handles clicks on the sidebar navigation rail."""
        index = e.control.selected_index
        if index == 1:    # Classroom Icon
            self.on_open_meeting_hub()
        elif index == 2:  # Assignments Icon
            self.on_open_assignments()  # FIXED: Routing execution now cleanly maps here