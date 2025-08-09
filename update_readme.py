import os
import re

README_FILE = "README.md"
SOLUTIONS_FOLDER = "."  # Change if your solutions are in a subfolder

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

    solved_files = {file for file in os.listdir(SOLUTIONS_FOLDER) if file.endswith(".py")}

    # Regex to extract table rows (problem number, difficulty, status)
    table_pattern = re.compile(
        r"(\|\s*(\d+)\s*\|.*?\|\s*(Easy|Medium|Hard)\s*\|\s*(✅|❌|⏳)\s*\|.*?\|)", re.DOTALL)

    updated_rows = []

    solved_count = 0
    total_problems = 0

    # Counters by difficulty
    difficulty_stats = {
        "Easy": {"total": 0, "solved": 0},
        "Medium": {"total": 0, "solved": 0},
        "Hard": {"total": 0, "solved": 0},
    }

    for full_row, problem_num, difficulty, status in table_pattern.findall(readme_content):
        total_problems += 1
        difficulty_stats[difficulty]["total"] += 1

        problem_num = int(problem_num)
        filename_prefix = f"{problem_num:02}_"

        matching_file = next((f for f in solved_files if f.startswith(filename_prefix)), None)

        if matching_file:
            solved_count += 1
            difficulty_stats[difficulty]["solved"] += 1
            new_row = re.sub(r"\|\s*(✅|❌|⏳)\s*\|", "| ✅ |", full_row)
            new_row = re.sub(r"\|\s*-\s*\|", f"| [{matching_file}]({matching_file}) |", new_row)
        else:
            new_row = re.sub(r"\|\s*(✅|❌|⏳)\s*\|", "| ❌ |", full_row)
            new_row = re.sub(r"\|\s*\[.*?\]\(.*?\)\s*\|", "| - |", new_row)

        updated_rows.append(new_row)

    updated_content = table_pattern.sub(lambda m: updated_rows.pop(0), readme_content)

    percentage = (solved_count / total_problems) * 100 if total_problems else 0
    progress_bar = create_progress_bar(percentage)

    # Replace or add progress bar
    progress_pattern = re.compile(r"## 📊 Progress\n.*?\n", re.DOTALL)
    if "## 📊 Progress" in updated_content:
        updated_content = progress_pattern.sub(f"## 📊 Progress\n{progress_bar}\n\n", updated_content)
    else:
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"## 📊 Progress\n{progress_bar}\n\n## 🎯 Goal"
        )

    # Generate the summary table text
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

    # Replace or insert the summary section
    summary_pattern = re.compile(r"## 📊 Summary by Difficulty\n(?:\|.*\n)+", re.DOTALL)
    if "## 📊 Summary by Difficulty" in updated_content:
        updated_content = summary_pattern.sub(summary_text, updated_content)
    else:
        # Insert summary after progress bar
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"{summary_text}\n## 🎯 Goal"
        )

    # Save back
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✅ README.md updated! {solved_count}/{total_problems} solved ({percentage:.1f}%)")


if __name__ == "__main__":
    update_readme()
