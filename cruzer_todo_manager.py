import json
import os
from datetime import datetime

import customtkinter as ctk
from tkinter import messagebox


class CruzerTodoManager(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Cruzer To-Do Manager")
        self.geometry("1020x720")
        self.minsize(900, 620)

        self.storage_file = "tasks.json"
        self.tasks = []
        self.filtered_tasks = []
        self.drag_source_id = None
        self.current_theme = "light"

        self.palette = {
            "light": {
                "bg_top": "#f5f8ff",
                "bg_bottom": "#edf3ff",
                "card": "#ffffff",
                "fg": "#1e293b",
                "sub_fg": "#64748b",
                "border": "#dbe3f3",
                "hover": "#f4f7fd",
                "primary": "#4f46e5",
                "primary_hover": "#4338ca",
                "success": "#16a34a",
                "warning": "#f59e0b",
                "danger": "#ef4444",
            },
            "dark": {
                "bg_top": "#0b1220",
                "bg_bottom": "#111827",
                "card": "#1f2937",
                "fg": "#e5e7eb",
                "sub_fg": "#9ca3af",
                "border": "#334155",
                "hover": "#273449",
                "primary": "#6366f1",
                "primary_hover": "#4f46e5",
                "success": "#22c55e",
                "warning": "#f59e0b",
                "danger": "#f43f5e",
            },
        }

        # General appearance.
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Tkinter variables.
        self.task_var = ctk.StringVar()
        self.priority_var = ctk.StringVar(value="Medium")
        self.due_var = ctk.StringVar()
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="All")
        self.task_placeholder = "Enter your task (e.g., Complete assignment)"

        self._build_ui()
        self._bind_shortcuts()
        self.load_tasks()
        self.refresh_tasks()
        self._apply_palette()

    def _build_ui(self):
        self.bg_top = ctk.CTkFrame(self, corner_radius=0)
        self.bg_top.pack(fill="both", expand=True)

        self.content = ctk.CTkFrame(self.bg_top, corner_radius=18)
        self.content.pack(fill="both", expand=True, padx=18, pady=18)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(3, weight=1)

        self.header = ctk.CTkFrame(self.content, corner_radius=14)
        self.header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="🚀  Cruzer To-Do Manager",
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, pady=(12, 4))

        self.tagline_label = ctk.CTkLabel(
            self.header,
            text="Organize life, the Cruzer way",
            font=ctk.CTkFont(family="Segoe UI", size=14),
        )
        self.tagline_label.grid(row=1, column=0, pady=(0, 12))

        # Theme switch.
        self.theme_switch = ctk.CTkSwitch(
            self.header,
            text="Dark Mode",
            command=self.toggle_theme,
            progress_color="#6366f1",
        )
        self.theme_switch.grid(row=0, column=1, rowspan=2, padx=12, pady=12, sticky="e")

        # Input card.
        self.input_card = ctk.CTkFrame(self.content, corner_radius=12, border_width=1)
        self.input_card.grid(row=1, column=0, sticky="ew", padx=16, pady=8)
        self.input_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.input_card,
            text="📝 Add New Task",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=14, pady=(12, 8))

        self.task_input_label = ctk.CTkLabel(
            self.input_card,
            text="Task",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.task_input_label.grid(row=1, column=0, sticky="w", padx=(14, 8), pady=(0, 4))

        self.priority_input_label = ctk.CTkLabel(
            self.input_card,
            text="Priority",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.priority_input_label.grid(row=1, column=1, sticky="w", padx=8, pady=(0, 4))

        self.due_input_label = ctk.CTkLabel(
            self.input_card,
            text="Due Date",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.due_input_label.grid(row=1, column=2, sticky="w", padx=8, pady=(0, 4))

        self.task_entry = ctk.CTkEntry(
            self.input_card,
            textvariable=self.task_var,
            placeholder_text=self.task_placeholder,
            height=38,
            corner_radius=10,
        )
        self.task_entry.grid(row=2, column=0, sticky="ew", padx=(14, 8), pady=(0, 4))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        self.task_entry.bind("<FocusIn>", self._handle_task_focus_in)
        self.task_entry.bind("<FocusOut>", self._handle_task_focus_out)
        self.task_entry.bind("<FocusIn>", lambda e: self._highlight_active_input("task"), add="+")
        self.task_entry.bind("<FocusOut>", lambda e: self._highlight_active_input(None), add="+")

        self.priority_menu = ctk.CTkOptionMenu(
            self.input_card,
            values=["Select priority (Low / Medium / High)", "Low", "Medium", "High"],
            variable=self.priority_var,
            width=130,
            height=38,
            corner_radius=10,
        )
        self.priority_var.set("Select priority (Low / Medium / High)")
        self.priority_menu.grid(row=2, column=1, padx=8, pady=(0, 4))

        self.due_entry = ctk.CTkEntry(
            self.input_card,
            textvariable=self.due_var,
            placeholder_text="Select due date",
            width=150,
            height=38,
            corner_radius=10,
        )
        self.due_entry.grid(row=2, column=2, padx=8, pady=(0, 4))
        self.due_entry.bind("<FocusIn>", lambda e: self._highlight_active_input("due"))
        self.due_entry.bind("<FocusOut>", lambda e: self._highlight_active_input(None))

        self.add_btn = ctk.CTkButton(
            self.input_card,
            text="Add Task",
            command=self.add_task,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        )
        self.add_btn.grid(row=2, column=3, padx=(8, 14), pady=(0, 4))

        self.helper_task = ctk.CTkLabel(
            self.input_card,
            text="Keep your task short and clear.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        )
        self.helper_task.grid(row=3, column=0, sticky="w", padx=(14, 8), pady=(0, 10))

        self.helper_priority = ctk.CTkLabel(
            self.input_card,
            text="Choose priority based on urgency.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        )
        self.helper_priority.grid(row=3, column=1, sticky="w", padx=8, pady=(0, 10))

        self.validation_label = ctk.CTkLabel(
            self.input_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        )
        self.validation_label.grid(row=3, column=2, columnspan=2, sticky="e", padx=(8, 14), pady=(0, 10))

        # Search/filter row.
        self.filter_card = ctk.CTkFrame(self.content, corner_radius=12, border_width=1)
        self.filter_card.grid(row=2, column=0, sticky="ew", padx=16, pady=8)

        self.search_label = ctk.CTkLabel(
            self.filter_card,
            text="Search",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.search_label.pack(side="left", padx=(12, 4), pady=10)

        self.search_entry = ctk.CTkEntry(
            self.filter_card,
            textvariable=self.search_var,
            placeholder_text="Search tasks...",
            height=34,
            corner_radius=10,
            width=320,
        )
        self.search_entry.pack(side="left", padx=12, pady=10)
        self.search_var.trace_add("write", lambda *_: self.refresh_tasks())
        self.search_entry.bind("<FocusIn>", lambda e: self._highlight_active_input("search"))
        self.search_entry.bind("<FocusOut>", lambda e: self._highlight_active_input(None))

        self.filter_label = ctk.CTkLabel(
            self.filter_card,
            text="Filter",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        )
        self.filter_label.pack(side="left", padx=(2, 4), pady=10)

        self.filter_menu = ctk.CTkOptionMenu(
            self.filter_card,
            values=["All", "Pending", "Completed", "High Priority"],
            variable=self.filter_var,
            command=lambda _: self.refresh_tasks(),
            width=150,
            height=34,
            corner_radius=10,
        )
        self.filter_menu.pack(side="left", padx=8, pady=10)

        # Task list area.
        self.list_card = ctk.CTkFrame(self.content, corner_radius=12, border_width=1)
        self.list_card.grid(row=3, column=0, sticky="nsew", padx=16, pady=8)
        self.list_card.grid_rowconfigure(1, weight=1)
        self.list_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.list_card,
            text="📋 Tasks",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 4))

        self.tasks_scroll = ctk.CTkScrollableFrame(self.list_card, corner_radius=10)
        self.tasks_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(2, 10))
        self.tasks_scroll.grid_columnconfigure(0, weight=1)

        self.empty_label = ctk.CTkLabel(
            self.tasks_scroll,
            text="No tasks yet 🚀 Start by adding one!",
            justify="center",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        )

        # Bottom action bar (moved to end of page).
        self.actions_footer = ctk.CTkFrame(self.content, corner_radius=12, border_width=1)
        self.actions_footer.grid(row=4, column=0, sticky="ew", padx=16, pady=(8, 4))

        self.complete_btn = ctk.CTkButton(
            self.actions_footer,
            text="✔ Complete",
            command=self.toggle_complete_selected,
            width=120,
            corner_radius=10,
        )
        self.complete_btn.pack(side="right", padx=(6, 10), pady=10)

        self.delete_btn = ctk.CTkButton(
            self.actions_footer,
            text="🗑 Delete",
            command=self.delete_selected,
            width=95,
            corner_radius=10,
        )
        self.delete_btn.pack(side="right", padx=6, pady=10)

        self.edit_btn = ctk.CTkButton(
            self.actions_footer,
            text="✏ Edit",
            command=self.edit_selected,
            width=80,
            corner_radius=10,
        )
        self.edit_btn.pack(side="right", padx=6, pady=10)

        self.search_hint = ctk.CTkLabel(
            self.filter_card,
            text="Tip: Search by keywords and combine with filter for quick results.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        )
        self.search_hint.pack(side="bottom", anchor="w", padx=12, pady=(0, 8))

        # Footer stats.
        self.footer = ctk.CTkFrame(self.content, corner_radius=12, border_width=1)
        self.footer.grid(row=5, column=0, sticky="ew", padx=16, pady=(4, 16))
        self.stats_label = ctk.CTkLabel(
            self.footer,
            text="🧾 Total: 0   ✅ Completed: 0   ⏳ Pending: 0",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self.stats_label.pack(padx=12, pady=10, anchor="w")

    # ----------------------------- Theme Styling ------------------------------
    def _apply_palette(self):
        p = self.palette[self.current_theme]
        self.configure(fg_color=p["bg_top"])
        self.bg_top.configure(fg_color=p["bg_bottom"])
        self.content.configure(fg_color=p["bg_top"])

        for card in [self.header, self.input_card, self.filter_card, self.list_card, self.actions_footer, self.footer]:
            card.configure(fg_color=p["card"], border_color=p["border"])

        self.title_label.configure(text_color=p["fg"])
        self.tagline_label.configure(text_color=p["sub_fg"])
        self.stats_label.configure(text_color=p["sub_fg"])
        self.task_input_label.configure(text_color=p["fg"])
        self.priority_input_label.configure(text_color=p["fg"])
        self.due_input_label.configure(text_color=p["fg"])
        self.search_label.configure(text_color=p["fg"])
        self.filter_label.configure(text_color=p["fg"])
        self.helper_task.configure(text_color=p["sub_fg"])
        self.helper_priority.configure(text_color=p["sub_fg"])
        self.search_hint.configure(text_color=p["sub_fg"])
        self.validation_label.configure(text_color=p["danger"])
        if hasattr(self, "empty_label") and self.empty_label.winfo_exists():
            self.empty_label.configure(text_color=p["sub_fg"])

        self.add_btn.configure(fg_color=p["primary"], hover_color=p["primary_hover"], text_color="#ffffff")
        self.complete_btn.configure(fg_color=p["success"], hover_color="#15803d", text_color="#ffffff")
        self.edit_btn.configure(fg_color=p["warning"], hover_color="#d97706", text_color="#111827")
        self.delete_btn.configure(fg_color=p["danger"], hover_color="#dc2626", text_color="#ffffff")

        self.task_entry.configure(fg_color=p["bg_top"], border_color=p["border"], text_color=p["fg"])
        self.due_entry.configure(fg_color=p["bg_top"], border_color=p["border"], text_color=p["fg"])
        self.search_entry.configure(fg_color=p["bg_top"], border_color=p["border"], text_color=p["fg"])
        self.tasks_scroll.configure(fg_color=p["bg_top"])

    def _highlight_active_input(self, field_name):
        """Highlight active input field for better focus visibility."""
        p = self.palette[self.current_theme]
        default_border = p["border"]
        active_border = p["primary"]

        self.task_entry.configure(border_color=active_border if field_name == "task" else default_border)
        self.due_entry.configure(border_color=active_border if field_name == "due" else default_border)
        self.search_entry.configure(border_color=active_border if field_name == "search" else default_border)

    def toggle_theme(self):
        self.current_theme = "dark" if self.theme_switch.get() == 1 else "light"
        ctk.set_appearance_mode(self.current_theme)
        self._apply_palette()
        self.refresh_tasks()

    # ----------------------------- Data Handling ------------------------------
    def load_tasks(self):
        if not os.path.exists(self.storage_file):
            self.tasks = []
            return
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.tasks = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "id" in item and "text" in item:
                        self.tasks.append(
                            {
                                "id": str(item.get("id")),
                                "text": str(item.get("text", "")),
                                "completed": bool(item.get("completed", False)),
                                "priority": str(item.get("priority", "Medium")),
                                "due_date": str(item.get("due_date", "")),
                                "created_at": str(item.get("created_at", "")),
                            }
                        )
                    elif isinstance(item, dict) and "text" in item:
                        self.tasks.append(
                            {
                                "id": str(datetime.now().timestamp()),
                                "text": str(item.get("text", "")),
                                "completed": bool(item.get("completed", False)),
                                "priority": "Medium",
                                "due_date": "",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            }
                        )
        except (OSError, json.JSONDecodeError) as err:
            self.tasks = []
            messagebox.showerror("Load Error", f"Could not load tasks.\n{err}")

    def save_tasks(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except OSError as err:
            messagebox.showerror("Save Error", f"Could not save tasks.\n{err}")

    # ----------------------------- Task Actions -------------------------------
    def _handle_task_focus_in(self, _event):
        """Clear placeholder when user starts typing."""
        if self.task_var.get() == self.task_placeholder:
            self.task_var.set("")

    def _handle_task_focus_out(self, _event):
        """Restore placeholder if input is empty."""
        if not self.task_var.get().strip():
            self.task_var.set("")

    def add_task(self):
        self.validation_label.configure(text="")
        text = self.task_var.get().strip()
        if not text:
            self.validation_label.configure(text="Task cannot be empty.")
            self.task_entry.focus_set()
            return

        due = self.due_var.get().strip()
        if due and not self._valid_date(due):
            messagebox.showwarning("Date Error", "Date must be YYYY-MM-DD.")
            return

        self.tasks.append(
            {
                "id": str(datetime.now().timestamp()),
                "text": text,
                "completed": False,
                "priority": (
                    "Medium"
                    if self.priority_var.get() == "Select priority (Low / Medium / High)"
                    else self.priority_var.get()
                ),
                "due_date": due,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        self.task_var.set("")
        self.due_var.set("")
        self.save_tasks()
        self.refresh_tasks(animate=True)

    def edit_selected(self):
        task = self._selected_task()
        if not task:
            messagebox.showinfo("Selection Required", "Select a task card first.")
            return
        self.task_var.set(task["text"])
        self.priority_var.set(task.get("priority", "Medium"))
        self.due_var.set(task.get("due_date", ""))
        self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
        self.save_tasks()
        self.refresh_tasks()
        self.task_entry.focus_set()

    def delete_selected(self):
        task = self._selected_task()
        if not task:
            messagebox.showinfo("Selection Required", "Select a task card first.")
            return
        self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
        self.save_tasks()
        self.refresh_tasks(animate=True)

    def toggle_complete_selected(self):
        task = self._selected_task()
        if not task:
            messagebox.showinfo("Selection Required", "Select a task card first.")
            return
        for item in self.tasks:
            if item["id"] == task["id"]:
                item["completed"] = not item["completed"]
                break
        self.save_tasks()
        self.refresh_tasks()

    def clear_all_tasks(self):
        if not self.tasks:
            messagebox.showinfo("Nothing to Clear", "Task list is already empty.")
            return
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.refresh_tasks()

    def _valid_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ------------------------- Card List / Rendering --------------------------
    def _ensure_empty_label(self):
        """Create empty-state label if it does not exist or was destroyed."""
        if hasattr(self, "empty_label") and self.empty_label.winfo_exists():
            return

        self.empty_label = ctk.CTkLabel(
            self.tasks_scroll,
            text="No tasks yet 🚀 Start by adding one!",
            justify="center",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        )
        self.empty_label.configure(text_color=self.palette[self.current_theme]["sub_fg"])

    def refresh_tasks(self, animate=False):
        self._ensure_empty_label()

        for child in self.tasks_scroll.winfo_children():
            if child is not self.empty_label:
                child.destroy()

        query = self.search_var.get().strip().lower()
        filter_mode = self.filter_var.get()
        self.filtered_tasks = []

        for task in self.tasks:
            if query and query not in task["text"].lower():
                continue
            if filter_mode == "Pending" and task.get("completed"):
                continue
            if filter_mode == "Completed" and not task.get("completed"):
                continue
            if filter_mode == "High Priority" and task.get("priority") != "High":
                continue
            self.filtered_tasks.append(task)

        if not self.filtered_tasks:
            if self.empty_label.winfo_exists():
                self.empty_label.grid(row=0, column=0, pady=24)
        else:
            if self.empty_label.winfo_exists():
                self.empty_label.grid_forget()
            for i, task in enumerate(self.filtered_tasks):
                self._create_task_card(i, task, animate=animate)

        done = sum(1 for t in self.tasks if t.get("completed"))
        pending = len(self.tasks) - done
        self.stats_label.configure(text=f"🧾 Total: {len(self.tasks)}   ✅ Completed: {done}   ⏳ Pending: {pending}")

    def _create_task_card(self, row, task, animate=False):
        p = self.palette[self.current_theme]
        priority = task.get("priority", "Medium")

        priority_colors = {
            "Low": ("#22c55e", "#14532d"),
            "Medium": ("#f59e0b", "#78350f"),
            "High": ("#ef4444", "#7f1d1d"),
        }
        badge_bg, badge_text = priority_colors.get(priority, ("#64748b", "#0f172a"))

        card = ctk.CTkFrame(self.tasks_scroll, corner_radius=10, border_width=1, border_color=p["border"], fg_color=p["card"])
        card.grid(row=row, column=0, sticky="ew", padx=4, pady=6)
        card.grid_columnconfigure(1, weight=1)

        # Selection handling.
        card.task_id = task["id"]
        card.selected = False
        card.bind("<Button-1>", lambda e, c=card: self._select_card(c))
        card.bind("<Enter>", lambda e, c=card: c.configure(fg_color=p["hover"] if not c.selected else p["primary"]))
        card.bind("<Leave>", lambda e, c=card: c.configure(fg_color=p["card"] if not c.selected else p["primary"]))

        # Optional tiny visual animation.
        if animate:
            card.configure(border_width=0)
            self.after(60, lambda: card.configure(border_width=1) if card.winfo_exists() else None)

        check_var = ctk.BooleanVar(value=task.get("completed", False))
        check = ctk.CTkCheckBox(
            card,
            text="",
            variable=check_var,
            width=24,
            command=lambda t=task: self._toggle_by_id(t["id"]),
        )
        check.grid(row=0, column=0, padx=(10, 8), pady=10)

        text_color = "#94a3b8" if task.get("completed") else p["fg"]
        title_text = f"✓ {task['text']}" if task.get("completed") else task["text"]
        title = ctk.CTkLabel(
            card,
            text=title_text,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=text_color,
            anchor="w",
        )
        title.grid(row=0, column=1, sticky="w", padx=4)

        due_date = task.get("due_date", "")
        due_text = f"📅 {due_date}" if due_date else "📅 No due date"
        due = ctk.CTkLabel(
            card,
            text=due_text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=p["sub_fg"],
        )
        due.grid(row=1, column=1, sticky="w", padx=4, pady=(0, 10))

        badge = ctk.CTkLabel(
            card,
            text=priority,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            corner_radius=8,
            fg_color=badge_bg,
            text_color=badge_text,
            width=86,
            height=26,
        )
        badge.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

        # Drag-drop reorder handlers.
        card.bind("<ButtonPress-1>", lambda e, task_id=task["id"]: self._drag_start(task_id))
        card.bind("<ButtonRelease-1>", lambda e, task_id=task["id"]: self._drag_drop(task_id))

    def _toggle_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task.get("completed", False)
                break
        self.save_tasks()
        self.refresh_tasks()

    def _selected_task(self):
        for child in self.tasks_scroll.winfo_children():
            if getattr(child, "selected", False):
                for task in self.tasks:
                    if task["id"] == child.task_id:
                        return task
        return None

    def _select_card(self, selected_card):
        p = self.palette[self.current_theme]
        for child in self.tasks_scroll.winfo_children():
            child.selected = False
            child.configure(fg_color=p["card"])
        selected_card.selected = True
        selected_card.configure(fg_color=p["primary"])

    # ----------------------------- Drag and Drop ------------------------------
    def _drag_start(self, task_id):
        self.drag_source_id = task_id

    def _drag_drop(self, target_id):
        if not self.drag_source_id or self.drag_source_id == target_id:
            self.drag_source_id = None
            return
        source_idx = next((i for i, t in enumerate(self.tasks) if t["id"] == self.drag_source_id), None)
        target_idx = next((i for i, t in enumerate(self.tasks) if t["id"] == target_id), None)
        if source_idx is None or target_idx is None:
            self.drag_source_id = None
            return
        task = self.tasks.pop(source_idx)
        self.tasks.insert(target_idx, task)
        self.drag_source_id = None
        self.save_tasks()
        self.refresh_tasks()

    # ------------------------------- Shortcuts --------------------------------
    def _bind_shortcuts(self):
        self.bind("<Control-Return>", lambda e: self.add_task())
        self.bind("<Delete>", lambda e: self.delete_selected())
        self.bind("<Control-d>", lambda e: self.toggle_complete_selected())
        self.bind("<Control-f>", lambda e: self._focus_search())
        self.bind("<Control-l>", lambda e: self.clear_all_tasks())

    def _focus_search(self):
        self.search_entry.focus_set()
        return "break"


if __name__ == "__main__":
    app = CruzerTodoManager()
    app.mainloop()
