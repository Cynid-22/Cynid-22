# Automated README Repository Updates (Topic-Based)

This system automatically discovers and displays your GitHub repositories based on topics - no manual configuration needed!

## 📁 Files Overview

- **`.github/workflows/update-readme.yml`** - GitHub Action that runs daily or manually
- **`.github/featured-repos.json`** - Configuration for username, topic, and theme
- **`.github/scripts/update_readme.py`** - Python script that fetches repos from GitHub API

## 🎯 How It Works

The script uses the GitHub API to:
1. Fetch all your repositories
2. Filter for repos with the `readme-profile` topic
3. Sort them by stars (most popular first)
4. Automatically update your README

## 🚀 Quick Start

### Step 1: Add the topic to your repositories

For each repo you want to feature:
1. Go to the repository on GitHub (e.g., `https://github.com/Cynid-22/TOTP-Authenticator`)
2. Click the **⚙️ gear icon** next to "About" in the right sidebar
3. In the "Topics" field, add: `readme-profile`
4. Click "Save changes"

**That's it!** The next time the workflow runs, your repo will appear in the README.

### Step 2: Trigger the update

You can either:
- **Wait for automatic update** - Runs daily at midnight UTC
- **Manual trigger**:
  1. Go to your repo's **Actions** tab
  2. Click **"Update README with Featured Repos"**
  3. Click **"Run workflow"** → **"Run workflow"**

## ⚙️ Configuration

Edit `.github/featured-repos.json` to customize:

```json
{
  "username": "Cynid-22",           // Your GitHub username
  "topic": "readme-profile",        // Topic to filter by
  "theme": {
    "name": "radical",              // GitHub stats card theme
    "bg_color": "1F222E",          // Background color
    "title_color": "E91E63",       // Title color
    "icon_color": "F8D866",        // Icon color
    "hide_border": true,           // Hide/show border
    "show_icons": false            // Show/hide icons
  }
}
```

## 📋 Examples

### Adding TOTP-Authenticator to Featured Repos

1. Visit: https://github.com/Cynid-22/TOTP-Authenticator
2. Click gear ⚙️ next to "About"
3. Add topic: `readme-profile`
4. Done! ✅

### Removing a Repo

1. Visit the repository
2. Click gear ⚙️ next to "About"  
3. Remove `readme-profile` from topics
4. Next update removes it from README

## 🔧 Advanced

### Testing Locally

Test the script before pushing:

```bash
python .github\scripts\update_readme.py
```

This will:
- Fetch your repos from GitHub API
- Show which repos have the `readme-profile` topic
- Update your local README.md

### Using a Different Topic

Want to use `featured` instead of `readme-profile`?

1. Edit `.github/featured-repos.json`
2. Change `"topic": "readme-profile"` to `"topic": "featured"`
3. Commit and push
4. Add the new topic to your repos

### Multiple Profiles

You can use different topics for different contexts:
- `readme-profile` - Main profile repos
- `readme-work` - Work-related projects
- `readme-learning` - Learning projects

Just change the `topic` in the config!

## 💡 Tips

- Repos are sorted by **star count** (highest first), then alphabetically
- The topic must be **exactly** `readme-profile` (case-sensitive)
- You can have multiple topics on a repo - only `readme-profile` matters for featuring
- If no repos have the topic, the script safely exits without changing README

## 🐛 Troubleshooting

**Q: I added the topic but my README hasn't updated**
- Wait for the daily run or manually trigger the workflow
- Check the Actions tab for any errors
- Verify the topic is spelled exactly: `readme-profile`

**Q: Can I change the order of repos?**
- Currently sorted by stars. To customize, edit the `fetch_repos_with_topic()` function in the Python script

**Q: Rate limits?**
- GitHub API allows 60 unauthenticated requests/hour
- Your workflow runs once daily, well within limits
- For authenticated requests (5000/hour), add a GitHub token to the workflow
