import csv
from pathlib import Path

DATA_FILE = Path("students.csv")


def load_students():
    """Load student records from the CSV file."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def calculate_percentage(marks):
    """Return the percentage for a list of marks out of 100."""
    if not marks:
        return 0.0
    return sum(marks) / len(marks)


def get_grade(percentage):
    """Convert a percentage into a simple grade."""
    if percentage >= 90:
        return "A"
    if percentage >= 80:
        return "B"
    if percentage >= 70:
        return "C"
    if percentage >= 60:
        return "D"
    return "F"


def show_report(students):
    """Print each student's percentage and grade."""
    if not students:
        print("No student records found.")
        return

    print("\nSTUDENT PERFORMANCE REPORT")
    print("-" * 58)
    print(f"{'Name':<20}{'Percentage':>14}{'Grade':>12}")
    print("-" * 58)

    results = []
    for student in students:
        try:
            marks = [
                float(student["maths"]),
                float(student["science"]),
                float(student["english"]),
            ]
        except (KeyError, ValueError):
            print(f"Skipping invalid record: {student}")
            continue

        percentage = calculate_percentage(marks)
        grade = get_grade(percentage)
        results.append((student["name"], percentage, grade))
        print(f"{student['name']:<20}{percentage:>13.1f}%{grade:>12}")

    if results:
        best_student = max(results, key=lambda result: result[1])
        class_average = sum(result[1] for result in results) / len(results)
        print("-" * 58)
        print(f"Class average: {class_average:.1f}%")
        print(
            f"Top performer: {best_student[0]} "
            f"({best_student[1]:.1f}%)"
        )


def add_student():
    """Ask for a student's marks and append the record to the CSV file."""
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    marks = []
    for subject in ("maths", "science", "english"):
        while True:
            try:
                mark = float(input(f"{subject.title()} marks (0-100): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                print("Please enter a mark between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

    file_exists = DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "maths", "science", "english"]
        )
        if not file_exists or DATA_FILE.stat().st_size == 0:
            writer.writeheader()
        writer.writerow({
            "name": name,
            "maths": marks[0],
            "science": marks[1],
            "english": marks[2],
        })

    print(f"Added record for {name}.")


def main():
    """Run the command-line menu."""
    while True:
        print("\nStudent Performance Analyzer")
        print("1. View report")
        print("2. Add student")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_report(load_students())
        elif choice == "2":
            add_student()
        elif choice == "3":
            print("Good luck with your studies!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
