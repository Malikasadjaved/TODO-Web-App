"""Command-line interface for Todo Application."""

from typing import Optional
from colorama import Fore, Style, init as colorama_init

from src.todo.models import Task, Priority, RecurrencePattern
from src.todo import commands, filters


# Initialize colorama for Windows support
colorama_init(autoreset=True)


def format_task(task: Task) -> str:
    """Format a task for display.

    Args:
        task: Task to format

    Returns:
        Formatted string representation of the task
    """
    # Status indicator
    status_icon = "[X]" if task.status == "complete" else "[ ]"

    # Priority indicator
    priority_map = {
        Priority.HIGH: f"{Fore.RED}[H]",
        Priority.MEDIUM: f"{Fore.YELLOW}[M]",
        Priority.LOW: f"{Fore.GREEN}[L]",
    }
    priority_str = priority_map.get(task.priority, "[?]")

    # Overdue indicator
    overdue_str = f"{Fore.RED}[!]" if task.is_overdue else ""

    # Task type
    task_type_str = f"[{task.task_type.value}]"

    # Tags
    tags_str = f" {Fore.CYAN}#{',#'.join(task.tags)}" if task.tags else ""

    # Due date
    due_date_str = ""
    if task.due_date:
        due_date_str = f" {Fore.MAGENTA}Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"

    # Recurrence
    recurrence_str = ""
    if task.recurrence:
        recurrence_str = f" {Fore.BLUE}[{task.recurrence.value}]"

    # Build output
    output = (
        f"{status_icon} {priority_str} "
        f"{Style.BRIGHT}#{task.id}{Style.RESET_ALL} "
        f"{task.title}"
        f"{overdue_str}"
        f"{tags_str}"
        f"{due_date_str}"
        f"{recurrence_str}"
        f" {Fore.WHITE}{task_type_str}"
    )

    if task.description:
        output += f"\n    {Fore.WHITE}{task.description}"

    return output


def display_menu() -> None:
    """Display the main menu."""
    print(f"\n{Style.BRIGHT}{'='*60}")
    print(f"{Fore.CYAN}{Style.BRIGHT}TODO APPLICATION - MAIN MENU")
    print(f"{Style.BRIGHT}{'='*60}{Style.RESET_ALL}\n")

    print(f"{Style.BRIGHT}PRIMARY TIER - Core Features{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}1.{Style.RESET_ALL} Add Task")
    print(f"  {Fore.GREEN}2.{Style.RESET_ALL} View All Tasks")
    print(f"  {Fore.GREEN}3.{Style.RESET_ALL} Update Task")
    print(f"  {Fore.GREEN}4.{Style.RESET_ALL} Delete Task")
    print(f"  {Fore.GREEN}5.{Style.RESET_ALL} Mark Task Complete")
    print(f"  {Fore.GREEN}6.{Style.RESET_ALL} Mark Task Incomplete")

    print(f"\n{Style.BRIGHT}INTERMEDIATE TIER - Organization{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}7.{Style.RESET_ALL} Search Tasks")
    print(f"  {Fore.YELLOW}8.{Style.RESET_ALL} Filter Tasks")
    print(f"  {Fore.YELLOW}9.{Style.RESET_ALL} Sort Tasks")

    print(f"\n{Style.BRIGHT}ADVANCED TIER - Automation{Style.RESET_ALL}")
    print(
        f"  {Fore.RED}10.{Style.RESET_ALL} Recurring Tasks "
        f"(Automatic - set via Add/Update)"
    )
    print(
        f"  {Fore.RED}11.{Style.RESET_ALL} Reminders "
        f"(Automatic - set via Add/Update)"
    )

    print(f"\n{Fore.WHITE}0. Exit{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{'='*60}{Style.RESET_ALL}\n")


def get_input(prompt: str, required: bool = True) -> Optional[str]:
    """Get user input with optional requirement.

    Args:
        prompt: Prompt to display
        required: If True, keep asking until non-empty input received

    Returns:
        User input string or None if not required and empty
    """
    while True:
        value = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
        if value or not required:
            return value if value else None
        print(f"{Fore.RED}This field is required. Please try again.{Style.RESET_ALL}")


def select_priority() -> Priority:
    """Display priority selection menu and get user choice.

    Returns:
        Priority enum value (defaults to MEDIUM)
    """
    print(f"\n{Fore.CYAN}Select Priority:{Style.RESET_ALL}")
    print("  1. HIGH")
    print("  2. MEDIUM (default)")
    print("  3. LOW")

    choice = get_input("Enter choice (1-3) [2]: ", required=False)

    # Default to MEDIUM if empty
    if not choice:
        return Priority.MEDIUM

    priority_map = {
        "1": Priority.HIGH,
        "2": Priority.MEDIUM,
        "3": Priority.LOW,
    }

    if choice in priority_map:
        return priority_map[choice]
    else:
        print(f"{Fore.RED}Invalid choice. Using MEDIUM.{Style.RESET_ALL}")
        return Priority.MEDIUM


