
1. Simulated Evidence Generation Pipeline
Our pipeline begins with a simulated multi-source, multi-modal data generation module delivered at fixed time intervals to our agent system. We use begin with publically available video datasets including annotated subclips from these videos. For a given subset of videos, we use a parent VLM model to generate a text-based situation report detailing a plausible hazardous scenario requiring further investigation. The report R_i (1<= i <= k) will be associated with E_i total pieces of evidence. For each report R_i we create j variations, so that E_ij will contain the same E_i pieces of evidence, but reported at different timestamps (via random permutations). This represents different possible data-intake scenarios, where evidence may or may not be received when it is most useful for evidence-based QA.

Each report is created with instructions to the VLM to generate 1) a 300-word summary of the incident, 2) Q/A pairs with answers supported via the visual evidence.


2. Memory Consolidation
Our experiment compares different memory consolidation setups for the synthetic evidence dataset. We compare 1) meta-agent with fixed memory budget + evidence replacement, 2) meta-agent w/ fixed memory budget without replacement, 3) no meta-agent with fixed memory budget and without replacement.

Next, for every generated report, the parent VLM generates in chronological order for each incoming piece of evidence E 1) the NLI relation between E



3. Experiment Setup
- Cross-Task Transfer Ability of the compression strategies.
- In our experiments, once a memory compression agent has gone through a full run in one domain/dataset, we will transfer it to a new task domain and see if the memory compression strategy will still lead to improvement.