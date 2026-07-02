import flet as ft

class AssignmentScreen(ft.Container):
    def __init__(self, on_back_to_dashboard):
        """
        Initialize the Assignment System.
        :param on_back_to_dashboard: Function to route back to the main lobby.
        """
        super().__init__()
        self.on_back_to_dashboard = on_back_to_dashboard
        self.expand = True
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 30

        # Simulation Application Memory State Rows
        self.assignments_data = [
            {"title": "Thermodynamics Lab Report", "subject": "Advanced Physics", "due": "Tomorrow, 11:59 PM", "status": "Pending"},
            {"title": "Loop Structures Practice", "subject": "Computer Science", "due": "In 3 days", "status": "Submitted"}
        ]
        self.submissions_data = [
            {"student": "Alex Bradley", "assignment": "Thermodynamics Lab Report", "file": "thermo_lab_draft.pdf", "grade": ""},
            {"student": "Sarah Jenkins", "assignment": "Thermodynamics Lab Report", "file": "final_report_v2.pdf", "grade": "A"}
        ]

        # --- Dynamic View Container ---
        self.dynamic_view = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        # --- Top Menu Actions ---
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=self.go_back),
                        ft.Text("Assignment Desk", size=32, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Dropdown(
                    label="View Role Profile",
                    width=200,
                    value="Student",
                    options=[
                        ft.DropdownOption("Student"),
                        ft.DropdownOption("Teacher")
                    ],
                    on_change=self.handle_role_toggle
                )
            ]
        )

        # Build initial display layout state
        self.content = ft.Column(
            expand=True,
            controls=[
                self.header,
                ft.Divider(color=ft.Colors.OUTLINE_VARIANT, height=20),
                self.dynamic_view
            ]
        )
        
        # Render default student interface on initialization pass
        self.render_student_interface()

    def go_back(self, e):
        """Helper to safely execute the back transition callback."""
        if self.on_back_to_dashboard:
            self.on_back_to_dashboard()

    def handle_role_toggle(self, e):
        """Switches the interface mode dynamically based on selection entries."""
        if e.control.value == "Teacher":
            self.render_teacher_interface()
        else:
            self.render_student_interface()

    def render_student_interface(self):
        """Generates dynamic layouts tracking active homework queues."""
        self.dynamic_view.controls.clear()
        
        self.dynamic_view.controls.append(
            ft.Text("Your Active Assignments", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
        )

        for assignment in self.assignments_data:
            status_color = ft.Colors.ORANGE_400 if assignment["status"] == "Pending" else ft.Colors.GREEN_400
            
            # Extract Textfield declaration to read its value on click
            input_field = ft.TextField(
                hint_text="Enter file name or document path link...", 
                expand=True,
                border_radius=8,
                text_size=14
            )

            # Create button click handler separately to clean up inline lambdas
            def make_submit_handler(title=assignment["title"], field=input_field):
                return lambda e: self.handle_student_submit(title, field)

            pending_action_row = ft.Row(
                controls=[
                    input_field,
                    ft.ElevatedButton(
                        content=ft.Text("Submit Work"),
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        on_click=make_submit_handler()
                    )
                ]
            )

            card_content = ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(assignment["title"], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Course: {assignment['subject']} | Due: {assignment['due']}", color=ft.Colors.OUTLINE)
                                ]
                            ),
                            ft.Chip(
                                label=ft.Text(assignment["status"]),
                                bgcolor=status_color
                            )
                        ]
                    ),
                    ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                    pending_action_row if assignment["status"] == "Pending" else ft.Text("✓ Submission successfully filed with instructional staff.", color=ft.Colors.GREEN_300, italic=True)
                ]
            )

            self.dynamic_view.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=card_content
                    )
                )
            )
        self.update()

    def render_teacher_interface(self):
        """Generates control panels allowing teachers to publish exercises and file grades."""
        self.dynamic_view.controls.clear()
        
        # References for creating new assignments
        self.new_title = ft.TextField(label="Assignment Name", hint_text="e.g., Quantum Mechanics Essay")
        self.new_subject = ft.TextField(label="Subject/Course", hint_text="e.g., Physics II")
        self.new_due = ft.TextField(label="Due Date Template", hint_text="e.g., Friday, 5:00 PM", expand=True)

        # Section A: Publish Creation Panel
        self.dynamic_view.controls.extend([
            ft.Text("Create New Learning Assignment", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            self.new_title,
                            self.new_subject,
                            ft.Row(
                                spacing=15,
                                controls=[
                                    self.new_due,
                                    ft.ElevatedButton(
                                        content=ft.Text("Publish Task"),
                                        bgcolor=ft.Colors.GREEN_600,
                                        color=ft.Colors.WHITE,
                                        on_click=self.handle_create_assignment
                                    )
                                ]
                            )
                        ]
                    )
                )
             )],
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            ft.Text("Student Submission Assessment Board", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
        ) # <--- FIXED SYNTAX ERROR HERE

        # Section B: Assessment Verification Board Rows
        for sub in self.submissions_data:
            grade_box = ft.TextField(
                label="Grade", 
                value=sub["grade"], 
                width=120, 
                text_align=ft.TextAlign.CENTER,
                border_radius=8
            )
            
            def make_file_handler(filename=sub["file"]):
                return lambda e: self.handle_view_file(filename)

            def make_grade_handler(student_name=sub["student"], box=grade_box):
                return lambda e: self.handle_save_grade(student_name, box)

            sub_info_col = ft.Column(
                controls=[
                    ft.Text(sub["student"], weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(f"Task: {sub['assignment']}", size=14, color=ft.Colors.OUTLINE),
                    ft.TextButton(
                        content=ft.Row(controls=[ft.Icon(ft.Icons.ATTACH_FILE, size=16), ft.Text(sub["file"])]),
                        on_click=make_file_handler()
                    )
                ]
            )

            actions_row = ft.Row(
                spacing=10,
                controls=[
                    grade_box,
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE_ROUNDED,
                        icon_color=ft.Colors.GREEN_400,
                        tooltip="Commit Grade Entry",
                        on_click=make_grade_handler()
                    )
                ]
            )

            row_container = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[sub_info_col, actions_row]
            )

            self.dynamic_view.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=row_container
                    )
                )
            )
        self.update()

    def handle_student_submit(self, assignment_title, field_ref):
        """Processes simulation hooks for student file uploads."""
        submission_text = field_ref.value.strip()
        if not submission_text:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a file link or description before submitting!"), bgcolor=ft.Colors.RED_600)
            self.page.snack_bar.open = True
            self.page.update()
            return

        for assignment in self.assignments_data:
            if assignment["title"] == assignment_title:
                assignment["status"] = "Submitted"
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Submitted: '{submission_text}' for {assignment_title}"),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.render_student_interface()

    def handle_create_assignment(self, e):
        """Simulates creation verification alerts for publishing pipelines."""
        if not self.new_title.value.strip() or not self.new_subject.value.strip():
            return
        
        # Actually save data to internal list state
        self.assignments_data.append({
            "title": self.new_title.value.strip(),
            "subject": self.new_subject.value.strip(),
            "due": self.new_due.value.strip() or "No Deadline",
            "status": "Pending"
        })

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("New assignment published successfully!"),
            bgcolor=ft.Colors.GREEN_600
        )
        self.page.snack_bar.open = True
        self.render_teacher_interface() # Re-render panel

    def handle_view_file(self, filename):
        """Triggers simulated file reading action notification sheets."""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Downloading assignment workspace package: {filename}"))
        self.page.snack_bar.open = True
        self.page.update()

    def handle_save_grade(self, student_name, grade_input_field):
        """Saves grade box configurations directly back into dataset rows safely."""
        grade_val = grade_input_field.value.strip()
        if not grade_val:
            return
            
        for sub in self.submissions_data:
            if sub["student"] == student_name:
                sub["grade"] = grade_val
                
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Grade ledger updated for {student_name} -> [{grade_val}]"),
            bgcolor=ft.Colors.BLUE_600
        )
        self.page.snack_bar.open = True
        self.page.update()