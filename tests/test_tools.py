import tempfile
import unittest
from pathlib import Path

from jarvis.tools.memory import MemoryTool
from jarvis.tools.system import SystemTool


class SystemToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = SystemTool()

    def test_allows_a_whitelisted_command(self) -> None:
        self.assertEqual(self.tool.run("echo 'arc reactor'"), "arc reactor\n")

    def test_blocks_shell_operator_injection(self) -> None:
        result = self.tool.run("echo safe; pwd")
        self.assertEqual(result, "safe; pwd\n")

    def test_blocks_non_whitelisted_command(self) -> None:
        self.assertTrue(self.tool.run("whoami").startswith("Blocked:"))


class MemoryToolTests(unittest.TestCase):
    def test_history_is_capped_and_returns_a_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryTool(str(Path(directory) / "history.json"), max_history=2)
            memory.add("user", "one")
            memory.add("assistant", "two")
            memory.add("user", "three")

            history = memory.history()
            self.assertEqual([item["content"] for item in history], ["two", "three"])
            history.clear()
            self.assertEqual(len(memory.history()), 2)


if __name__ == "__main__":
    unittest.main()
