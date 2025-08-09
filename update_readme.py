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

    # Find solved files
    solved_files = {file for file in os.listdir(SOLUTIONS_FOLDER) if file.endswith(".py")}

    # Pattern to find table rows
    table_pattern = re.compile(r"(\|\s*\d+\s*\|.+?\|\s*(?:✅|❌|⏳)\s*\|\s*.*?\|)", re.DOTALL)
    updated_rows = []

    solved_count = 0
    total_problems = 0

    for row in table_pattern.findall(readme_content):
        total_problems += 1

        # Extract problem number
        num_match = re.match(r"\|\s*(\d+)\s*\|", row)
        if not num_match:
            updated_rows.append(row)
            continue

        problem_num = int(num_match.group(1))
        filename_prefix = f"{problem_num:02}_"  # e.g. "01_", "02_"

        # Check if solution exists
        matching_file = next((f for f in solved_files if f.startswith(filename_prefix)), None)

        if matching_file:
            solved_count += 1
            new_row = re.sub(r"\|\s*(✅|❌|⏳)\s*\|", "| ✅ |", row)
            new_row = re.sub(r"\|\s*-\s*\|", f"| [{matching_file}]({matching_file}) |", new_row)
        else:
            new_row = re.sub(r"\|\s*(✅|❌|⏳)\s*\|", "| ❌ |", row)
            new_row = re.sub(r"\|\s*\[.*?\]\(.*?\)\s*\|", "| - |", new_row)

        updated_rows.append(new_row)

    # Replace old table rows with updated ones
    updated_content = table_pattern.sub(lambda m: updated_rows.pop(0), readme_content)

    # Calculate progress
    percentage = (solved_count / total_problems) * 100 if total_problems > 0 else 0
    progress_bar = create_progress_bar(percentage)

    # Update or insert progress bar
    progress_pattern = re.compile(r"## 📊 Progress\n.*?\n", re.DOTALL)
    if "## 📊 Progress" in updated_content:
        updated_content = progress_pattern.sub(f"## 📊 Progress\n{progress_bar}\n\n", updated_content)
    else:
        updated_content = updated_content.replace(
            "## 🎯 Goal",
            f"## 📊 Progress\n{progress_bar}\n\n## 🎯 Goal"
        )

    # Save README
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✅ README.md updated! {solved_count}/{total_problems} solved ({percentage:.1f}%)")

if __name__ == "__main__":
    update_readme()
