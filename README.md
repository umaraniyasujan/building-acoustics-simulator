# Building Acoustics Simulator

A lightweight, offline-first Python prototype for exploring basic room acoustics. The first milestone focuses on room dimensions, surface absorption, a Sabine reverberation-time estimate, and CSV export.

## Scope and limitations

This prototype calculates a Sabine RT estimate from user-entered areas and absorption coefficients. It does **not** simulate sound propagation, transmission between rooms, impact sound, or speech intelligibility, and it is not a standards-compliance tool. Results are estimates and depend on entered data and the diffuse-field assumptions of the Sabine method.

## Run on Windows 11

1. Install Python 3.10 or newer.
2. Open PowerShell in this directory.
3. Run `python app.py`.

Only Python's standard library is required. `python -m unittest` runs the basic tests.

## First milestone

- Tkinter desktop UI.
- Room dimensions and frequency-independent surface absorption inputs.
- Sabine estimate: `RT60 = 0.161 × V / A` (SI units), where V is room volume and A is equivalent absorption area.
- Save a results CSV.

## Next steps

Validate formulas and inputs, then add a frequency-band material library and benchmarked room impulse-response engine before presenting simulated results.
