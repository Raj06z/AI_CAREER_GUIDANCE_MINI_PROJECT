"""
==============================================================================
GUI Module — Tkinter User Interface
==============================================================================
Description : Modern, professional Tkinter GUI for the Career Guidance
              Expert System. Implements a multi-screen wizard-style interface
              with animated progress, styled widgets, and rich result display.
==============================================================================
"""

import tkinter as tk
from tkinter import ttk, font, messagebox
import threading
import time

from knowledge_base import QUESTIONS
from inference_engine import InferenceEngine
from recommendation import CareerRecommendationModule


# =============================================================================
# COLOR PALETTE & THEME CONSTANTS
# =============================================================================
COLORS = {
    "bg_dark":       "#0D1117",   # Deep dark background
    "bg_card":       "#161B22",   # Card/panel background
    "bg_input":      "#21262D",   # Input/option background
    "accent":        "#58A6FF",   # Primary blue accent
    "accent2":       "#3FB950",   # Green secondary accent
    "accent3":       "#F78166",   # Warm highlight
    "text_primary":  "#E6EDF3",   # Main text
    "text_secondary":"#8B949E",   # Muted text
    "text_dim":      "#484F58",   # Very dim text
    "border":        "#30363D",   # Border color
    "gold":          "#F0C040",   # Gold for top match
    "silver":        "#A0AFBE",   # Silver for 2nd
    "bronze":        "#C76B3A",   # Bronze for 3rd
    "hover":         "#1C2128",   # Hover state
    "selected":      "#1F6FEB",   # Selected option
    "white":         "#FFFFFF",
}

FONTS = {
    "title":    ("Segoe UI", 22, "bold"),
    "subtitle": ("Segoe UI", 13),
    "heading":  ("Segoe UI", 14, "bold"),
    "body":     ("Segoe UI", 11),
    "small":    ("Segoe UI", 9),
    "btn":      ("Segoe UI", 11, "bold"),
    "question": ("Segoe UI", 13),
    "category": ("Segoe UI", 9, "bold"),
    "mono":     ("Consolas", 10),
}


