PRD 3: DIU RESILIENT COMMS, METADATA HIDING (not recommended)

PROBLEM
Use generative AI to hide message metadata on open networks (LoRa mesh, Direct-to-Cell). Simulation allowed.

HONEST TAKE
Hard to show "hidden" convincingly. Traffic analysis is a research field. Pick this only if your builder knows networking or crypto.

SCOPE (must have)
1. Network simulator: nodes exchanging messages with realistic metadata (size, timing, source/dest, frequency of contact). Simple Python discrete-event sim.
2. Adversary: a classifier that infers who talks to whom or message type from metadata alone (baseline attack).
3. Defense: generative cover traffic that shapes packet size and timing to look like benign background traffic (a model trained or prompted to produce plausible traffic patterns), with padding and batching.
4. Measurement: attacker accuracy before vs after defense, and cost (added bandwidth, latency).
5. Dashboard: side-by-side attacker view with and without defense.

OUT OF SCOPE
Real radios, real crypto design, any claim of security guarantees.

KEY DATA
Everything synthetic. Say so loudly. Any accuracy numbers are results of your simulation, not real-world claims.

SUCCESS CRITERIA
Attacker accuracy drops meaningfully in the sim at a stated overhead cost, reproducibly.

RISKS
Judges will ask "how do you know the sim reflects real LoRa?" You have no good answer in 28 hours. Defense may look like just random noise. LoRa airtime limits make cover traffic costly, which undercuts the idea.

DEMO SCRIPT
0:00 Threat: even with encrypted content, who talks when gives away units and plans.
1:00 Attacker model reconstructs the network from metadata.
2:30 Turn on defense. Attacker accuracy falls.
4:00 Show the cost tradeoff and limits.
5:00 Path to real hardware testing.
