import copy
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import handoff_contract


class HandoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((ROOT / "examples/source.json").read_text(encoding="utf-8"))
        cls.ack = json.loads((ROOT / "examples/ack.json").read_text(encoding="utf-8"))

    def packet(self):
        return {
            "id": "handoff-001",
            "source_id": self.source["id"],
            "source_version": self.source["version"],
            "source_digest": handoff_contract.canonical_digest(self.source),
            "target_tenant": self.source["tenant"],
            "material_clauses": copy.deepcopy(self.source["material_clauses"]),
        }

    def verdict(self, packet=None, ack=None, today=date(2026, 9, 25)):
        return handoff_contract.audit(
            self.source, packet if packet is not None else self.packet(),
            ack if ack is not None else self.ack, today
        )

    def test_complete_round_trip_passes_packet_fidelity_only(self):
        result = self.verdict()
        self.assertEqual(result["state"], "PASS")
        self.assertFalse(result["execution_authorized"])

    def test_missing_prerequisite_is_unverified(self):
        packet = self.packet()
        packet["material_clauses"] = [x for x in packet["material_clauses"] if x["id"] != "prerequisite"]
        self.assertEqual(self.verdict(packet)["state"], "UNVERIFIED")

    def test_changed_prerequisite_fails(self):
        packet = self.packet()
        packet["material_clauses"][1]["text"] = "Security review can happen after launch."
        self.assertEqual(self.verdict(packet)["state"], "FAIL")

    def test_wrong_tenant_fails(self):
        packet = self.packet()
        packet["target_tenant"] = "other-tenant"
        self.assertEqual(self.verdict(packet)["state"], "FAIL")

    def test_unacknowledged_clause_is_unverified(self):
        ack = copy.deepcopy(self.ack)
        ack["acknowledged_clause_ids"].remove("prerequisite")
        self.assertEqual(self.verdict(ack=ack)["state"], "UNVERIFIED")

    def test_expired_source_fails(self):
        self.assertEqual(self.verdict(today=date(2026, 12, 2))["state"], "FAIL")

    def test_unsupported_clause_fails(self):
        packet = self.packet()
        packet["material_clauses"].append({"id": "auto-approval", "text": "Security review is optional."})
        self.assertEqual(self.verdict(packet)["state"], "FAIL")


if __name__ == "__main__":
    unittest.main()
