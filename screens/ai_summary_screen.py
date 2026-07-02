# screens/ai_summary_screen.py
import flet as ft

class AISummaryScreen(ft.Container):
    def __init__(self, on_return_home):
        """
        Initialize the AI Generated Summary Screen.
        :param on_return_home: Function to route back to the main dashboard.
        """
        super().__init__()
        self.on_return_home = on_return_home
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 30

        # --- 1. Header Section ---
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column([
                    ft.Text("AI Session Insights", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text("Advanced Physics - Section: Thermodynamics", color=ft.Colors.OUTLINE)
                ]),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.PICTURE_AS_PDF, size=18), ft.Text("Export PDF")]),
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        on_click=self.handle_export_pdf
                    ),
                    ft.TextButton(
                        content=ft.Text("Dashboard"),
                        on_click=lambda _: self.on_return_home()
                    )
                ], spacing=10)
            ]
        )

        # --- 2. Content Tabs (FIXED for Flet 0.80+ Architecture) ---
        self.tabs = ft.Tabs(
            selected_index=0,
            length=3, # Must explicitly define the total number of tabs
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    # The TabBar handles the clickable buttons
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Lesson Summary", icon=ft.Icons.ARTICLE),
                            ft.Tab(label="Key Concepts", icon=ft.Icons.LIGHTBULB),
                            ft.Tab(label="Homework & Flashcards", icon=ft.Icons.SCHOOL)
                        ]
                    ),
                    # The TabBarView securely holds and animates the corresponding content blocks
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            self.build_summary_tab(),
                            self.build_concepts_tab(),
                            self.build_homework_tab()
                        ]
                    )
                ]
            )
        )

        # --- Assemble Screen ---
        self.content = ft.Column(
            expand=True,
            controls=[
                self.header,
                ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=20),
                self.tabs
            ]
        )

    def build_summary_tab(self):
        """Builds the layout for the narrative summary tab."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text("Executive Summary", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Text(
                        "Today's lecture focused extensively on deep space thermodynamics, specifically investigating "
                        "how thermal energy transfers across cold, non-reflective atmospheric bodies. The session "
                        "established mathematical baselines for secondary laboratory calculations and mapped out "
                        "predictive models for heat dissipation in vacuum environments.",
                        size=16
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    ft.Text("Core Transcript Timeline", size=18, weight=ft.FontWeight.BOLD),
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Text(
                                "[10:02] Dr. Smith initiated the session covering vacuum conditions.\n"
                                "[10:15] Analyzed transfer coefficients on non-reflective planetary hulls.\n"
                                "[10:32] Reviewed assignment specifications outlined in section four.",
                                font_family="Courier",
                                size=14
                            )
                        )
                    )
                ]
            )
        )

    def build_concepts_tab(self):
        """Builds the layout highlighting vital educational definitions."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=15,
                controls=[
                    ft.Text("Extracted Key Terms", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    self.create_concept_tile("Thermodynamics", "The branch of physical science that deals with the relations between heat and other forms of energy."),
                    self.create_concept_tile("Non-Reflective Bodies", "Atmospheric or planetary entities that absorb maximum incoming solar or external radiation without scattering light back into space."),
                    self.create_concept_tile("Vacuum Transfer Hulls", "Specially designed structures built to safely measure mechanical heat dispersion inside zero-atmosphere testing environments.")
                ]
            )
        )

    def create_concept_tile(self, term, definition):
        """Helper to create a clean card for individual concepts."""
        return ft.Card(
            elevation=2,
            content=ft.Container(
                padding=15,
                content=ft.Column([
                    ft.Text(term, weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_200),
                    ft.Text(definition, size=14)
                ], spacing=5)
            )
        )

    def build_homework_tab(self):
        """Builds interactive flashcards and assignment prompts."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                controls=[
                    ft.Text("AI Assigned Homework Tasks", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Text("1. Complete the secondary laboratory calculations matching today's equation dataset.", size=15),
                    ft.Text("2. Read Section Four thoroughly and prepare a 200-word paragraph summarizing vacuum heat transfer boundaries.", size=15),
                    
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    
                    ft.Text("Interactive Flashcards", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.create_flashcard("Question", "What happens to heat in a complete vacuum?"),
                        self.create_flashcard("Answer", "It radiates entirely as electromagnetic waves since no medium exists for conduction.")
                    ], spacing=20, wrap=True)
                ]
            )
        )

    def create_flashcard(self, label, text):
        """Helper to render a clean, professional flashcard box."""
        accent = ft.Colors.BLUE_800 if label == "Question" else ft.Colors.GREEN_800
        return ft.Container(
            width=280,
            height=140,
            bgcolor=accent,
            border_radius=12,
            padding=15,
            alignment=ft.Alignment.CENTER,
            content=ft.Column([
                ft.Text(label, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE60),
                ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def handle_export_pdf(self, e):
        """Simulates report generation pipeline processing."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("PDF Compiled Successfully! Saved to /reports/summary_thermo.pdf"),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.page.update()