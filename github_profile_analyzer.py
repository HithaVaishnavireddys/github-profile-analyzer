import requests


def get_github_profile(username):
    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 404:
            print("GitHub user not found.")
            return None

        elif response.status_code == 403:
            print("GitHub API rate limit reached or access denied.")
            return None

        else:
            print("Unable to fetch profile.")
            print("Status Code:", response.status_code)
            return None

    except requests.exceptions.RequestException as error:
        print("Network error:", error)
        return None


def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"

    params = {
        "per_page": 100,
        "sort": "updated"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 404:
            print("Repositories not found.")
            return []

        elif response.status_code == 403:
            print("GitHub API rate limit reached or access denied.")
            return []

        else:
            print("Unable to fetch repositories.")
            print("Status Code:", response.status_code)
            return []

    except requests.exceptions.RequestException as error:
        print("Network error:", error)
        return []


def classify_profile(public_repos):
    if public_repos >= 20:
        return "Highly Active Developer"
    elif public_repos >= 10:
        return "Active Developer"
    elif public_repos >= 5:
        return "Growing Developer"
    else:
        return "Beginner Developer"


def analyze_repositories(repositories):
    repo_names = []
    languages = []
    total_stars = 0
    total_forks = 0

    for repo in repositories:
        repo_names.append(repo.get("name", "Unknown"))

        language = repo.get("language")

        if language:
            languages.append(language)

        total_stars += repo.get("stargazers_count", 0)
        total_forks += repo.get("forks_count", 0)

    unique_languages = set(languages)

    language_count = {}

    for language in languages:
        if language in language_count:
            language_count[language] += 1
        else:
            language_count[language] = 1

    most_used_language = None

    if language_count:
        most_used_language = max(
            language_count,
            key=language_count.get
        )

    most_starred_repository = None

    if repositories:
        most_starred_repository = repositories[0]

        for repo in repositories:
            if repo.get("stargazers_count", 0) > most_starred_repository.get("stargazers_count", 0):
                most_starred_repository = repo

    average_stars = 0

    if len(repositories) > 0:
        average_stars = total_stars / len(repositories)

    return {
        "repo_names": repo_names,
        "total_repos_analyzed": len(repositories),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "average_stars": average_stars,
        "unique_languages": unique_languages,
        "language_count": language_count,
        "most_used_language": most_used_language,
        "most_starred_repository": most_starred_repository
    }


def find_repositories_by_language(repositories, target_language):
    matches = []

    for repo in repositories:
        language = repo.get("language")

        if language and language.lower() == target_language.lower():
            matches.append(repo.get("name"))

    return matches


def search_repository(repositories, repository_name):
    for repo in repositories:
        if repo.get("name", "").lower() == repository_name.lower():
            return repo

    return None


def display_profile(profile, developer_level):
    print("\n" + "=" * 55)
    print("              GITHUB PROFILE")
    print("=" * 55)

    print("Name             :", profile.get("name") or "Not provided")
    print("Username         :", profile.get("login"))
    print("Bio              :", profile.get("bio") or "Not provided")
    print("Location         :", profile.get("location") or "Not provided")
    print("Company          :", profile.get("company") or "Not provided")
    print("Public Repos     :", profile.get("public_repos"))
    print("Followers        :", profile.get("followers"))
    print("Following        :", profile.get("following"))
    print("Profile Level    :", developer_level)
    print("Profile URL      :", profile.get("html_url"))


def display_repository_report(repositories, analysis):
    print("\n" + "=" * 55)
    print("              REPOSITORY ANALYSIS")
    print("=" * 55)

    if not repositories:
        print("No public repositories found.")
        return

    for index, repo in enumerate(repositories[:10], start=1):
        name = repo.get("name", "Unknown")
        language = repo.get("language") or "Not specified"
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)

        print(f"\n{index}. {name}")
        print("   Language :", language)
        print("   Stars    :", stars)
        print("   Forks    :", forks)

    print("\n" + "-" * 55)
    print("SUMMARY")
    print("-" * 55)

    print("Repositories analyzed :", analysis["total_repos_analyzed"])
    print("Total stars           :", analysis["total_stars"])
    print("Total forks           :", analysis["total_forks"])
    print("Average stars         :", round(analysis["average_stars"], 2))
    print("Unique languages      :", analysis["unique_languages"])
    print(
        "Most used language    :",
        analysis["most_used_language"] or "Not available"
    )

    most_starred = analysis["most_starred_repository"]

    if most_starred:
        print(
            "Most starred repo     :",
            most_starred.get("name")
        )
        print(
            "Most starred count    :",
            most_starred.get("stargazers_count", 0)
        )


def main():
    print("=" * 55)
    print("           GITHUB PROFILE ANALYZER")
    print("=" * 55)

    username = input("Enter a GitHub username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    print("\nFetching GitHub data...")

    profile = get_github_profile(username)

    if profile is None:
        return

    repositories = get_repositories(username)

    analysis = analyze_repositories(repositories)

    developer_level = classify_profile(
        profile.get("public_repos", 0)
    )

    display_profile(
        profile,
        developer_level
    )

    display_repository_report(
        repositories,
        analysis
    )

    print("\n" + "=" * 55)
    print("              REPOSITORY SEARCH")
    print("=" * 55)

    repository_name = input(
        "Enter repository name to search (or press Enter to skip): "
    ).strip()

    if repository_name:
        found_repo = search_repository(
            repositories,
            repository_name
        )

        if found_repo:
            print("Repository found!")
            print("Name     :", found_repo.get("name"))
            print("Language :", found_repo.get("language") or "Not specified")
            print("Stars    :", found_repo.get("stargazers_count", 0))
            print("Forks    :", found_repo.get("forks_count", 0))
            print("URL      :", found_repo.get("html_url"))
        else:
            print("Repository not found in the downloaded repositories.")

    print("\n" + "=" * 55)
    print("              LANGUAGE SEARCH")
    print("=" * 55)

    target_language = input(
        "Enter a programming language to search (or press Enter to skip): "
    ).strip()

    if target_language:
        language_repositories = find_repositories_by_language(
            repositories,
            target_language
        )

        if language_repositories:
            print(
                f"\nRepositories using {target_language}:"
            )

            for repo_name in language_repositories:
                print("-", repo_name)
        else:
            print(
                f"No repositories found using {target_language}."
            )

    print("\n" + "=" * 55)
    print("Analysis completed successfully.")
    print("=" * 55)


main()