# main.py
import flet as ft
from screens.splash_screen import SplashScreen
from screens.auth_screen import AuthScreen
from screens.dashboard_screen import DashboardScreen
from screens.classroom_screen import ClassroomScreen
from screens.ai_summary_screen import AISummaryScreen # NEW IMPORT
from screens.assignment_screen import AssignmentScreen # NEW IMPORT
from screens.quiz_screen import QuizScreen
from screens.settings_screen import SettingsScreen
from database.db_manager import init_db
class EduVerseApp:

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "EduVerse AI"
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.window.min_width = 800
        self.page.window.min_height = 600
        self.page.padding = 0
        
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_700, font_family="Roboto")

        self.show_splash_screen()

    def show_splash_screen(self):
        self.page.controls.clear()
        splash = SplashScreen(on_loading_complete=self.show_auth_screen)
        self.page.add(splash)
        self.page.update()

    def show_auth_screen(self):
        self.page.controls.clear()
        auth = AuthScreen(on_auth_success=self.show_dashboard)
        self.page.add(auth)
        self.page.update()

    def show_dashboard(self):
        self.page.controls.clear()
        dashboard = DashboardScreen(
            on_join_class=self.show_classroom,
            on_open_meeting_hub=self.show_meeting_hub,
            on_open_assignments=self.show_assignments,
            on_open_quizzes=self.show_quizzes, # NEW
            on_open_settings=self.show_settings  # NEW
        )
        self.page.add(dashboard)
        self.page.update()  


    def show_quizzes(self):
        self.page.controls.clear()
        quiz_panel = QuizScreen(on_back_to_dashboard=self.show_dashboard)
        self.page.add(quiz_panel)
        self.page.update()

    def show_assignments(self):
        """Clear the page and route to the Assignment System screen."""
        self.page.controls.clear()
        assignment_panel = AssignmentScreen(on_back_to_dashboard=self.show_dashboard)
        self.page.add(assignment_panel)
        self.page.update()

    def show_meeting_hub(self):
        self.page.controls.clear()
        import screens.meeting_hub_screen as mh
        hub = mh.MeetingHubScreen(
            on_enter_classroom=self.show_classroom,
            on_back=self.show_dashboard
        )
        self.page.add(hub)
        self.page.update()

    def show_classroom(self):
        self.page.controls.clear()
        # ROUTING CHANGE: When leaving class, redirect straight to the AI summary engine
        classroom = ClassroomScreen(on_leave_class=self.show_ai_summary)
        self.page.add(classroom)
        self.page.update()

    def show_ai_summary(self):
        """Clear the page and route to the AI Summary Generator Screen."""
        self.page.controls.clear()
        summary = AISummaryScreen(on_return_home=self.show_dashboard)
        self.page.add(summary)
        self.page.update()

    def show_settings(self):
     """Clear the page and route to the System Settings screen."""
     self.page.controls.clear()
     settings_panel = SettingsScreen(on_back_to_dashboard=self.show_dashboard)
     self.page.add(settings_panel)
     self.page.update()        
    
def main(page: ft.Page):
    """Entry point of the Flet application."""
    init_db() # Initializes SQLite on startup
    app = EduVerseApp(page)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")