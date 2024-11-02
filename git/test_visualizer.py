import unittest
from unittest.mock import patch, mock_open
import subprocess
import os
from typing import List
from dependency_visualizer import get_commit_messages, build_mermaid_graph, save_graph_to_file, main


REPO_PATH = "repoz"
OUTPUT_FILE_PATH = "result.mmd"

class TestCommitDependencyVisualizer(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_commit_messages(self, mock_run):
        # Имитация вывода команды `git log`
        mock_run.return_value.stdout = "initial commit\nadded second change\nadded third change"
        mock_run.return_value.returncode = 0

        # Ожидаемый результат
        expected_messages = ["initial commit", "added second change", "added third change"]

        # Вызов тестируемой функции
        commit_messages = get_commit_messages("fake/repo/path")

        # Проверка соответствия результата ожиданиям
        self.assertEqual(commit_messages, expected_messages[::-1])

    def test_build_mermaid_graph(self):
        # Входные данные
        commit_messages = ["initial commit", "added second change", "added third change"]
        # Ожидаемый результат
        expected_graph = (
            "graph TD;\n"
            "    0: \"initial commit\"\n"
            "    1: \"added second change\"\n"
            "    2: \"added third change\"\n"
            "    0 --> 1\n"
            "    1 --> 2"
        )
        # Вызываем функцию
        graph = build_mermaid_graph(commit_messages)
        # Проверяем, что граф совпадает с ожидаемым
        self.assertEqual(graph, expected_graph)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_graph_to_file(self, mock_file):
        # Входные данные: граф и путь к файлу
        graph = "graph TD;\n0[\"Initial commit\"]\n1[\"Added feature\"]\n0 --> 1"

        # Вызываем функцию
        save_graph_to_file(graph, OUTPUT_FILE_PATH)

        # Проверяем, что open был вызван с правильными аргументами
        mock_file.assert_called_once_with(OUTPUT_FILE_PATH, "w")

        # Проверяем, что файл был записан с правильным содержимым
        mock_file().write.assert_called_once_with(graph)

    @patch("builtins.open", new_callable=mock_open)
    def test_main_with_existing_repo(self, mock_file):
        with patch("sys.argv", ["prog", "--repo-path", REPO_PATH, "--output-file", OUTPUT_FILE_PATH]):
            main()

        # Проверяем, что файл был записан
        mock_file.assert_called_once_with(OUTPUT_FILE_PATH, "w")
        # Здесь можно расширить тест для проверки содержимого, если сообщения коммитов известны


if __name__ == "__main__":
    unittest.main()
