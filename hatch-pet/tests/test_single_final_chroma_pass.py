import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"


class SingleFinalChromaPassTest(unittest.TestCase):
    def test_cleanup_runs_once_after_v2_assembly_across_instruction_surface(self) -> None:
        instructions = "\n".join(
            path.read_text() for path in (SKILL, *sorted(REFERENCES.glob("*.md")))
        )

        self.assertEqual(instructions.count("scripts/despill_chroma_edges.py"), 1)
        self.assertNotIn("chroma-despill-standard.json", instructions)
        self.assertLess(
            instructions.index("scripts/assemble_extended_atlas.py"),
            instructions.index("scripts/despill_chroma_edges.py"),
        )

    def test_main_skill_routes_detailed_workflows_to_existing_references(self) -> None:
        main_instructions = SKILL.read_text()
        expected_references = (
            "generation-policy.md",
            "look-directions-and-qa.md",
            "worker-delegation.md",
            "acceptance-and-repair.md",
        )

        for filename in expected_references:
            with self.subTest(filename=filename):
                self.assertIn(
                    f"[{filename}](references/{filename})",
                    main_instructions,
                )
                self.assertTrue((REFERENCES / filename).is_file())

    def test_main_skill_stays_below_progressive_disclosure_limit(self) -> None:
        self.assertLess(len(SKILL.read_text().splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
