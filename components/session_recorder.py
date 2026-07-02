# components/session_recorder.py
import flet as ft
import time
import threading
from datetime import datetime

class SessionRecorder(ft.Container):
    def __init__(self, on_transcript_update):
        """
        Initialize the AI Session Recorder Component.
        :param on_transcript_update: Callback function triggered whenever a new line of text is processed.
        """
        super().__init__()
        self.on_transcript_update = on_transcript_update
        
        # Configure container base properties
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW
        self.border_radius = 12
        self.padding = 15
        
        # Internal Recording State
        self.is_recording = False
        self.seconds_elapsed = 0
        self.recording_thread = None
        self.timer_thread = None

        # --- UI Sub-Elements ---
        self.status_icon = ft.Icon(ft.Icons.RADIO_BUTTON_CHECKED, color=ft.Colors.OUTLINE, size=20)
        self.status_text = ft.Text("AI Recorder Idle", weight=ft.FontWeight.W_500, color=ft.Colors.OUTLINE)
        self.timer_text = ft.Text("00:00:00", size=16, weight=ft.FontWeight.BOLD)
        
        # Buttons
        self.record_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            tooltip="Start AI Recording",
            on_click=self.start_recording
        )
        self.stop_btn = ft.IconButton(
            icon=ft.Icons.STOP_ROUNDED,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_600,
            tooltip="Stop & Save Session",
            disabled=True,
            on_click=self.stop_recording
        )

        # Layout Assembly
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    self.status_icon,
                    ft.Column([
                        self.status_text,
                        self.timer_text
                    ], spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    self.record_btn,
                    self.stop_btn
                ], spacing=10)
            ]
        )

    def start_recording(self, e):
        """Activates background routines to capture audio stream data."""
        if self.is_recording:
            return

        self.is_recording = True
        self.status_icon.color = ft.Colors.RED_500
        self.status_text.value = "AI Transcribing Live..."
        self.status_text.color = ft.Colors.RED_400
        self.record_btn.disabled = True
        self.stop_btn.disabled = False
        self.update()

        # Spin up concurrent worker threads to protect the primary UI thread
        self.recording_thread = threading.Thread(target=self._speech_recognition_worker, daemon=True)
        self.timer_thread = threading.Thread(target=self._timer_worker, daemon=True)
        
        self.recording_thread.start()
        self.timer_thread.start()

    def stop_recording(self, e):
        """Halts worker threads and securely finalizes session data tracking."""
        if not self.is_recording:
            return

        self.is_recording = False
        self.status_icon.color = ft.Colors.OUTLINE
        self.status_text.value = "Recording Saved Successfully"
        self.status_text.color = ft.Colors.GREEN_400
        self.record_btn.disabled = False
        self.stop_btn.disabled = True
        self.update()

    def _timer_worker(self):
        """Asynchronously counts clock ticks to manage duration metrics safely."""
        while self.is_recording:
            time.sleep(1)
            if not self.is_recording:
                break
            self.seconds_elapsed += 1
            
            # Format time metrics into readable text layout
            hrs = self.seconds_elapsed // 3600
            mins = (self.seconds_elapsed % 3600) // 60
            secs = self.seconds_elapsed % 60
            
            self.timer_text.value = f"{hrs:02d}:{mins:02d}:{secs:02d}"
            
            # Safe boundary hook for Flet window rendering updates
            if self.page:
                self.page.update()

    def _speech_recognition_worker(self):
        """Simulates speech-to-text data packets being received asynchronously."""
        # Realistic programmatic lecture phrases to simulate processing inputs
        mock_lecture_snippets = [
            "Welcome back class. Today we're exploring deep space thermodynamics.",
            "Notice how heat transfers across non-reflective atmospheric bodies.",
            "This principle underpins our secondary laboratory calculations.",
            "Make sure to open your assignments tab and read section four.",
            "We will synthesize these core results during next week's testing phase."
        ]
        
        snippet_index = 0
        while self.is_recording:
            # Sleep for 4 seconds to replicate normal human speech patterns
            time.sleep(4)
            if not self.is_recording:
                break
            
            if snippet_index < len(mock_lecture_snippets):
                current_text = mock_lecture_snippets[snippet_index]
                snippet_index += 1
            else:
                current_text = "Continuing live instructional sequence monitoring..."

            # Safe cross-thread invocation to feed text packet back to main application screen
            if self.page:
                self.on_transcript_update(current_text)