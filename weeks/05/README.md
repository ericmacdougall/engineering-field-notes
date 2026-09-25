# Week 05 — AI in industrial control needs physical evidence

**Release state:** Eric approved the corrected overview film and article editorially. The corrected [overview film is Public on YouTube](https://www.youtube.com/watch?v=8O5u2a5i6KE), with its watch page, captions and synthetic-voice disclosure read back on September 25, 2026. The journal article remains unpublished while this companion and the live-site checks complete. The 28 approved original written reads are already live as text-only field notes. Add the article link here only after its journal route is read back.

## The claim

Generated PLC logic can compile and still fail the intended physical process. A successful build, an offline process model, an isolated controller bench, and a controlled plant observation answer different questions. The qualified engineering and safety owners define the required behavior and authorize each transition. A model or AI agent can draft and challenge the normal-control logic; it does not become the safety function or the release authority.

## Companion material

- [Physical-evidence oracle](../../examples/physical-evidence-oracle/README.md): a small, synthetic, read-only Python contract that distinguishes a stop command from measured motion and refuses to call missing evidence plant acceptance.
- [Ten discriminating probes](ten-probes.md): proposed desk, offline-model and authorized isolated-bench questions to resolve before a plant window. These are a plan, not claims of live execution.

## Tested boundary

Run `python examples/physical-evidence-oracle/run_probes.py` from the repository root. The ten local synthetic fixtures exercise normal, fault, identity and evidence-gap cases. They do not compile IEC 61131-3 code, connect to a controller, actuate equipment, test a vendor simulator, validate a safety function or commission a machine. The fictional conveyor values and deadlines are examples; a site owner must specify real requirements and independent acceptance evidence.

## Publication rule

The approved written reads may appear on the journal independently of this master article. Publish this week's article only after this companion folder and README are Public, the approved article and film fingerprints still match, and the production build and live article readback pass. The corrected film's Public watch-page, transcript and disclosure have been verified. Social premieres follow their separate calendar. Reference recuts and bonus build tracks need separate approval.