def select_recurrence() -> Optional[RecurrencePattern]:
    """Display recurrence selection menu and get user choice.

    Returns:
        RecurrencePattern enum value or None for no recurrence
    """
    print(f"\n{Fore.CYAN}Select Recurrence (optional):{Style.RESET_ALL}")
    print("  1. DAILY")
    print("  2. WEEKLY")
    print("  3. BIWEEKLY")
    print("  4. MONTHLY")
    print("  5. YEARLY")
    print("  0. None (no recurrence)")

    choice = get_input("Enter choice (0-5) [0]: ", required=False)

    # Default to None if empty
    if not choice or choice == "0":
        return None

    recurrence_map = {
        "1": RecurrencePattern.DAILY,
        "2": RecurrencePattern.WEEKLY,
        "3": RecurrencePattern.BIWEEKLY,
        "4": RecurrencePattern.MONTHLY,
        "5": RecurrencePattern.YEARLY,
    }

    if choice in recurrence_map:
        return recurrence_map[choice]
    else:
        print(f"{Fore.RED}Invalid choice. Skipping recurrence.{Style.RESET_ALL}")
        return None


def add_task_interactive() -> None:
    """Interactive flow for adding a task."""
    print(f"\n{Style.BRIGHT}Add New Task{Style.RESET_ALL}")
    print(f"{'-'*60}")

    title = get_input("Title: ", required=True)
    description = get_input("Description (optional): ", required=False) or ""

    # Use selection menu for priority
    priority_enum = select_priority()
    priority = priority_enum.value

    tags = get_input("Tags (comma-separated, optional): ", required=False) or ""
    due_date = (
        get_input(
            "Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional): ", required=False
        )
        or ""
    )

    # Use selection menu for recurrence
    recurrence_enum = select_recurrence()
    recurrence = recurrence_enum.value if recurrence_enum else ""

    reminder = (
        get_input("Reminder (hours before due date, optional): ", required=False) or ""
    )

    result = commands.add_task_command(
        title=title,
        description=description,
        priority=priority,
        tags=tags,
        due_date_str=due_date,
        recurrence_str=recurrence,
        reminder_offset_str=reminder,
    )

    if result.success:
        print(f"\n{Fore.GREEN}[OK] {result.message}{Style.RESET_ALL}")
        if result.data:
            print(f"\n{format_task(result.data)}")
    else:
        print(f"\n{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")
        for error in result.errors:
            print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")


def view_all_tasks_interactive() -> None:
    """Interactive flow for viewing all tasks."""
    print(f"\n{Style.BRIGHT}All Tasks{Style.RESET_ALL}")
    print(f"{'-'*60}")

    result = commands.view_all_tasks_command()

    if result.success:
        if not result.data:
            print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        else:
            for task in result.data:
                print(f"\n{format_task(task)}")
            print(f"\n{Fore.GREEN}{result.message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")


def update_task_interactive() -> None:
    """Interactive flow for updating a task."""
    print(f"\n{Style.BRIGHT}Update Task{Style.RESET_ALL}")
    print(f"{'-'*60}")

    task_id_str = get_input("Task ID: ", required=True)
    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"{Fore.RED}Invalid task ID. Must be a number.{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}Leave blank to keep current value{Style.RESET_ALL}")

    updates = {}
    title = get_input("New Title (optional): ", required=False)
    if title:
        updates["title"] = title

    description = get_input("New Description (optional): ", required=False)
    if description:
        updates["description"] = description

    # Ask if user wants to update priority
    update_priority = get_input("Update Priority? (y/n) [n]: ", required=False)
    if update_priority and update_priority.lower() in ["y", "yes"]:
        priority_enum = select_priority()
        updates["priority"] = priority_enum.value

    tags = get_input("New Tags (comma-separated, optional): ", required=False)
    if tags:
        updates["tags"] = tags

    due_date = get_input(
        "New Due Date (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional): ", required=False
    )
    if due_date:
        updates["due_date"] = due_date

    # Ask if user wants to update recurrence
    update_recurrence = get_input("Update Recurrence? (y/n) [n]: ", required=False)
    if update_recurrence and update_recurrence.lower() in ["y", "yes"]:
        recurrence_enum = select_recurrence()
        if recurrence_enum:
            updates["recurrence"] = recurrence_enum.value

    if not updates:
        print(f"{Fore.YELLOW}No updates provided.{Style.RESET_ALL}")
        return

    result = commands.update_task_command(task_id, **updates)

    if result.success:
        print(f"\n{Fore.GREEN}[OK] {result.message}{Style.RESET_ALL}")
        if result.data:
            print(f"\n{format_task(result.data)}")
    else:
        print(f"\n{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")
        for error in result.errors:
            print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")


