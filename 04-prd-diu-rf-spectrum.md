PRD 4: DIU RF SPECTRUM ANALYSIS WITH LLMS (not recommended)

PROBLEM
Use SDR output plus LLMs to identify signals, explain spectrum, flag anomalies. No hardware, public captures.

HONEST TAKE
Visually the best demo of the DIU two (waterfall plots look great), but the real work is signal processing. LLMs do not read raw IQ. You would need feature extraction first. Pick only if your builder has DSP or ham radio background.

SCOPE (must have)
1. Ingest public SDR captures (find sample IQ/WAV recordings in the first hour, e.g. public datasets and recorded FM, ADS-B, weather satellite, ISM band captures; verify licenses).
2. DSP pipeline (numpy/scipy): spectrogram, peak detection, bandwidth and occupancy estimates, simple modulation hints.
3. Convert features to structured text and images for the LLM: "signal at X MHz, bandwidth Y kHz, bursty, period Z."
4. LLM explainer: identifies likely signal type with confidence and cites the features, explains in plain language.
5. Anomaly flag: compare against a baseline capture and flag new or changed signals.
6. UI: waterfall viewer with annotated signals and an explanation panel.

NICE TO HAVE
Chat with the spectrum, ground-truth check against known band plans.

OUT OF SCOPE
Live hardware, demodulating encrypted or digital protocols, geolocation.

RISKS
Wrong IDs stated confidently. Mitigate: ground truth from labeled captures, show a confusion table honestly, LLM must say "unknown" when features do not match a known band plan. Large files slow everything. Time lost finding good captures.

DEMO SCRIPT
0:00 Why spectrum awareness matters and why analysts are overloaded.
1:00 Load a capture, waterfall appears.
2:00 Click a signal, get explanation and evidence.
3:30 Load second capture with a planted anomaly, flagged.
5:00 Accuracy on labeled set, with the misses shown.
