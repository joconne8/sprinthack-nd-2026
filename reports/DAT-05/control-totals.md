# Disjoint source reconciliation

Counts: source = accepted (including corrected) + duplicate + rejected.
Numeric gross/refunds: source = accepted + duplicate + rejected money.
If any required source money is nonnumeric, the corresponding source/rejected
controls stay null rather than using a guessed zero. Differences/rejected rows
block publication; valid staging rows in a failed batch remain evidence only.

Fixed test: existing row gross 10.00/refund 1.00 plus new row gross 20.00/refund
2.00 → source gross 30.00, duplicate gross 10.00, accepted gross 20.00, rejected
gross 0.00. Curated demo net sales remain 27.00. Source payouts/shipping/tax/fees
are excluded. Manifest controls, row-count/checksum/date mismatches, malformed
rows and exception resolution are verified in foundation tests.