def delete_task_interactive() -> None:
    """Interactive flow for deleting a task."""
    print(f"\n{Style.BRIGHT}Delete Task{Style.RESET_ALL}")
    print(f"{'-'*60}")

    task_id_str = get_input("Task ID: ", required=True)
    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"{Fore.RED}Invalid task ID. Must be a number.{Style.RESET_ALL}")
        return

    # First call to get confirmation prompt
    result = commands.delete_task_command(task_id, confirmed=False)

    if not result.success:
        print(f"{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")
        return

    # Show task and ask for confirmation
    if result.data:
        print(f"\n{format_task(result.data)}")

    confirm = get_input(f"\n{result.message} (yes/no): ", required=True)

    if confirm.lower() not in ["yes", "y"]:
        print(f"{Fore.YELLOW}Deletion cancelled.{Style.RESET_ALL}")
        return

    # Confirmed - delete task
    result = commands.delete_task_command(task_id, confirmed=True)

    if result.success:
        print(f"\n{Fore.GREEN}[OK] {result.message}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")


def mark_complete_interactive() -> None:
    """Interactive flow for marking task as complete."""
    print(f"\n{Style.BRIGHT}Mark Task Complete{Style.RESET_ALL}")
    print(f"{'-'*60}")

    task_id_str = get_input("Task ID: ", required=True)
    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"{Fore.RED}Invalid task ID. Must be a number.{Style.RESET_ALL}")
        return

    result = commands.mark_complete_command(task_id)

    if result.success:
        print(f"\n{Fore.GREEN}[OK] {result.message}{Style.RESET_ALL}")
        if result.data:
            print(f"\n{format_task(result.data)}")
    else:
        print(f"\n{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")
        for error in result.errors:
            print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")


def mark_incomplete_interactive() -> None:
    """Interactive flow for marking task as incomplete."""
    print(f"\n{Style.BRIGHT}Mark Task Incomplete{Style.RESET_ALL}")
    print(f"{'-'*60}")

    task_id_str = get_input("Task ID: ", required=True)
    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"{Fore.RED}Invalid task ID. Must be a number.{Style.RESET_ALL}")
        return

    result = commands.mark_incomplete_command(task_id)

    if result.success:
        print(f"\n{Fore.GREEN}[OK] {result.message}{Style.RESET_ALL}")
        if result.data:
            print(f"\n{format_task(result.data)}")
    else:
        print(f"\n{Fore.RED}[ERROR] {result.message}{Style.RESET_ALL}")
        for error in result.errors:
            print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")


def search_tasks_interactive() -> None:
    """Interactive flow for searching tasks."""
    print(f"\n{Style.BRIGHT}Search Tasks{Style.RESET_ALL}")
    print(f"{'-'*60}")

    keyword = get_input("Search keyword: ", required=True)

    result = commands.view_all_tasks_command()
    if not result.success or not result.data:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return

    # Apply search filter
    filtered_tasks = filters.search_tasks(result.data, keyword)

    if not filtered_tasks:
        print(f"{Fore.YELLOW}No tasks match '{keyword}'.{Style.RESET_ALL}")
    else:
        result_count = len(filtered_tasks)
        print(
            f"\n{Style.BRIGHT}Search Results ({result_count} found):"
            f"{Style.RESET_ALL}"
        )
        for task in filtered_tasks:
            print(f"\n{format_task(task)}")


