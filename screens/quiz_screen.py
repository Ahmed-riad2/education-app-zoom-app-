# screens/quiz_screen.py
import flet as ft

class QuizScreen(ft.Container):
    def __init__(self, on_back_to_dashboard):
        """
        Initialize the Quiz System.
        :param on_back_to_dashboard: Function to route back to the main lobby.
        """
        super().__init__()
        self.on_back_to_dashboard = on_back_to_dashboard
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 40

        # --- Quiz State Data ---
        self.questions = [
            {
                "question": "What is the primary mechanism of heat transfer in a vacuum?",
                "options": ["Conduction", "Convection", "Radiation", "Evaporation"],
                "answer": "Radiation"
            },
            {
                "question": "Which Python keyword is used to create a background thread?",
                "options": ["async", "threading", "await", "multiprocessing"],
                "answer": "threading"
            },
            {
                "question": "In Flet, which layout control handles scrolling items vertically?",
                "options": ["ft.Row", "ft.Container", "ft.Stack", "ft.ListView"],
                "answer": "ft.ListView"
            }
        ]
        self.current_index = 0
        self.score = 0
        self.selected_option = None

        # --- UI Elements ---
        self.header = ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.on_back_to_dashboard()),
                ft.Text("Knowledge Check", size=32, weight=ft.FontWeight.BOLD)
            ]
        )

        # Dynamic Question Elements
        self.question_title = ft.Text("", size=24, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_300)
        
        # RadioGroup handles the exclusive selection (only one option can be selected)
        self.options_group = ft.RadioGroup(
            content=ft.Column(spacing=15, controls=[]), 
            on_change=self.on_option_select
        )
        
        self.btn_text = ft.Text("Next Question")
        self.next_btn = ft.ElevatedButton(
            content=self.btn_text,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            disabled=True,
            on_click=self.handle_next
        )

        self.quiz_content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                self.question_title,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.options_group,
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                self.next_btn
            ]
        )

        # Base Layout Assembly
        self.content = ft.Column(
            expand=True,
            controls=[
                self.header,
                ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=20),
                self.quiz_content
            ]
        )

    def did_mount(self):
        """Loads the first question as soon as the screen is attached."""
        self.load_question()

    def load_question(self):
        """Injects the current question and options into the UI."""
        if self.current_index < len(self.questions):
            q_data = self.questions[self.current_index]
            
            # Update title
            self.question_title.value = f"Question {self.current_index + 1} of {len(self.questions)}:\n{q_data['question']}"
            
            # Clear and populate radio buttons
            self.options_group.value = None
            self.options_group.content.controls.clear()
            for opt in q_data["options"]:
                self.options_group.content.controls.append(ft.Radio(value=opt, label=opt))
            
            # Lock the next button until an answer is clicked
            self.next_btn.disabled = True
            
            # Change button text on the final question
            if self.current_index == len(self.questions) - 1:
                self.btn_text.value = "Submit Quiz"
                
            if self.page:
                self.update()
        else:
            self.show_results()

    def on_option_select(self, e):
        """Unlocks the Next button when a user selects a radio option."""
        self.selected_option = e.control.value
        self.next_btn.disabled = False
        self.update()

    def handle_next(self, e):
        """Checks the answer, increments the score, and loads the next view."""
        correct_answer = self.questions[self.current_index]["answer"]
        
        if self.selected_option == correct_answer:
            self.score += 1
            
        self.current_index += 1
        self.load_question()

    def show_results(self):
        """Replaces the question UI with a final score overview."""
        self.quiz_content.controls.clear()
        
        percentage = (self.score / len(self.questions)) * 100
        color = ft.Colors.GREEN_400 if percentage >= 70 else ft.Colors.ORANGE_400
        
        self.quiz_content.controls.extend([
            ft.Text("Quiz Completed!", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
            ft.Text(f"Final Score: {self.score} out of {len(self.questions)}", size=24),
            ft.Text(f"{percentage:.0f}%", size=48, weight=ft.FontWeight.BOLD, color=color),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton(
                content=ft.Text("Return to Dashboard"), 
                bgcolor=ft.Colors.GREEN_600, 
                color=ft.Colors.WHITE, 
                on_click=lambda _: self.on_back_to_dashboard()
            )
        ])
        
        if self.page:
            self.update()