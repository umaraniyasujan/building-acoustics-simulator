"""Starter building-acoustics desktop app: Sabine RT estimate only."""
from __future__ import annotations

import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def sabine_rt60(length: float, width: float, height: float, surfaces: list[tuple[str, float, float]]) -> tuple[float, float, float]:
    """Return (volume m³, equivalent absorption area m² sabin, RT60 seconds).

    surfaces entries are (name, area_m2, absorption_coefficient). This is a
    simplified diffuse-field Sabine estimate, not a wave simulation.
    """
    if min(length, width, height) <= 0:
        raise ValueError("Room dimensions must be greater than zero.")
    if not surfaces:
        raise ValueError("Add at least one surface.")
    volume = length * width * height
    absorption = 0.0
    for name, area, alpha in surfaces:
        if area < 0 or not 0 <= alpha <= 1:
            raise ValueError(f"{name}: area must be non-negative and absorption must be between 0 and 1.")
        absorption += area * alpha
    if absorption <= 0:
        raise ValueError("Total absorption must be greater than zero.")
    return volume, absorption, 0.161 * volume / absorption


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Building Acoustics — Starter")
        self.geometry("760x600")
        self.minsize(650, 500)
        self._build()

    def _build(self):
        outer = ttk.Frame(self, padding=14)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Room acoustics: Sabine RT estimate", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Estimate only — not a sound propagation or building transmission simulation.", foreground="#8a3b12").pack(anchor="w", pady=(2, 12))

        dims = ttk.LabelFrame(outer, text="Room dimensions (m)", padding=10)
        dims.pack(fill="x")
        self.length = self._field(dims, "Length", "6")
        self.width = self._field(dims, "Width", "5")
        self.height = self._field(dims, "Height", "2.8")

        box = ttk.LabelFrame(outer, text="Surfaces and absorption", padding=10)
        box.pack(fill="both", expand=True, pady=12)
        ttk.Label(box, text="Enter the total area and an approximate absorption coefficient (0–1) for each surface group.").pack(anchor="w", pady=(0, 8))
        self.tree = ttk.Treeview(box, columns=("area", "alpha"), show="headings", height=8)
        self.tree.heading("area", text="Area (m²)")
        self.tree.heading("alpha", text="Absorption coefficient")
        self.tree.column("area", width=120, anchor="center")
        self.tree.column("alpha", width=180, anchor="center")
        self.tree.pack(fill="both", expand=True)
        for item in [("Floor", "30", "0.05"), ("Ceiling", "30", "0.10"), ("Walls", "61.6", "0.05")]:
            self.tree.insert("", "end", values=item)
        row = ttk.Frame(box)
        row.pack(fill="x", pady=(8, 0))
        self.surface_name = ttk.Entry(row, width=18)
        self.surface_name.insert(0, "New surface")
        self.surface_name.pack(side="left", padx=(0, 6))
        self.surface_area = ttk.Entry(row, width=10)
        self.surface_area.insert(0, "10")
        self.surface_area.pack(side="left", padx=6)
        self.surface_alpha = ttk.Entry(row, width=10)
        self.surface_alpha.insert(0, "0.2")
        self.surface_alpha.pack(side="left", padx=6)
        ttk.Button(row, text="Add surface", command=self.add_surface).pack(side="left", padx=6)
        ttk.Button(row, text="Remove selected", command=self.remove_surface).pack(side="left", padx=6)

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Calculate estimate", command=self.calculate).pack(side="left")
        ttk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side="left", padx=8)
        self.result = ttk.Label(outer, text="Enter inputs, then calculate.", font=("Segoe UI", 11, "bold"), justify="left")
        self.result.pack(anchor="w", pady=12)
        ttk.Label(outer, text="Assumptions: frequency-independent absorption, diffuse field, Sabine formula. Real results depend on geometry, furnishings, scattering, and measured material data.", wraplength=700).pack(anchor="w")

    @staticmethod
    def _field(parent, label, default):
        frame = ttk.Frame(parent)
        frame.pack(side="left", padx=(0, 18))
        ttk.Label(frame, text=label).pack(anchor="w")
        entry = ttk.Entry(frame, width=12)
        entry.insert(0, default)
        entry.pack()
        return entry

    def add_surface(self):
        try:
            name = self.surface_name.get().strip() or "Surface"
            area = float(self.surface_area.get())
            alpha = float(self.surface_alpha.get())
            if area < 0 or not 0 <= alpha <= 1:
                raise ValueError("Area must be non-negative and coefficient must be in [0, 1].")
            self.tree.insert("", "end", values=(name, area, alpha))
        except ValueError as exc:
            messagebox.showerror("Invalid surface", str(exc))

    def remove_surface(self):
        for selected in self.tree.selection():
            self.tree.delete(selected)

    def data(self):
        surfaces = [(str(v[0]), float(v[1]), float(v[2])) for v in (self.tree.item(i, "values") for i in self.tree.get_children())]
        return float(self.length.get()), float(self.width.get()), float(self.height.get()), surfaces

    def calculate(self):
        try:
            v, a, rt = sabine_rt60(*self.data())
            self.result.config(text=f"Calculated estimate\nVolume: {v:.2f} m³   |   Equivalent absorption: {a:.2f} m² sabin\nSabine RT60: {rt:.2f} s")
        except ValueError as exc:
            messagebox.showerror("Check inputs", str(exc))

    def export_csv(self):
        try:
            length, width, height, surfaces = self.data()
            volume, absorption, rt = sabine_rt60(length, width, height, surfaces)
        except ValueError as exc:
            messagebox.showerror("Check inputs", str(exc))
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="acoustics_estimate.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Result type", "Calculated estimate (Sabine RT60)"])
            writer.writerow(["Length (m)", length]); writer.writerow(["Width (m)", width]); writer.writerow(["Height (m)", height])
            writer.writerow(["Volume (m3)", volume]); writer.writerow(["Equivalent absorption area (m2 sabin)", absorption]); writer.writerow(["RT60 estimate (s)", rt])
            writer.writerow([]); writer.writerow(["Surface", "Area (m2)", "Absorption coefficient"])
            writer.writerows(surfaces)
        messagebox.showinfo("Export complete", f"Saved {path}")


if __name__ == "__main__":
    App().mainloop()