def filter_tasks_interactive() -> None:
    """Interactive flow for filtering tasks."""
    print(f"\n{Style.BRIGHT}Filter Tasks{Style.RESET_ALL}")
    print(f"{'-'*60}")

    # Get all tasks
    result = commands.view_all_tasks_command()
    if not result.success or not result.data:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return

    # Collect filter criteria
    print(f"{Fore.CYAN}Enter filter criteria (leave blank to skip):{Style.RESET_ALL}\n")

    status_input = get_input("Status (complete/incomplete): ", required=False)
    status = status_input if status_input in ["complete", "incomplete"] else None

    priority_input = get_input(
        "Priority (HIGH/MEDIUM/LOW, comma-separated): ", required=False
    )
    priorities = None
    if priority_input:
        priority_strs = [p.strip().upper() for p in priority_input.split(",")]
        priorities = []
        for p_str in priority_strs:
            try:
                priorities.append(Priority[p_str])
            except KeyError:
                pass

    tag_input = get_input("Tag: ", required=False)
    tag = tag_input if tag_input else None

    overdue_input = get_input("Show only overdue? (yes/no): ", required=False)
    overdue_only = overdue_input.lower() in ["yes", "y"] if overdue_input else False

    today_input = get_input("Show only due today? (yes/no): ", required=False)
    due_today_only = today_input.lower() in ["yes", "y"] if today_input else False

    week_input = get_input("Show only due this week? (yes/no): ", required=False)
    due_this_week_only = week_input.lower() in ["yes", "y"] if week_input else False

    # Apply filters
    filtered_tasks = filters.combine_filters(
        result.data,
        status=status,
        priorities=priorities,
        tag=tag,
        overdue_only=overdue_only,
        due_today_only=due_today_only,
        due_this_week_only=due_this_week_only,
    )

    # Display results
    filter_summary = filters.get_filter_summary(
        status=status,
        priorities=priorities,
        tag=tag,
        overdue_only=overdue_only,
        due_today_only=due_today_only,
        due_this_week_only=due_this_week_only,
    )

    print(f"\n{Style.BRIGHT}{filter_summary}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}Results: {len(filtered_tasks)} task(s){Style.RESET_ALL}\n")

    if not filtered_tasks:
        print(f"{Fore.YELLOW}No tasks match the filter criteria.{Style.RESET_ALL}")
    else:
        for task in filtered_tasks:
            print(f"\n{format_task(task)}")


def sort_tasks_interactive() -> None:
    """Interactive flow for sorting tasks."""
    print(f"\n{Style.BRIGHT}Sort Tasks{Style.RESET_ALL}")
    print(f"{'-'*60}")

    # Get all tasks
    result = commands.view_all_tasks_command()
    if not result.success or not result.data:
        print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
        return

    # Display sort options
    print(f"{Fore.CYAN}Sort by:{Style.RESET_ALL}")
    print("  1. Due Date (earliest first)")
    print("  2. Priority (HIGH → MEDIUM → LOW)")
    print("  3. Title (A-Z)")
    print("  4. Created Date (oldest first)")

    choice = get_input("\nSelect sort option (1-4): ", required=True)

    sort_map = {
        "1": ("due_date", filters.sort_by_due_date),
        "2": ("priority", filters.sort_by_priority),
        "3": ("title", filters.sort_by_title),
        "4": ("created_date", filters.sort_by_created_date),
    }

    if choice not in sort_map:
        print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        return

    sort_key, sort_func = sort_map[choice]
    sorted_tasks = sort_func(result.data)

    # Display sorted results
    sort_desc = filters.get_sort_description(sort_key)
    print(f"\n{Style.BRIGHT}Sorted by: {sort_desc}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{len(sorted_tasks)} task(s){Style.RESET_ALL}\n")

    for task in sorted_tasks:
        print(f"\n{format_task(task)}")


def run_cli() -> None:
    """Main CLI event loop."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Welcome to Todo Application!{Style.RESET_ALL}")

    while True:
        display_menu()
        choice = get_input("Enter your choice: ", required=True)

        if choice == "0":
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
            break
        elif choice == "1":
            add_task_interactive()
        elif choice == "2":
            view_all_tasks_interactive()
        elif choice == "3":
            update_task_interactive()
        elif choice == "4":
            delete_task_interactive()
        elif choice == "5":
            mark_complete_interactive()
        elif choice == "6":
            mark_incomplete_interactive()
        elif choice == "7":
            search_tasks_interactive()
        elif choice == "8":
            filter_tasks_interactive()
        elif choice == "9":
            sort_tasks_interactive()
        elif choice == "10":
            print(f"\n{Fore.CYAN}Recurring Tasks:{Style.RESET_ALL}")
            print(
                "Recurring tasks are created automatically when you "
                "mark a recurring task complete."
            )
            print("To create a recurring task:")
            print("  1. Select 'Add Task' or 'Update Task'")
            print("  2. Set a recurrence pattern (DAILY/WEEKLY/MONTHLY/YEARLY)")
            print("  3. When you mark it complete, a new instance is auto-created")
        elif choice == "11":
            print(f"\n{Fore.CYAN}Reminders:{Style.RESET_ALL}")
            print("Reminders are set when creating or updating a task.")
            print("To set a reminder:")
            print("  1. Select 'Add Task' or 'Update Task'")
            print("  2. Set a due_date")
            print("  3. Set reminder_offset (hours before due date)")
            print("Reminders will trigger based on your settings.")
        else:
            print(f"\n{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

        input(f"\n{Fore.WHITE}Press Enter to continue...{Style.RESET_ALL}")
