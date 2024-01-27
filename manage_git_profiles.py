import subprocess
import sys
import os

def install_required_packages():
    try:
        import pyfiglet
    except ImportError:
        print("Installing required package 'pyfiglet'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyfiglet"])

def display_banner():
    import pyfiglet
    banner = pyfiglet.figlet_format("Shri: Manage Your Git Profiles")
    print(banner)

def print_divider(title=None):
    if title:
        print("\n" + "-" * 10 + f" {title} " + "-" * 10 + "\n")
    else:
        print("\n" + "-" * 30 + "\n")

def get_all_git_profiles():
    profiles = []
    try:
        global_config = subprocess.check_output(["git", "config", "--global", "--list"], encoding="utf-8")
        name = email = None
        for line in global_config.splitlines():
            if 'user.name=' in line:
                name = line.split('=')[1].strip()
            elif 'user.email=' in line:
                email = line.split('=')[1].strip()
        if name or email:
            profiles.append((name, email))
    except subprocess.CalledProcessError:
        print("No global git profiles found.")
    return profiles

def get_git_profiles_in_directory(directory):
    print_divider("Local Repository Search")
    print(f"Searching for Git repositories in {directory}...")
    profiles = []
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs[:] = []
            config_path = os.path.join(root, '.git', 'config')
            try:
                with open(config_path, 'r') as file:
                    name = email = None
                    for line in file:
                        if 'user.email' in line:
                            email = line.split('=')[1].strip()
                        elif 'user.name' in line:
                            name = line.split('=')[1].strip()
                    if name or email:
                        profiles.append((name, email))
            except FileNotFoundError:
                continue
    return profiles

def get_git_profiles_in_directory(directory):
    print_divider("Local Repository Search")
    print(f"Searching for Git repositories in {directory}...")
    profiles = []
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs[:] = []
            git_dir = os.path.join(root, '.git')
            try:
                name = subprocess.check_output(["git", "config", "--file", os.path.join(git_dir, "config"), "user.name"], encoding="utf-8").strip()
            except subprocess.CalledProcessError:
                name = None
            try:
                email = subprocess.check_output(["git", "config", "--file", os.path.join(git_dir, "config"), "user.email"], encoding="utf-8").strip()
            except subprocess.CalledProcessError:
                email = None
            if name or email:
                profiles.append((name, email, root))  # Include repository path
    return profiles


def add_git_profile():
    name = input("Enter the new Git username: ")
    email = input("Enter the new Git email: ")

    scope = input("Add this profile globally or locally? Enter 'global' or 'local': ").lower()
    if scope == 'global':
        subprocess.run(["git", "config", "--global", "user.name", name])
        subprocess.run(["git", "config", "--global", "user.email", email])
        print("New global profile added.")
    elif scope == 'local':
        repo_path = input("Enter the full path to the local repository: ")
        git_config_path = os.path.join(repo_path, ".git", "config")

        # Check if .git/config exists, if not, initialize the repository
        if not os.path.exists(git_config_path):
            print("Initializing new Git repository...")
            subprocess.run(["git", "-C", repo_path, "init"])

        subprocess.run(["git", "-C", repo_path, "config", "user.name", name])
        subprocess.run(["git", "-C", repo_path, "config", "user.email", email])
        print("New local profile added to the repository.")
    else:
        print("Invalid option. Profile not added.")


def delete_git_profile(global_profiles, local_profiles):
    print_divider("Delete Profile")

    scope = input("Do you want to delete a 'global' or 'local' profile? Enter 'global' or 'local': ").lower()

    if scope == 'global':
        if not global_profiles:
            print("No global profiles available to delete.")
            return

        for i, (name, email) in enumerate(global_profiles, 1):
            print(f"{i}. Name: {name}, Email: {email}")

        choice = int(input("Enter the number of the global profile you want to delete: ")) - 1
        name, email = global_profiles[choice]

        if name:
            subprocess.run(["git", "config", "--global", "--unset", "user.name"])
        if email:
            subprocess.run(["git", "config", "--global", "--unset", "user.email"])

        print(f"Global profile '{name or ''}, {email or ''}' deleted.")

    elif scope == 'local':
        if not local_profiles:
            print("No local profiles available to delete.")
            return

        for i, (name, email, repo_path) in enumerate(local_profiles, 1):
            print(f"{i}. Name: {name}, Email: {email}, Repository: {repo_path}")

        choice = int(input("Enter the number of the local profile you want to delete: ")) - 1
        name, email, repo_path = local_profiles[choice]

        confirmation = input(f"Are you sure you want to delete the profile '{name or ''}, {email or ''}' in repository {repo_path}? (yes/no): ")
        if confirmation.lower() == 'yes':
            if name:
                subprocess.run(["git", "-C", repo_path, "config", "--unset", "user.name"])
            if email:
                subprocess.run(["git", "-C", repo_path, "config", "--unset", "user.email"])

            print(f"Local profile '{name or ''}, {email or ''}' deleted in repository {repo_path}.")
        else:
            print("Profile deletion canceled.")

    else:
        print("Invalid option. No profile deleted.")

def show_updated_profiles():
    print_divider("Updated Git Profiles")
    global_profiles = get_all_git_profiles()
    for profile in global_profiles:
        print(f" - {profile}")

def show_combined_profiles(profiles):
    name = None
    email = None
    for profile in profiles:
        if profile.startswith('user.name'):
            name = profile.split('=')[1].strip()
        elif profile.startswith('user.email'):
            email = profile.split('=')[1].strip()

    if name and email:
        print(f" - Name: {name}, Email: {email}")
    elif name:
        print(f" - Name: {name}")
    elif email:
        print(f" - Email: {email}")

def main():
    display_banner()
    search_directory = input("Enter the directory path to search for Git repositories: ")
    local_profiles = get_git_profiles_in_directory(search_directory)
    global_profiles = get_all_git_profiles()

    while True:  # Start of the loop
        print_divider("Global Git Profiles")
        global_profiles = get_all_git_profiles()
        for name, email in global_profiles:
            print(f" - Name: {name}, Email: {email}")

        print_divider("Local Git Profiles")
        local_profiles = get_git_profiles_in_directory(search_directory)
        for name, email, repo_path in local_profiles: 
            print(f" - Name: {name}, Email: {email}, Repository: {repo_path}")

        action = input("\nDo you want to 'add' a new profile, 'delete' an existing one, or 'exit' the script? (add/delete/exit): ")

        if action.lower() == 'add':
            add_git_profile()
        elif action.lower() == 'delete':
            delete_git_profile(global_profiles, local_profiles)
        elif action.lower() == 'exit':
            print("Exiting the script.")
            break  # Exit the loop
        else:
            print("Invalid action. Please choose a valid option.")

if __name__ == "__main__":
    install_required_packages()
    main()