# =============================================================================
class CareerGuidanceApp:
    """
    Main application class managing all GUI screens and state.
    Screens: Welcome → Questionnaire → Loading → Results
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_root()

        # Core engine instances
        self.engine = InferenceEngine()
        self.recommender = CareerRecommendationModule()

        # State
        self.current_question_index = 0
        self.selected_option = tk.StringVar()
        self.option_buttons = []

        # Build first screen
        self.show_welcome_screen()

    # =========================================================================
    # ROOT CONFIGURATION
    # =========================================================================
    def _configure_root(self):
        self.root.title("AI Career Guidance Expert System")
        self.root.geometry("900x650")
        self.root.minsize(800, 580)
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(True, True)

        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 450
        y = (self.root.winfo_screenheight() // 2) - 325
        self.root.geometry(f"900x650+{x}+{y}")

    # =========================================================================
    # UTILITY: CLEAR SCREEN
    # =========================================================================
    def _clear_screen(self):
        """Destroy all widgets on the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # =========================================================================
    # UTILITY: STYLED WIDGETS
    # =========================================================================
    def _make_frame(self, parent, bg=None, **kwargs):
        return tk.Frame(parent, bg=bg or COLORS["bg_dark"], **kwargs)

    def _make_label(self, parent, text, fg=None, font_key="body", bg=None, **kwargs):
        return tk.Label(
            parent,
            text=text,
            fg=fg or COLORS["text_primary"],
            font=FONTS[font_key],
            bg=bg or COLORS["bg_dark"],
            **kwargs
        )

    def _make_button(self, parent, text, command, bg=None, fg=None, font_key="btn", **kwargs):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg or COLORS["accent"],
            fg=fg or COLORS["white"],
            font=FONTS[font_key],
            relief="flat",
            cursor="hand2",
            activebackground=COLORS["hover"],
            activeforeground=COLORS["white"],
            padx=20,
            pady=10,
            **kwargs
        )
        return btn

    def _add_hover(self, widget, normal_bg, hover_bg):
        """Add hover color effect to a widget."""
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    # =========================================================================
    # SCREEN 1: WELCOME
    # =========================================================================
    def show_welcome_screen(self):
        """Display the welcome/intro screen."""
        self._clear_screen()
        self.engine.reset()
        self.current_question_index = 0

        # ---------- Header bar ----------
        header = self._make_frame(self.root, bg=COLORS["bg_card"])
        header.pack(fill="x")

        hinner = self._make_frame(header, bg=COLORS["bg_card"])
        hinner.pack(pady=12, padx=30, anchor="w")

        self._make_label(hinner, "🎓", fg=COLORS["accent"], font_key="title", bg=COLORS["bg_card"]).pack(side="left")
        self._make_label(
            hinner, "  AI Career Guidance Expert System",
            fg=COLORS["text_primary"], font_key="title", bg=COLORS["bg_card"]
        ).pack(side="left")

        # Divider
        tk.Frame(self.root, bg=COLORS["border"], height=1).pack(fill="x")

        # ---------- Main content ----------
        main = self._make_frame(self.root)
        main.pack(expand=True, fill="both", padx=60, pady=30)

        # Tagline
        self._make_label(
            main,
            "Discover Your Ideal Career Path with AI",
            fg=COLORS["accent"],
            font_key="heading"
        ).pack(pady=(20, 8))

        self._make_label(
            main,
            "Answer 18 questions about your interests, skills, favourite subjects,\n"
            "and personality — our expert system will recommend the best career for you.",
            fg=COLORS["text_secondary"],
            font_key="subtitle",
            justify="center"
        ).pack(pady=(0, 30))

        # ---------- Feature cards ----------
        cards_frame = self._make_frame(main)
        cards_frame.pack(pady=10)

        features = [
            ("🧠", "Expert System",   "Rule-based AI reasoning"),
            ("📋", "18 Questions",    "Interests, Skills & Personality"),
            ("🎯", "Top 3 Careers",   "Scored & explained recommendations"),
            ("📊", "Match Score",     "Percentage-based ranking"),
        ]

        for icon, title, desc in features:
            card = self._make_frame(cards_frame, bg=COLORS["bg_card"])
            card.pack(side="left", padx=8, pady=5, ipadx=14, ipady=12)

            tk.Frame(card, bg=COLORS["accent"], width=3).pack(side="left", fill="y")

            inner = self._make_frame(card, bg=COLORS["bg_card"])
            inner.pack(side="left", padx=12, pady=4)

            self._make_label(inner, f"{icon} {title}", fg=COLORS["text_primary"],
                             font_key="body", bg=COLORS["bg_card"]).pack(anchor="w")
            self._make_label(inner, desc, fg=COLORS["text_secondary"],
                             font_key="small", bg=COLORS["bg_card"]).pack(anchor="w")

        # ---------- Career pills ----------
        careers_frame = self._make_frame(main)
        careers_frame.pack(pady=20)

        self._make_label(
            careers_frame, "Careers Covered:",
            fg=COLORS["text_secondary"], font_key="small"
        ).pack(side="left", padx=(0, 8))

        careers = ["💻 Software Eng.", "🩺 Doctor", "📚 Teacher", "⚖️ Lawyer",
                   "🎨 Graphic Design", "📊 Accountant", "⚙️ Mech. Eng."]
        for c in careers:
            lbl = tk.Label(
                careers_frame, text=c,
                bg=COLORS["bg_input"], fg=COLORS["text_secondary"],
                font=FONTS["small"], padx=8, pady=3, relief="flat"
            )
            lbl.pack(side="left", padx=3)

        # ---------- Start button ----------
        btn_frame = self._make_frame(main)
        btn_frame.pack(pady=25)

        start_btn = self._make_button(
            btn_frame,
            "  ▶   Start Career Assessment  ",
            command=self.show_question_screen,
            bg=COLORS["accent"],
            font_key="btn"
        )
        start_btn.pack(ipady=4)
        self._add_hover(start_btn, COLORS["accent"], "#1A85FF")

        self._make_label(
            main, "Takes approximately 3–5 minutes",
            fg=COLORS["text_dim"], font_key="small"
        ).pack()

        # ---------- Footer ----------
        footer = self._make_frame(self.root, bg=COLORS["bg_card"])
        footer.pack(fill="x", side="bottom")
        self._make_label(
            footer,
            "Powered by Expert System  •  Rule-Based Reasoning  •  Inference Engine",
            fg=COLORS["text_dim"], font_key="small", bg=COLORS["bg_card"]
        ).pack(pady=8)

    # =========================================================================
    # SCREEN 2: QUESTIONNAIRE
    # =========================================================================
    def show_question_screen(self):
        """Display the current question in the questionnaire flow."""
        self._clear_screen()

        q = QUESTIONS[self.current_question_index]
        total = len(QUESTIONS)
        answered = self.current_question_index
        progress_pct = answered / total

        # ---------- Header bar ----------
        header = self._make_frame(self.root, bg=COLORS["bg_card"])
        header.pack(fill="x")

        header_inner = self._make_frame(header, bg=COLORS["bg_card"])
        header_inner.pack(fill="x", padx=24, pady=10)

        self._make_label(
            header_inner,
            "🎓 AI Career Guidance",
            fg=COLORS["accent"], font_key="heading", bg=COLORS["bg_card"]
        ).pack(side="left")

        self._make_label(
            header_inner,
            f"Question {self.current_question_index + 1} of {total}",
            fg=COLORS["text_secondary"], font_key="body", bg=COLORS["bg_card"]
        ).pack(side="right")

        # ---------- Progress bar ----------
        prog_outer = self._make_frame(self.root, bg=COLORS["border"])
        prog_outer.pack(fill="x")

        prog_fill = tk.Frame(
            prog_outer,
            bg=COLORS["accent"],
            height=4,
            width=int(self.root.winfo_width() * progress_pct)
        )
        prog_fill.pack(side="left")

        # Divider
        tk.Frame(self.root, bg=COLORS["border"], height=1).pack(fill="x")

        # ---------- Main content ----------
        main = self._make_frame(self.root)
        main.pack(expand=True, fill="both", padx=60, pady=15)

        # Category badge
        cat_frame = self._make_frame(main)
        cat_frame.pack(anchor="w", pady=(10, 0))

        cat_label = tk.Label(
            cat_frame,
            text=f"  {q['category'].upper()}  ",
            bg=COLORS["bg_input"],
            fg=COLORS["accent"],
            font=FONTS["category"],
            padx=6, pady=3
        )
        cat_label.pack(side="left")

        # Filled progress text
        self._make_label(
            cat_frame,
            f"  {int(progress_pct * 100)}% complete",
            fg=COLORS["text_dim"], font_key="small"
        ).pack(side="left", padx=10)

        # Question text
        self._make_label(
            main,
            q["text"],
            fg=COLORS["text_primary"],
            font_key="question",
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=(16, 20))

        # ---------- Option buttons ----------
        self.option_buttons = []
        self.selected_option.set("")

        options_frame = self._make_frame(main)
        options_frame.pack(fill="x", anchor="w")

        for opt in q["options"]:
            btn = tk.Button(
                options_frame,
                text=f"  {opt}",
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"],
                font=FONTS["body"],
                relief="flat",
                cursor="hand2",
                anchor="w",
                justify="left",
                padx=16,
                pady=12,
                activebackground=COLORS["selected"],
                activeforeground=COLORS["white"],
                command=lambda o=opt: self._select_option(o),
            )
            btn.pack(fill="x", pady=4, ipady=2)
            self.option_buttons.append((btn, opt))

            self._add_hover(btn, COLORS["bg_input"], COLORS["hover"])

        # ---------- Navigation ----------
        nav_frame = self._make_frame(main)
        nav_frame.pack(fill="x", pady=(20, 5))

        # Back button (only if not first question)
        if self.current_question_index > 0:
            back_btn = self._make_button(
                nav_frame, "← Back",
                command=self._go_back,
                bg=COLORS["bg_input"],
                fg=COLORS["text_secondary"]
            )
            back_btn.pack(side="left")
            self._add_hover(back_btn, COLORS["bg_input"], COLORS["border"])

        # Next / Finish button (disabled until option selected)
        is_last = self.current_question_index == total - 1
        btn_text = "  Finish & See Results  " if is_last else "  Next →  "

        self.next_btn = self._make_button(
            nav_frame,
            btn_text,
            command=self._go_next,
            bg=COLORS["accent"],
            state="disabled"
        )
        self.next_btn.pack(side="right")

        # ---------- Question counter dots ----------
        dots_frame = self._make_frame(main)
        dots_frame.pack(pady=(15, 0))
        for i in range(total):
            color = COLORS["accent"] if i < answered else (COLORS["accent2"] if i == answered else COLORS["border"])
            tk.Frame(dots_frame, bg=color, width=8 if i == answered else 6, height=8 if i == answered else 6).pack(
                side="left", padx=2
            )

        # ---------- Footer ----------
        footer = self._make_frame(self.root, bg=COLORS["bg_card"])
        footer.pack(fill="x", side="bottom")
        self._make_label(
            footer,
            "Select one option to continue  •  Your answers are analyzed by the AI Inference Engine",
            fg=COLORS["text_dim"], font_key="small", bg=COLORS["bg_card"]
        ).pack(pady=8)

        # Pre-fill if user is going back to a previously answered question
        q_id = q["id"]
        if q_id in self.engine.user_answers:
            self._select_option(self.engine.user_answers[q_id])

    # -------------------------------------------------------------------------
    def _select_option(self, option: str):
        """Highlight the selected option button and enable Next."""
        self.selected_option.set(option)
        for btn, opt in self.option_buttons:
            if opt == option:
                btn.config(bg=COLORS["selected"], fg=COLORS["white"])
            else:
                btn.config(bg=COLORS["bg_input"], fg=COLORS["text_primary"])
        self.next_btn.config(state="normal")

    # -------------------------------------------------------------------------
    def _go_next(self):
        """Save answer and move to next question or results."""
        answer = self.selected_option.get()
        if not answer:
            return

        q_id = QUESTIONS[self.current_question_index]["id"]
        self.engine.record_answer(q_id, answer)

        if self.current_question_index < len(QUESTIONS) - 1:
            self.current_question_index += 1
            self.show_question_screen()
        else:
            self.show_loading_screen()

    # -------------------------------------------------------------------------
    def _go_back(self):
        """Go to the previous question."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question_screen()

    # =========================================================================
    # SCREEN 3: LOADING / PROCESSING
    # =========================================================================
    def show_loading_screen(self):
        """Display a loading screen while the inference engine processes."""
        self._clear_screen()

        main = self._make_frame(self.root)
        main.pack(expand=True, fill="both")

        center = self._make_frame(main)
        center.place(relx=0.5, rely=0.5, anchor="center")

        self._make_label(center, "🧠", fg=COLORS["accent"], font_key="title").pack(pady=(0, 10))
        self._make_label(
            center, "Analyzing Your Profile...",
            fg=COLORS["text_primary"], font_key="heading"
        ).pack()
        self._make_label(
            center, "The Inference Engine is applying IF-THEN rules\nto match your profile with career knowledge base.",
            fg=COLORS["text_secondary"], font_key="body", justify="center"
        ).pack(pady=12)

        # Animated progress bar
        self.load_var = tk.DoubleVar(value=0)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "AI.Horizontal.TProgressbar",
            troughcolor=COLORS["bg_input"],
            background=COLORS["accent"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["accent"],
            darkcolor=COLORS["accent"],
        )
        pb = ttk.Progressbar(
            center, variable=self.load_var, maximum=100,
            length=300, mode="determinate",
            style="AI.Horizontal.TProgressbar"
        )
        pb.pack(pady=10)

        self.load_status = self._make_label(
            center, "Loading knowledge base...",
            fg=COLORS["text_dim"], font_key="small"
        )
        self.load_status.pack()

        steps = [
            (15, "Loading knowledge base..."),
            (35, "Evaluating interest patterns..."),
            (55, "Applying inference rules..."),
            (75, "Scoring career matches..."),
            (90, "Generating explanations..."),
            (100, "Done! Preparing results..."),
        ]

        def animate(i=0):
            if i < len(steps):
                val, msg = steps[i]
                self.load_var.set(val)
                self.load_status.config(text=msg)
                self.root.after(350, lambda: animate(i + 1))
            else:
                self.root.after(400, self.show_results_screen)

        animate()

    # =========================================================================
    # SCREEN 4: RESULTS
    # =========================================================================
    def show_results_screen(self):
        """Display the career recommendations results screen."""
        self._clear_screen()

        # Get recommendations
        raw_recs = self.engine.get_recommendations(top_n=3)
        recs = [CareerRecommendationModule.format_recommendation(r) for r in raw_recs]

        # ---------- Header ----------
        header = self._make_frame(self.root, bg=COLORS["bg_card"])
        header.pack(fill="x")

        hinner = self._make_frame(header, bg=COLORS["bg_card"])
        hinner.pack(fill="x", padx=24, pady=12)

        self._make_label(
            hinner, "🎯 Your Career Recommendations",
            fg=COLORS["text_primary"], font_key="heading", bg=COLORS["bg_card"]
        ).pack(side="left")

        restart_btn = self._make_button(
            hinner, "↺  Start Over",
            command=self.show_welcome_screen,
            bg=COLORS["bg_input"],
            fg=COLORS["text_secondary"]
        )
        restart_btn.pack(side="right")
        self._add_hover(restart_btn, COLORS["bg_input"], COLORS["border"])

        tk.Frame(self.root, bg=COLORS["border"], height=1).pack(fill="x")

        # ---------- Scrollable main area ----------
        canvas_frame = self._make_frame(self.root)
        canvas_frame.pack(expand=True, fill="both", padx=0, pady=0)

        canvas = tk.Canvas(canvas_frame, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = self._make_frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(event):
            canvas.itemconfig(1, width=event.width)

        canvas.bind("<Configure>", on_resize)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mousewheel scroll
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta / 120), "units"))

        # ---------- Intro text ----------
        intro_frame = self._make_frame(inner)
        intro_frame.pack(fill="x", padx=40, pady=(20, 5))

        if recs:
            top = recs[0]
            self._make_label(
                intro_frame,
                f"Based on your profile, your best career match is  {top['icon']} {top['career']}!",
                fg=COLORS["accent2"],
                font_key="heading"
            ).pack(anchor="w")
            self._make_label(
                intro_frame,
                f"The inference engine fired {len(self.engine.get_fired_rules())} rules "
                f"across {len(self.engine.user_answers)} answers to determine your results.",
                fg=COLORS["text_secondary"],
                font_key="small"
            ).pack(anchor="w", pady=(4, 0))

        # ---------- Recommendation cards ----------
        card_colors = {
            1: (COLORS["gold"],   "#1A1608"),
            2: (COLORS["silver"], "#131618"),
            3: (COLORS["bronze"], "#1A0F08"),
        }

        for rec in recs:
            rank = rec["rank"]
            accent_color, card_bg = card_colors.get(rank, (COLORS["accent"], COLORS["bg_card"]))

            card = tk.Frame(inner, bg=card_bg, relief="flat", bd=0)
            card.pack(fill="x", padx=40, pady=10, ipady=4)

            # Left accent bar
            tk.Frame(card, bg=accent_color, width=5).pack(side="left", fill="y")

            body = self._make_frame(card, bg=card_bg)
            body.pack(side="left", fill="both", expand=True, padx=18, pady=14)

            # --- Top row: rank + career name + match % ---
            top_row = self._make_frame(body, bg=card_bg)
            top_row.pack(fill="x")

            rank_lbl = tk.Label(
                top_row, text=rec["rank_label"],
                bg=accent_color, fg="#000000",
                font=FONTS["small"], padx=8, pady=3
            )
            rank_lbl.pack(side="left")

            self._make_label(
                top_row,
                f"  {rec['icon']}  {rec['career']}",
                fg=COLORS["text_primary"],
                font_key="heading",
                bg=card_bg
            ).pack(side="left")

            self._make_label(
                top_row,
                f"{rec['match_percentage']}% Match",
                fg=accent_color,
                font_key="heading",
                bg=card_bg
            ).pack(side="right")

            # --- Match bar ---
            bar_frame = self._make_frame(body, bg=card_bg)
            bar_frame.pack(fill="x", pady=(6, 2))

            bar_outer = tk.Frame(bar_frame, bg=COLORS["bg_input"], height=8)
            bar_outer.pack(fill="x")
            bar_outer.update_idletasks()

            fill_pct = rec["match_percentage"] / 100
            bar_inner = tk.Frame(bar_outer, bg=accent_color, height=8)
            bar_inner.place(relwidth=fill_pct, relheight=1)

            # --- Description ---
            self._make_label(
                body, rec["description"],
                fg=COLORS["text_secondary"],
                font_key="body",
                bg=card_bg,
                wraplength=720,
                justify="left"
            ).pack(anchor="w", pady=(10, 6))

            # --- Details row ---
            details_frame = self._make_frame(body, bg=card_bg)
            details_frame.pack(fill="x", pady=4)

            detail_items = [
                ("🎓", "Education", rec["education"]),
                ("💰", "Salary",    rec["salary_range"]),
                ("📈", "Growth",    rec["growth"]),
            ]

            for icon, label, value in detail_items:
                di = self._make_frame(details_frame, bg=COLORS["bg_input"])
                di.pack(side="left", padx=(0, 8), pady=2, ipadx=10, ipady=6)

                self._make_label(
                    di, f"{icon} {label}", fg=COLORS["text_dim"],
                    font_key="small", bg=COLORS["bg_input"]
                ).pack(anchor="w")
                self._make_label(
                    di, value, fg=COLORS["text_primary"],
                    font_key="small", bg=COLORS["bg_input"]
                ).pack(anchor="w")

            # --- Why this career ---
            self._make_label(
                body, "🔍 Why this career?",
                fg=accent_color, font_key="body", bg=card_bg
            ).pack(anchor="w", pady=(10, 2))

            for exp in rec["all_explanations"]:
                self._make_label(
                    body, f"  → {exp}",
                    fg=COLORS["text_secondary"],
                    font_key="small",
                    bg=card_bg,
                    wraplength=720,
                    justify="left"
                ).pack(anchor="w", pady=1)

            # Separator
            tk.Frame(inner, bg=COLORS["border"], height=1).pack(fill="x", padx=40)

        # ---------- Score overview ----------
        scores_frame = self._make_frame(inner)
        scores_frame.pack(fill="x", padx=40, pady=20)

        self._make_label(
            scores_frame, "📊 All Career Scores",
            fg=COLORS["text_primary"], font_key="heading"
        ).pack(anchor="w", pady=(0, 10))

        all_scores = self.engine.get_all_scores()
        max_score = max(all_scores.values()) if all_scores else 1

        icons = CareerRecommendationModule.CAREER_ICONS
        for career, score in all_scores.items():
            row = self._make_frame(scores_frame)
            row.pack(fill="x", pady=2)

            self._make_label(
                row, f"{icons.get(career,'')} {career}",
                fg=COLORS["text_secondary"], font_key="body"
            ).pack(side="left", width=220, anchor="w")

            bar_outer = tk.Frame(row, bg=COLORS["bg_input"], height=14, width=300)
            bar_outer.pack(side="left", padx=10)
            bar_outer.pack_propagate(False)

            fill_w = int((score / max(max_score, 1)) * 300)
            tk.Frame(bar_outer, bg=COLORS["accent"], height=14, width=fill_w).pack(side="left")

            self._make_label(
                row, f"  {score} pts",
                fg=COLORS["text_dim"], font_key="small"
            ).pack(side="left")

        # Bottom padding
        self._make_frame(inner).pack(pady=30)

        # ---------- Footer ----------
        footer = self._make_frame(self.root, bg=COLORS["bg_card"])
        footer.pack(fill="x", side="bottom")
        self._make_label(
            footer,
            "AI Career Guidance Expert System  •  Rule-Based Reasoning  •  Knowledge Base  •  Inference Engine",
            fg=COLORS["text_dim"], font_key="small", bg=COLORS["bg_card"]
        ).pack(pady=8)
