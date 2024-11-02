import os
import subprocess
import argparse
from typing import List


def get_commit_messages(repo_path: str) -> List[str]:

    # Формируем команду git для получения сообщений всех коммитов
    git_command = [
        "git",
        "-C",  # Используем ключ -C для работы в указанной директории репозитория
        repo_path,
        "log",  # Команда git log для получения списка коммитов
        "--pretty=format:%s"  # Только сообщения коммитов (без хешей, авторов и дат)
    ]

    # Выполняем команду git и сохраняем результат в result
    result = subprocess.run(git_command, stdout=subprocess.PIPE, text=True)

    # Проверяем, успешно ли завершилась команда git
    if result.returncode != 0:
        raise Exception(f"Ошибка при выполнении git-команды: {result.stderr}")

    # Разбиваем вывод команды на строки
    commit_messages = result.stdout.splitlines()
    return commit_messages[::-1]


def build_mermaid_graph(commit_messages: List[str]) -> str:
    # Начинаем построение графа Mermaid с указания типа диаграммы
    graph_lines = ["graph TD;"]

    # Проходим по каждому коммиту и добавляем его в граф
    for i, message in enumerate(commit_messages):
        # Формируем метку узла: коммит представлен его сообщением
        node_label = f"{i}: \"{message}\""
        # Добавляем узел в граф
        graph_lines.append(f"    {node_label}")

        # Затем создаем связи между узлами в хронологическом порядке
    for i in range(1, len(commit_messages)):
        graph_lines.append(f"    {i - 1} --> {i}")

    # Объединяем все строки графа в одну строку для вывода в виде Mermaid-кода
    return "\n".join(graph_lines)


def save_graph_to_file(graph: str, output_file: str) -> None:
    # Записываем код графа в файл
    with open(output_file, "w") as file:
        file.write(graph)

    print(f"Граф зависимостей сохранён в {output_file}.")

def main():
    # Создаём парсер аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Инструмент для визуализации графа зависимостей git-коммитов в формате Mermaid.")

    # Аргумент для указания пути к git-репозиторию
    parser.add_argument("--repo-path", required=True, help="Путь к анализируемому git-репозиторию.")

    # Аргумент для указания пути к файлу, в который будет сохранён результат (код графа)
    parser.add_argument("--output-file", required=True, help="Путь к выходному файлу с кодом графа Mermaid.")

    # Читаем аргументы командной строки
    args = parser.parse_args()

    # Проверяем, существует ли указанный путь к репозиторию
    if not os.path.exists(args.repo_path):
        print(f"Ошибка: Путь к репозиторию '{args.repo_path}' не существует.")
        return

    # Получаем список сообщений коммитов из репозитория
    commit_messages = get_commit_messages(args.repo_path)

    # Проверяем, есть ли коммиты в репозитории
    if not commit_messages:
        print(f"В репозитории не найдено коммитов.")
        return

    # Строим граф зависимостей на основе сообщений коммитов
    graph = build_mermaid_graph(commit_messages)

    # Сохраняем граф в указанный файл
    save_graph_to_file(graph, args.output_file)

    # Выводим граф зависимостей на экран (консоль)
    print("\nГраф зависимостей в формате Mermaid:")
    print(graph)

if __name__ == "__main__":
    main()
