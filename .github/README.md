# GitHub Actions Workflows

This directory contains GitHub Actions workflow configurations for automated testing and CI/CD.

## Workflows

### `test.yml` - Automated Testing

Runs on every push and pull request to `main`, `master`, or `develop` branches.

**Jobs:**
- **Test** - Run unit tests across Python 3.9-3.13
- **Lint** - Code quality checks (flake8, black, isort)
- **Security** - Security scanning (bandit, safety)

**Features:**
- ✅ Multi-Python version testing (3.9, 3.10, 3.11, 3.12, 3.13)
- ✅ Chrome + ChromeDriver setup
- ✅ Headless Selenium testing
- ✅ Graceful degradation (works without Forebet in CI/CD)
- ✅ Automatic test reports
- ✅ Security vulnerability scanning

## Testing Locally

Before pushing to GitHub, run local CI/CD simulation:

```bash
python test_github_actions_simulation.py
```

This will run the same tests as GitHub Actions.

## Important Notes

### Forebet in CI/CD

⚠️ **Forebet does NOT work in GitHub Actions** (requires visible browser).

The application uses graceful degradation:
- **Without `--use-forebet`**: Works perfectly in CI/CD (headless mode)
- **With `--use-forebet`**: Flag is ignored in CI/CD, app continues without Forebet

### Manual Trigger

You can manually trigger the workflow:
1. Go to Actions tab in GitHub
2. Select "Tests" workflow
3. Click "Run workflow"

## Status Badge

Add to README.md:

```markdown
![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Tests/badge.svg)
```

## See Also

- [GITHUB_ACTIONS_GUIDE.md](../GITHUB_ACTIONS_GUIDE.md) - Detailed CI/CD documentation
- [test_ci_cd.py](../test_ci_cd.py) - CI/CD compatible unit tests
- [test_github_actions_simulation.py](../test_github_actions_simulation.py) - Local CI/CD simulation
