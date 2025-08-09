import os
import re

README_FILE = "README.md"
SOLUTIONS_FOLDER = "."  # Change if your solutions are in a subfolder like "solutions/"

def create_progress_bar(percentage):
    """Return a colorful progress bar string based on percentage."""
    total_blocks = 20
    filled_blocks = int(total_blocks * percentage / 100)
    empty_blocks = total_blocks - filled_blocks
    bar = f"{'█' * filled_blocks}{'░' * empty_blocks}"

    # Special trophy for 100%
    if percentage == 100:
        return f"🏆 [{bar}] 100.0% — All problems solved!"

    # Color emoji based on progress level
    if percentage >= 80:
        emoji = "🟩"
    elif percentage >= 50:
        emoji = "🟨"
    else:
        emoji = "🟥"

    return f"{emoji} [{bar}] {percentage:.1f}%"


def update_readme():
    # Read README
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Find all Python solution files in the folder
    solved_files = {file for file in os.listdir(SOLUTIONS_FOLDER) if file.endswith(".py")}

    # Regex to match each table row in the problems table:
    # Captures:
    # - full row text
    # - problem number
    # - difficulty (Easy, Medium, Hard)
    # - status emoji (✅, ❌, ⏳)
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

    found_rows = table_pattern.findall(readme_content)
    print(f"DEBUG: Found {len(found_rows)} problem rows in README")  # Debug print

    for full_row, problem_num_str, difficulty, status in found_rows:
        total_problems += 1
        difficulty_stats[difficulty]["total"] += 1

        problem_num = int(problem_num_str)
        filename_prefix = f"{problem_num:02}_"

        # Find a solution file starting with the problem number prefix
        matching_file = next((f for f in solved_files if f.startswith(filename_prefix)), None)

        if matching_file:
            solved_count += 1
            difficulty_stats[difficulty]["solved"] += 1
            # Mark row as solved ✅ and add link to solution file
            new_row = re.sub(r"\|\s*(✅|❌|⏳)\s*\|", "| ✅ |", full_row)
            new_row = re.sub(r"\|\s*-\s*\|", f"| [{matching_file}]({matching_file}) |", new_row)
        else:
            # Mark row as unsolved ❌ and remove link
            new_row = re.sub(r"\|\s*(✅|❌|⏳)\s*\|", "| ❌ |", full_row)
            new_row = re.sub(r"\|\s*\[.*?\]\(.*?\)\s*\|", "| - |", new_row)

        updated_rows.append(new_row)

    # Replace old table rows with updated ones in the README content
    updated_content = table_pattern.sub(lambda m: updated_rows.pop(0), readme_content)

    # Calculate overall progress percentage
    percentage = (solved_count / total_problems) * 100 if total_problems > 0 else 0
    progress_bar = create_progress_bar(percentage)

    # Update or insert the progress bar section
    progress_pattern = re.compile(r"## 📊 Progress\n.*?\n", re.DOTALL)
    if "## 📊 Progress" in updated_content:
        updated_content = progress_pattern.sub(f"## 📊 Progress\n{progress_bar}\n\n", updated_content)
    else:
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"## 📊 Progress\n{progress_bar}\n\n## 🎯 Goal"
        )

    # Build the summary table by difficulty
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

    # Replace or insert the summary section in README
    summary_pattern = re.compile(r"## 📊 Summary by Difficulty\n(?:\|.*\n)+", re.DOTALL)
    if "## 📊 Summary by Difficulty" in updated_content:
        updated_content = summary_pattern.sub(summary_text, updated_content)
    else:
        # Insert summary just before the "## 🎯 Goal" section
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"{summary_text}\n## 🎯 Goal"
        )

    # Save the updated README.md file
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✅ README.md updated! {solved_count}/{total_problems} solved ({percentage:.1f}%)")


if __name__ == "__main__":
    update_readme()
