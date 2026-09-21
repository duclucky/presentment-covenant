# Official source lock

Refreshed 2026-09-21T10:30:56Z. URLs are frozen for this build; claims are limited to the support boundaries below.

| Source | Supports | Does not support |
|---|---|---|
| https://docs.genlayer.com/developers/intelligent-contracts/first-contract | current contract structure and Python API family | deployment success or adoption |
| https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle | leader/validator equivalence and custom validator pattern | truth of an external document |
| https://docs.genlayer.com/developers/intelligent-contracts/testing | direct and Studio testing boundaries | network finality evidence |
| https://docs.genlayer.com/developers/intelligent-contracts/features/value-transfers | payable metadata, GEN units, and EOA transfer interface | a successful transfer in this repository |
| https://docs.genlayer.com/developers/consensus-v06-migration | Studio Dev chain ID 61997, RC compatibility family, fee-aware transaction requirement | current deployment address or transaction success |
| https://docs.genlayer.com/api-references/genlayer-py | Studio Dev client profile and fee estimation/submission flow | a successful deployment in this repository |
| https://github.com/dcsaorg/Conformance-Gateway/tree/1d0bf380123a849f6b15ad255055f4abcfb96f1a | DCSA official synthetic conformance fixture provenance | real-world bill of lading, title, or commercial truth |
| https://reference.dcsa.org/content/standards/guidelines/implementing-ebl-td-digital-signatures | DCSA eBL integrity/authenticity design context | invoice authenticity or legal enforceability |
| https://uncitral.un.org/en/texts/ecommerce/modellaw/electronic_transferable_records | functional-equivalence concepts for electronic records | enactment or legal effect in a jurisdiction |

Pinned DCSA fixture URL:

`https://raw.githubusercontent.com/dcsaorg/Conformance-Gateway/1d0bf380123a849f6b15ad255055f4abcfb96f1a/ebl/src/main/resources/standards/ebl/messages/ebl-api-3.0.0-negotiable-bl.json`

Observed response: HTTP 200, 2,588 bytes, SHA-256 `2098535c024fafa973577ef2f3c5c7b9b60ec06d0413c08bf143bfb2d57fa7ed`.

Material drift: the target network and runtime/API family moved from legacy Studionet/v0.2 to Studio Dev/Consensus v0.6 RC. This revision migrates the contract and tooling as one unit, pins the new dependencies, and records a matching Studio Dev schema preflight. The frozen DCSA evidence body and digest did not drift. A later changed body, URL, runtime hash, chain definition, or receipt shape blocks advancement and requires a new compatibility record.
