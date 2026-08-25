from __future__ import annotations

import threading
import wave
from functools import lru_cache
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from predict import load_pipeline, predict_app_output_from_wav


APP_TITLE = "Parkinson's Voice Screening Demo"
ARTIFACT_DIR = Path(__file__).resolve().parent
DATASET_XLSX = ARTIFACT_DIR / "dataset" / "Demographics_age_sex.xlsx"

BG_COLOR = "#f5efe6"
HERO_COLOR = "#143642"
CARD_COLOR = "#fffdf9"
TEXT_COLOR = "#18313f"
MUTED_COLOR = "#6c7a80"
ACCENT_COLOR = "#f28f3b"
SUCCESS_COLOR = "#2a9d8f"
WARN_COLOR = "#e76f51"


@lru_cache(maxsize=1)
def load_dataset_metadata() -> dict[str, dict[str, str | float]]:
    if not DATASET_XLSX.exists():
        return {}

    try:
        import pandas as pd
    except ImportError:
        return {}

    df = pd.read_excel(DATASET_XLSX, sheet_name="Parselmouth")
    metadata = {}
    for row in df.to_dict(orient="records"):
        sample_id = str(row["Sample ID"]).strip()
        metadata[sample_id] = {
            "label": str(row["Label"]).strip(),
            "age": float(row["Age"]) if row.get("Age") is not None else "",
            "sex": str(row["Sex"]).strip(),
        }
    return metadata


def lookup_sample_metadata(wav_path: str | Path) -> dict[str, str | float]:
    wav_path = Path(wav_path)
    return load_dataset_metadata().get(wav_path.stem, {})


def get_demo_samples(limit: int = 3) -> list[Path]:
    dataset_root = ARTIFACT_DIR / "dataset"
    if not dataset_root.exists():
        return []

    samples: list[Path] = []
    hc_files = sorted((dataset_root / "HC_AH" / "HC_AH").glob("*.wav"))
    pd_files = sorted((dataset_root / "PD_AH" / "PD_AH").glob("*.wav"))

    if hc_files:
        samples.append(hc_files[0])
    if pd_files:
        samples.append(pd_files[0])
    if len(hc_files) > 1:
        samples.append(hc_files[1])

    return samples[:limit]


def get_audio_duration_seconds(wav_path: str | Path) -> float | None:
    try:
        with wave.open(str(wav_path), "rb") as wav_file:
            frame_rate = wav_file.getframerate()
            frame_count = wav_file.getnframes()
            if frame_rate <= 0:
                return None
            return frame_count / frame_rate
    except Exception:
        try:
            import parselmouth
        except ImportError:
            return None

        try:
            sound = parselmouth.Sound(str(wav_path))
            return float(sound.get_total_duration())
        except Exception:
            return None


def analyze_audio_file(
    wav_path: str | Path,
    model=None,
    scaler=None,
) -> dict:
    wav_path = Path(wav_path).resolve()
    result = predict_app_output_from_wav(str(wav_path), model=model, scaler=scaler)

    duration_seconds = get_audio_duration_seconds(wav_path)
    file_info = {
        "file_name": wav_path.name,
        "path": str(wav_path),
        "size_kb": round(wav_path.stat().st_size / 1024, 1),
        "duration_seconds": round(duration_seconds, 2) if duration_seconds is not None else None,
    }

    metadata = lookup_sample_metadata(wav_path)
    if metadata:
        result["dataset_context"] = {
            "ground_truth_label": metadata.get("label", ""),
            "age": metadata.get("age", ""),
            "sex": metadata.get("sex", ""),
        }
    else:
        result["dataset_context"] = None

    result["file_info"] = file_info
    return result


