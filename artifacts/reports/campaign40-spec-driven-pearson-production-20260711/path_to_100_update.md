# Campaign 40 Path-to-100 Update

Actual specification-driven evidence:

- Frozen candidates processed: 8
- Accepted: 6
- Rejected: 2
- Accepted yield: 0.75
- Acquisition duration: 0.07s offline reuse for corrected rerun; live acquisition was 4.128s in provisional execution.
- Publication duration: 0.266s in live execution; bounded replacement/reindex succeeded.
- PostgreSQL rebuild duration: captured in replacement evidence; rebuild return code 0.
- Repository count after Campaign 40: 538
- Pearson relationship objects after Campaign 40: 13
- Remaining to 100: 87
- Batches needed at actual Campaign 40 accepted yield (6 per batch): 15

Dominant bottleneck is no longer coefficient computation. It is coefficient-free registry construction plus evidence/acquisition/validation governance for candidates likely to survive missingness and construction-risk checks.

Realistic next batch size remains 6-8 frozen candidates with expected 5-6 accepted until registry automation and downstream consumption pressure improve.
