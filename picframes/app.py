from __future__ import annotations

import os
import threading
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
from tkinterdnd2 import COPY, DND_FILES, TkinterDnD

from .processor import build_jobs, SUPPORTED_EXTENSIONS
from .runner import run_jobs
from .option_builder import build_options, default_output_dir, resolve_sources
from .resources import asset_path
from . import settings as app_settings
from . import theme
from .license import LicenseInfo, validate_key, FREE_BATCH_LIMIT
from .license.activation_dialog import ActivationDialog
from .ui import BannerFrame, HeroSection, OutputCard, PreviewStrip, ProgressCard, SettingsCard, SourceCard

APP_TITLE = "PicFrames"


class PicFramesApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self) -> None:
        super().__init__()
        self._settings = app_settings.load()
        ctk.set_appearance_mode(self._settings.get("appearance_mode", "system"))
        ctk.set_default_color_theme("blue")
        self.title(APP_TITLE)
        self.geometry("940x700")
        self.minsize(860, 640)
        self.configure(fg_color=theme.BG)
        TkinterDnD._require(self)
        icon = asset_path("app_icon.ico")
        if icon.exists():
            self.iconbitmap(default=str(icon))
        self.mode_var = ctk.StringVar(value="files")
        self.selected_files: list[Path] = []
        self.selected_folder: Path | None = None
        self.output_dir: Path | None = None
        self.is_running = False
        self._cancel_event: threading.Event | None = None
        self._license_info: LicenseInfo | None = None
        self._build_ui()
        self._init_drag_and_drop()
        self._sync_view()
        if os.environ.get("PICFRAMES_DEV_PRO") == "1":
            dev_license = LicenseInfo(email="dev@test.local", tier="pro", issued_at="2026-01-01", expires_at=None)
            self._apply_license(dev_license)
        else:
            key = self._settings.get("license_key", "")
            self._apply_license(validate_key(key) if key else None)
        self.after(0, lambda: self.state("zoomed"))

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._banner = BannerFrame(
            self,
            on_toggle_appearance=self._toggle_appearance,
            on_open_activation=self._open_activation_dialog,
            appearance_mode=self._settings.get("appearance_mode", "system"),
        )
        self._banner.grid(row=0, column=0, sticky="ew")

        body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=28, pady=28)
        body.grid_columnconfigure(0, weight=1)

        self._hero = HeroSection(body, self._run_job)
        self._hero.grid(row=0, column=0, sticky="ew")

        controls = ctk.CTkFrame(body, fg_color="transparent")
        controls.grid(row=1, column=0, sticky="ew", pady=(22, 0))
        controls.grid_columnconfigure((0, 1), weight=1, uniform="cards")

        self._source_card = SourceCard(
            controls, self.mode_var, lambda _: self._sync_view(), self._choose_source
        )
        self._source_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self._settings_card = SettingsCard(controls)
        self._settings_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self._preview_strip = PreviewStrip(controls)
        self._preview_strip.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(14, 0))

        footer = ctk.CTkFrame(body, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", pady=(22, 0))
        footer.grid_columnconfigure((0, 1), weight=1, uniform="footer")

        self._output_card = OutputCard(footer, self._choose_output, self._open_output_folder)
        self._output_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self._progress_card = ProgressCard(footer, self._run_job)
        self._progress_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    def _init_drag_and_drop(self) -> None:
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self._on_drop)

    def _on_drop(self, event):
        dropped = [Path(p) for p in self.tk.splitlist(event.data) if p]
        files = [p for p in dropped if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
        folders = [p for p in dropped if p.is_dir()]
        pc = self._progress_card
        if files:
            self.mode_var.set("files")
            self.selected_files, self.selected_folder = files, None
            pc.status_label.configure(text=f"Loaded {len(files)} dropped image(s).")
        elif len(folders) == 1:
            self.mode_var.set("folder")
            self.selected_folder, self.selected_files = folders[0], []
            pc.status_label.configure(text=f"Loaded dropped folder: {folders[0]}")
        else:
            messagebox.showinfo(APP_TITLE, "Drop supported image files or a single folder.")
        self._sync_view()
        return COPY

    def _toggle_appearance(self) -> None:
        mode = "dark" if ctk.get_appearance_mode() == "Light" else "light"
        ctk.set_appearance_mode(mode)
        self._settings["appearance_mode"] = mode
        app_settings.save(self._settings)

    def _apply_license(self, info: LicenseInfo | None) -> None:
        self._license_info = info
        self._banner.update_license(info)
        self._settings_card.apply_license_state(info is not None and info.is_pro)

    def _open_activation_dialog(self) -> None:
        ActivationDialog(
            self,
            on_activated=self._on_key_activated,
            current_key=self._settings.get("license_key", ""),
        )

    def _on_key_activated(self, key: str, info: LicenseInfo) -> None:
        self._settings["license_key"] = key
        app_settings.save(self._settings)
        self._apply_license(info)
        messagebox.showinfo(APP_TITLE, f"Pro license activated!\nLicensed to: {info.email}")

    def _choose_source(self) -> None:
        self.selected_files, self.selected_folder = self._source_card.pick(self.mode_var.get())
        self._sync_view()

    def _choose_output(self) -> None:
        self.output_dir = self._output_card.pick() or self.output_dir
        self._sync_view()

    def _open_output_folder(self) -> None:
        mode = self.mode_var.get()
        target = self.output_dir or default_output_dir(mode, self.selected_files, self.selected_folder)
        if target is None:
            messagebox.showinfo(APP_TITLE, "Choose a source first so the output folder can be determined.")
            return
        target.mkdir(parents=True, exist_ok=True)
        os.startfile(target)

    def _sync_view(self) -> None:
        mode = self.mode_var.get()
        self._source_card.sync(mode, self.selected_files, self.selected_folder)
        self._output_card.sync(
            self.output_dir,
            default_output_dir(mode, self.selected_files, self.selected_folder),
        )
        self._preview_strip.update(self._preview_paths(mode))

    def _preview_paths(self, mode: str) -> list[Path]:
        if mode == "files":
            return self.selected_files
        if self.selected_folder and self.selected_folder.is_dir():
            return [
                p for p in sorted(self.selected_folder.iterdir())
                if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
        return []

    def _run_job(self) -> None:
        if self.is_running:
            return
        try:
            options = build_options(self._settings_card)
        except ValueError as exc:
            messagebox.showerror(APP_TITLE, str(exc))
            return
        mode = self.mode_var.get()
        recursive = bool(self._settings_card.recursive_checkbox.get())
        sources, source_root = resolve_sources(mode, self.selected_files, self.selected_folder, recursive)
        if not sources:
            messagebox.showinfo(APP_TITLE, "Select at least one image or a folder containing images.")
            return
        is_pro = self._license_info is not None and self._license_info.is_pro
        if not is_pro and len(sources) > FREE_BATCH_LIMIT:
            sources = sources[:FREE_BATCH_LIMIT]
            messagebox.showwarning(
                APP_TITLE,
                f"Free tier is limited to {FREE_BATCH_LIMIT} images per batch.\n"
                "Upgrade to Pro for unlimited batch processing.\n\n"
                f"Processing the first {FREE_BATCH_LIMIT} images only.",
            )
        out = self.output_dir or default_output_dir(mode, self.selected_files, self.selected_folder)
        if out is None:
            messagebox.showerror(APP_TITLE, "Unable to determine an output folder.")
            return
        jobs = build_jobs(sources, out, options, source_root=source_root)
        if not jobs:
            messagebox.showinfo(APP_TITLE, "No supported image files were found.")
            return
        self.is_running = True
        self._cancel_event = threading.Event()
        self._hero.set_running(True, on_cancel=self._cancel_job)
        self._progress_card.begin(len(jobs))
        run_jobs(
            jobs, options, out, self.after,
            lambda i, t, r: self._progress_card.update_progress(i, t),
            self._finish_job,
            cancel_event=self._cancel_event,
        )

    def _cancel_job(self) -> None:
        if self._cancel_event:
            self._cancel_event.set()

    def _finish_job(self, results, output_dir: Path) -> None:
        cancelled = bool(self._cancel_event and self._cancel_event.is_set())
        self.is_running = False
        self._cancel_event = None
        self._hero.set_running(False)
        processed, failed = self._progress_card.show_finish(results, cancelled=cancelled)
        self.output_dir = output_dir
        self._sync_view()
        if failed == 0:
            messagebox.showinfo(APP_TITLE, f"Done! {processed} image(s) saved to:\n{output_dir}")
        else:
            messagebox.showwarning(APP_TITLE, f"Finished with {failed} failure(s).")


def main() -> None:
    app = PicFramesApp()
    app.mainloop()
