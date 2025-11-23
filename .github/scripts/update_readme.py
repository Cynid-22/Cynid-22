#!/usr/bin/env python3
"""
Auto-update README.md with featured repositories.
Fetches repositories with 'readme-profile' topic from GitHub API.
"""

import json
import re
import urllib.request
import urllib.error
from pathlib import Path


def load_config():
    """Load the featured repositories configuration."""
    config_path = Path('.github/featured-repos.json')
    with open(config_path, 'r') as f:
        return json.load(f)


def fetch_repos_with_topic(username, topic, repo_order=None):
    """
    Fetch repositories for a user that have a specific topic.
    Returns list of repos sorted by manual order (if provided), then by stars.
    """
    # GitHub API endpoint for user repositories
    api_url = f'https://api.github.com/users/{username}/repos?per_page=100&sort=updated'
    
    try:
        # Make request to GitHub API
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        with urllib.request.urlopen(req) as response:
            repos = json.loads(response.read().decode())
        
        # Filter repos that have the specified topic
        featured_repos = []
        for repo in repos:
            if topic in repo.get('topics', []):
                featured_repos.append({
                    'name': repo['name'],
                    'stars': repo['stargazers_count'],
                    'updated': repo['updated_at']
                })
        
        # Sort based on manual order if provided, otherwise by stars
        if repo_order:
            # Create a dict for easy lookup
            repo_dict = {repo['name']: repo for repo in featured_repos}
            
            # First, add repos in the specified order
            sorted_repos = []
            for repo_name in repo_order:
                if repo_name in repo_dict:
                    sorted_repos.append(repo_dict[repo_name])
            
            # Then add any remaining repos (not in manual order) sorted by stars
            remaining_repos = [repo for repo in featured_repos if repo['name'] not in repo_order]
            remaining_repos.sort(key=lambda x: (-x['stars'], x['name']))
            sorted_repos.extend(remaining_repos)
            
            featured_repos = sorted_repos
        else:
            # Default: Sort by stars (descending), then by name
            featured_repos.sort(key=lambda x: (-x['stars'], x['name']))
        
        return [repo['name'] for repo in featured_repos]
        
    except urllib.error.HTTPError as e:
        print(f"Error fetching repos from GitHub API: {e}")
        print("Falling back to empty list")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []



def generate_repo_card(username, repo_name, theme):
    """Generate HTML for a single repository card."""
    params = [
        f"username={username}",
        f"repo={repo_name}",
        f"theme={theme['name']}",
        f"bg_color={theme['bg_color']}",
        f"title_color={theme['title_color']}",
        f"icon_color={theme['icon_color']}"
    ]
    
    if theme.get('hide_border', False):
        params.append('hide_border=true')
    
    if not theme.get('show_icons', True):
        params.append('show_icons=false')
    
    query_string = '&'.join(params)
    
    return f'''    <a href="https://github.com/{username}/{repo_name}">
        <img width="278" src="https://denvercoder1-github-readme-stats.vercel.app/api/pin/?{query_string}" alt="{repo_name}">
    </a>'''


def update_readme():
    """Update README.md with featured repositories."""
    # Load configuration
    config = load_config()
    theme = config['theme']
    username = config.get('username', 'Cynid-22')
    topic = config.get('topic', 'readme-profile')
    repo_order = config.get('repo_order', None)  # Optional manual ordering
    
    print(f"Fetching repos for user '{username}' with topic '{topic}'...")
    
    # Fetch repositories with the specified topic from GitHub API
    repos = fetch_repos_with_topic(username, topic, repo_order)
    
    if not repos:
        print(f"No repositories found with topic '{topic}'")
        return
    
    print(f"Found {len(repos)} repo(s): {', '.join(repos)}")
    
    # Generate repository cards
    repo_cards = []
    for repo in repos:
        repo_cards.append(generate_repo_card(username, repo, theme))
    
    # Create the new featured projects section
    featured_section = f'''<details open>
  <summary><h2>📘 My Top Open Source Projects</h2></summary>

  <p align="left">
{chr(10).join(repo_cards)}
  </p>

  <a href="https://github.com/{username}?tab=repositories&sort=stargazers"><img alt="All Repositories" title="All Repositories" src="https://custom-icon-badges.demolab.com/badge/-Click%20Here%20For%20All%20My%20Repos-1F222E?style=for-the-badge&logoColor=white&logo=repo"/></a>
</details>'''
    
    # Read current README
    readme_path = Path('README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the entire featured projects section
    pattern = r'<details open>[\s\S]*?<summary><h2>📘 My Top Open Source Projects</h2></summary>[\s\S]*?</details>'
    
    # Replace the section
    new_content = re.sub(pattern, featured_section, content)
    
    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[SUCCESS] Updated README with {len(repos)} featured repositories")


if __name__ == '__main__':
    update_readme()