class VoiceScreeningDemo(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x860")
        self.minsize(1080, 760)
        self.configure(bg=BG_COLOR)

        self.model = None
        self.scaler = None
        self.sample_map = {sample.name: sample for sample in get_demo_samples()}

        self.selected_file = tk.StringVar()
        self.selected_sample = tk.StringVar(value=next(iter(self.sample_map), ""))
        self.status_var = tk.StringVar(value="Choose a WAV file to begin.")
        self.summary_var = tk.StringVar(value="Upload a recording to generate a patient-friendly summary.")
        self.file_meta_var = tk.StringVar(value="No file selected.")
        self.dataset_meta_var = tk.StringVar(value="Dataset metadata will appear here for bundled demo samples.")
        self.score_label_var = tk.StringVar(value="Severity")
        self.score_value_var = tk.StringVar(value="--")
        self.updrs_value_var = tk.StringVar(value="--")
        self.status_chip_var = tk.StringVar(value="Ready")

        self._build_styles()
        self._build_layout()
        self._draw_score_ring(0, "Ready")

    def _build_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Card.TFrame", background=CARD_COLOR)
        style.configure("Hero.TFrame", background=HERO_COLOR)
        style.configure("CardTitle.TLabel", background=CARD_COLOR, foreground=TEXT_COLOR, font=("Segoe UI Semibold", 16))
        style.configure("CardBody.TLabel", background=CARD_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 11))
        style.configure("Muted.TLabel", background=CARD_COLOR, foreground=MUTED_COLOR, font=("Segoe UI", 10))
        style.configure("HeroTitle.TLabel", background=HERO_COLOR, foreground="#fbf8f3", font=("Georgia", 22, "bold"))
        style.configure("HeroBody.TLabel", background=HERO_COLOR, foreground="#d7e3e8", font=("Segoe UI", 11))
        style.configure("MetricValue.TLabel", background=CARD_COLOR, foreground=TEXT_COLOR, font=("Segoe UI Semibold", 26))
        style.configure("MetricTitle.TLabel", background=CARD_COLOR, foreground=MUTED_COLOR, font=("Segoe UI", 10))
        style.configure("Primary.TButton", font=("Segoe UI Semibold", 11))
        style.configure("Secondary.TButton", font=("Segoe UI", 10))

        style.configure(
            "Feature.Treeview",
            background=CARD_COLOR,
            fieldbackground=CARD_COLOR,
            foreground=TEXT_COLOR,
            rowheight=28,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Feature.Treeview.Heading",
            background="#e8f0f0",
            foreground=TEXT_COLOR,
            font=("Segoe UI Semibold", 10),
        )

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        hero = ttk.Frame(self, style="Hero.TFrame", padding=(28, 24))
        hero.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 12))
        hero.columnconfigure(0, weight=1)

        ttk.Label(hero, text=APP_TITLE, style="HeroTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            hero,
            text="Upload a single WAV recording and present a clean patient result plus doctor-ready feature details.",
            style="HeroBody.TLabel",
            wraplength=900,
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        controls = ttk.Frame(self, style="Card.TFrame", padding=22)
        controls.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 12))
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(4, weight=1)

        ttk.Label(controls, text="Audio File", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        file_entry = ttk.Entry(controls, textvariable=self.selected_file, font=("Segoe UI", 11))
        file_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 0), padx=(0, 10))

        self.browse_button = ttk.Button(
            controls,
            text="Choose WAV",
            style="Primary.TButton",
            command=self._choose_file,
        )
        self.browse_button.grid(row=1, column=2, sticky="ew", pady=(8, 0), padx=(0, 10))

        self.analyze_button = ttk.Button(
            controls,
            text="Analyze Recording",
            style="Primary.TButton",
            command=self._start_analysis,
        )
        self.analyze_button.grid(row=1, column=3, sticky="ew", pady=(8, 0))

        if self.sample_map:
            ttk.Label(controls, text="Quick Demo Sample", style="CardTitle.TLabel").grid(row=0, column=4, sticky="w")
            sample_combo = ttk.Combobox(
                controls,
                textvariable=self.selected_sample,
                values=list(self.sample_map.keys()),
                state="readonly",
                font=("Segoe UI", 10),
            )
            sample_combo.grid(row=1, column=4, sticky="ew", pady=(8, 0), padx=(14, 10))
            ttk.Button(
                controls,
                text="Load Sample",
                style="Secondary.TButton",
                command=self._load_sample,
            ).grid(row=1, column=5, sticky="ew", pady=(8, 0))

        ttk.Label(controls, textvariable=self.status_var, style="Muted.TLabel").grid(
            row=2, column=0, columnspan=6, sticky="w", pady=(12, 0)
        )

        content = ttk.Frame(self, style="Card.TFrame")
        content.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(1, weight=1)

        left_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        left_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 12))
        left_card.columnconfigure(0, weight=1)

        ttk.Label(left_card, text="Patient View", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")

        score_area = ttk.Frame(left_card, style="Card.TFrame")
        score_area.grid(row=1, column=0, sticky="ew", pady=(14, 18))
        score_area.columnconfigure(0, weight=1)
        score_area.columnconfigure(1, weight=1)

        self.score_canvas = tk.Canvas(
            score_area,
            width=270,
            height=270,
            bg=CARD_COLOR,
            highlightthickness=0,
        )
        self.score_canvas.grid(row=0, column=0, sticky="w")

        summary_card = ttk.Frame(score_area, style="Card.TFrame", padding=(10, 6))
        summary_card.grid(row=0, column=1, sticky="nsew")
        summary_card.columnconfigure(0, weight=1)

        ttk.Label(summary_card, text="Severity Label", style="MetricTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.severity_badge = tk.Label(
            summary_card,
            textvariable=self.score_label_var,
            bg="#e8f0f0",
            fg=TEXT_COLOR,
            font=("Segoe UI Semibold", 14),
            padx=14,
            pady=8,
        )
        self.severity_badge.grid(row=1, column=0, sticky="w", pady=(8, 18))

        ttk.Label(summary_card, text="Estimated total UPDRS", style="MetricTitle.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Label(summary_card, textvariable=self.updrs_value_var, style="MetricValue.TLabel").grid(row=3, column=0, sticky="w", pady=(6, 18))

        ttk.Label(summary_card, text="Patient Summary", style="MetricTitle.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Label(
            summary_card,
            textvariable=self.summary_var,
            style="CardBody.TLabel",
            wraplength=360,
            justify="left",
        ).grid(row=5, column=0, sticky="w", pady=(8, 0))

        info_card = ttk.Frame(left_card, style="Card.TFrame")
        info_card.grid(row=2, column=0, sticky="ew")
        info_card.columnconfigure(0, weight=1)
        info_card.columnconfigure(1, weight=1)

        file_card = ttk.Frame(info_card, style="Card.TFrame", padding=16)
        file_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(file_card, text="Recording", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(file_card, textvariable=self.file_meta_var, style="CardBody.TLabel", wraplength=360, justify="left").grid(row=1, column=0, sticky="w", pady=(8, 0))

        dataset_card = ttk.Frame(info_card, style="Card.TFrame", padding=16)
        dataset_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(dataset_card, text="Dataset Context", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(dataset_card, textvariable=self.dataset_meta_var, style="CardBody.TLabel", wraplength=360, justify="left").grid(row=1, column=0, sticky="w", pady=(8, 0))

        right_top = ttk.Frame(content, style="Card.TFrame", padding=22)
        right_top.grid(row=0, column=1, sticky="nsew")
        right_top.columnconfigure(0, weight=1)

        ttk.Label(right_top, text="Presentation Snapshot", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.snapshot_text = tk.Text(
            right_top,
            height=12,
            wrap="word",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Consolas", 10),
            relief="flat",
            padx=4,
            pady=4,
        )
        self.snapshot_text.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.snapshot_text.insert("1.0", "Patient and doctor result cards will appear here after analysis.")
        self.snapshot_text.configure(state="disabled")

        right_bottom = ttk.Frame(content, style="Card.TFrame", padding=22)
        right_bottom.grid(row=1, column=1, sticky="nsew", pady=(12, 0))
        right_bottom.columnconfigure(0, weight=1)
        right_bottom.rowconfigure(1, weight=1)

        top_bar = ttk.Frame(right_bottom, style="Card.TFrame")
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.columnconfigure(0, weight=1)

        ttk.Label(right_bottom, text="Doctor Report Features", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.status_chip = tk.Label(
            top_bar,
            textvariable=self.status_chip_var,
            bg="#e8f0f0",
            fg=TEXT_COLOR,
            font=("Segoe UI Semibold", 10),
            padx=10,
            pady=5,
        )
        self.status_chip.grid(row=0, column=1, sticky="e")

        self.feature_table = ttk.Treeview(
            right_bottom,
            columns=("feature", "value"),
            show="headings",
            style="Feature.Treeview",
            height=15,
        )
        self.feature_table.grid(row=1, column=0, sticky="nsew", pady=(14, 0))
        self.feature_table.heading("feature", text="Feature")
        self.feature_table.heading("value", text="Value")
        self.feature_table.column("feature", width=200, anchor="w")
        self.feature_table.column("value", width=120, anchor="center")

    def _choose_file(self) -> None:
        wav_path = filedialog.askopenfilename(
            title="Choose a WAV file",
            filetypes=[("WAV audio", "*.wav")],
        )
        if wav_path:
            self.selected_file.set(wav_path)
            self.status_var.set("File selected. Ready to analyze.")

    def _load_sample(self) -> None:
        sample_name = self.selected_sample.get()
        sample_path = self.sample_map.get(sample_name)
        if sample_path:
            self.selected_file.set(str(sample_path))
            self.status_var.set(f"Loaded demo sample: {sample_name}")

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.browse_button.configure(state=state)
        self.analyze_button.configure(state=state)
        self.status_chip_var.set("Analyzing..." if busy else "Ready")
        self.status_chip.configure(bg="#f4d6b5" if busy else "#e8f0f0")

    def _start_analysis(self) -> None:
        wav_path = self.selected_file.get().strip()
        if not wav_path:
            messagebox.showwarning("Missing file", "Choose a WAV file first.")
            return

        resolved = Path(wav_path)
        if not resolved.exists():
            messagebox.showerror("File not found", "The selected WAV file does not exist.")
            return

        self._set_busy(True)
        self.status_var.set("Running voice feature extraction and prediction...")

        worker = threading.Thread(
            target=self._analyze_worker,
            args=(resolved,),
            daemon=True,
        )
        worker.start()

    def _analyze_worker(self, wav_path: Path) -> None:
        try:
            if self.model is None or self.scaler is None:
                self.model, self.scaler = load_pipeline()

            result = analyze_audio_file(wav_path, model=self.model, scaler=self.scaler)
            self.after(0, lambda: self._render_result(result))
        except Exception as exc:
            self.after(0, lambda: self._handle_error(str(exc)))

    def _handle_error(self, error_message: str) -> None:
        self._set_busy(False)
        self.status_var.set("Analysis failed. See the error dialog for details.")
        messagebox.showerror("Analysis failed", error_message)

    def _render_result(self, result: dict) -> None:
        patient_view = result["patient_view"]
        doctor_report = result["doctor_report"]
        file_info = result["file_info"]
        dataset_context = result.get("dataset_context")

        severity_score = int(patient_view["severity_score"])
        severity_label = str(patient_view["severity_label"])
        estimated_updrs = float(patient_view["estimated_total_updrs"])

        self._draw_score_ring(severity_score, severity_label)
        self.score_label_var.set(severity_label)
        self.score_value_var.set(str(severity_score))
        self.updrs_value_var.set(f"{estimated_updrs:.2f}")
        self.summary_var.set(str(patient_view["summary"]))

        duration_text = (
            f"{file_info['duration_seconds']:.2f} sec" if file_info["duration_seconds"] is not None else "unknown duration"
        )
        self.file_meta_var.set(
            f"{file_info['file_name']}\n{file_info['size_kb']} KB • {duration_text}\n{file_info['path']}"
        )

        if dataset_context:
            self.dataset_meta_var.set(
                f"Ground truth label: {dataset_context['ground_truth_label']}\n"
                f"Age: {dataset_context['age']}\n"
                f"Sex: {dataset_context['sex']}"
            )
        else:
            self.dataset_meta_var.set(
                "This file is not part of the bundled demo dataset, so there is no ground-truth label to show."
            )

        self.snapshot_text.configure(state="normal")
        self.snapshot_text.delete("1.0", "end")
        self.snapshot_text.insert(
            "1.0",
            (
                f"Severity score: {severity_score}/100\n"
                f"Severity label: {severity_label}\n"
                f"Estimated total UPDRS: {estimated_updrs:.2f}\n\n"
                f"Patient summary:\n{patient_view['summary']}\n\n"
                f"Doctor view:\n"
                f"- 12 acoustic features extracted from the WAV\n"
                f"- Raw feature values are listed below\n"
            ),
        )
        self.snapshot_text.configure(state="disabled")

        for item in self.feature_table.get_children():
            self.feature_table.delete(item)
        for feature_name, value in doctor_report["features"].items():
            self.feature_table.insert("", "end", values=(feature_name, f"{value:.6f}"))

        self.status_var.set("Analysis complete. You can try another recording.")
        self._set_busy(False)

    def _draw_score_ring(self, score: int, severity_label: str) -> None:
        score = max(0, min(score, 100))
        extent = (score / 100.0) * 300
        color = self._color_for_label(severity_label)

        self.score_canvas.delete("all")
        self.score_canvas.create_oval(28, 28, 242, 242, outline="#e6dfd3", width=18)
        self.score_canvas.create_arc(
            28,
            28,
            242,
            242,
            start=120,
            extent=-extent,
            style="arc",
            width=18,
            outline=color,
        )
        self.score_canvas.create_text(
            135,
            110,
            text=str(score),
            fill=TEXT_COLOR,
            font=("Georgia", 40, "bold"),
        )
        self.score_canvas.create_text(
            135,
            145,
            text="/ 100",
            fill=MUTED_COLOR,
            font=("Segoe UI", 13),
        )
        self.score_canvas.create_text(
            135,
            186,
            text=severity_label,
            fill=color,
            font=("Segoe UI Semibold", 15),
        )
        self.severity_badge.configure(bg=color, fg="#ffffff")

    @staticmethod
    def _color_for_label(severity_label: str) -> str:
        if severity_label == "Mild":
            return SUCCESS_COLOR
        if severity_label == "Moderate":
            return ACCENT_COLOR
        if severity_label in {"High", "Very High"}:
            return WARN_COLOR
        return HERO_COLOR


def main() -> None:
    app = VoiceScreeningDemo()
    app.mainloop()


if __name__ == "__main__":
    main()
