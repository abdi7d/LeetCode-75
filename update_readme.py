import os
import re

README_FILE = "README.md"
SOLUTIONS_FOLDER = "."

def create_progress_bar(percentage):
    total_blocks = 20
    filled_blocks = int(total_blocks * percentage / 100)
    empty_blocks = total_blocks - filled_blocks
    bar = f"{'█' * filled_blocks}{'░' * empty_blocks}"
    if percentage == 100:
        return f"🏆 [{bar}] 100.0% — All problems solved!"
    if percentage >= 80:
        emoji = "🟩"
    elif percentage >= 50:
        emoji = "🟨"
    else:
        emoji = "🟥"
    return f"{emoji} [{bar}] {percentage:.1f}%"

def update_readme():
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    solved_files = {file for file in os.listdir(SOLUTIONS_FOLDER) if file.endswith(".py") and file != "update_readme.py"}

    # Regex for table row: | num | problem | difficulty | status | solution |
    table_pattern = re.compile(
        r"(\|\s*(\d+)\s*\|\s*([^\|]+?)\s*\|\s*(Easy|Medium|Hard)\s*\|\s*(✅|❌|⏳)\s*\|\s*([^\|]+?)\s*\|)", re.MULTILINE)

    updated_rows = []
    solved_count = 0
    total_problems = 0
    difficulty_stats = {
        "Easy": {"total": 0, "solved": 0},
        "Medium": {"total": 0, "solved": 0},
        "Hard": {"total": 0, "solved": 0},
    }

    found_rows = table_pattern.findall(readme_content)
    for full_row, num, problem, difficulty, status, solution in found_rows:
        total_problems += 1
        difficulty_stats[difficulty]["total"] += 1
        problem_num = int(num)
        filename_prefix = f"{problem_num:02}_"
        matching_file = next((f for f in solved_files if f.startswith(filename_prefix)), None)
        if matching_file:
            solved_count += 1
            difficulty_stats[difficulty]["solved"] += 1
            new_row = f"| {num} | {problem.strip()} | {difficulty} | ✅ | [{matching_file}]({matching_file}) |"
        else:
            new_row = f"| {num} | {problem.strip()} | {difficulty} | ❌ | - |"
        updated_rows.append(new_row)

    # Replace old table rows with updated ones
    def row_replacer(match):
        return updated_rows.pop(0)
    updated_content = table_pattern.sub(row_replacer, readme_content)

    # Progress bar
    percentage = (solved_count / total_problems) * 100 if total_problems > 0 else 0
    progress_bar = create_progress_bar(percentage)
    progress_pattern = re.compile(r"## 📊 Progress\n.*?\n\n", re.DOTALL)
    if "## 📊 Progress" in updated_content:
        updated_content = progress_pattern.sub(f"## 📊 Progress\n{progress_bar}\n\n", updated_content)
    else:
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"## 📊 Progress\n{progress_bar}\n\n## 🎯 Goal"
        )

    # Summary by difficulty
    summary_lines = [
        "## 📊 Summary by Difficulty\n",
        "| Difficulty | Total | Solved | Unsolved |",
        "|------------|-------|--------|----------|",
    ]
    for diff in ["Easy", "Medium", "Hard"]:
        total = difficulty_stats[diff]["total"]
        solved = difficulty_stats[diff]["solved"]
        unsolved = total - solved
        summary_lines.append(f"| {diff} | {total} | {solved} | {unsolved} |")
    summary_text = "\n".join(summary_lines) + "\n"
    summary_pattern = re.compile(r"## 📊 Summary by Difficulty\n(?:\|.*\n)+", re.DOTALL)
    if "## 📊 Summary by Difficulty" in updated_content:
        updated_content = summary_pattern.sub(summary_text, updated_content)
    else:
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"{summary_text}\n## 🎯 Goal"
        )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"✅ README.md updated! {solved_count}/{total_problems} solved ({percentage:.1f}%)")

if __name__ == "__main__":
    update_readme()