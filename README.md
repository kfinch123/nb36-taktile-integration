# nb36-taktile-integration

This project is an integration between GitHub and Taktile by automatically updating code nodes in Taktile decision flows with Python script changes. 
The sync ensures that changes made to the scripts in this GitHub repository (scripts folder) are reflected in the code nodes in Taktile's decision graphs.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kfinch123/nb36-taktile-integration.git
   ```

2. Set up your Taktile API key as a GitHub Secret (`TAKTILE_API_KEY`) for the GitHub Actions workflow.

## Usage

When you make changes to any Python script in the `scripts/` directory and push your changes to the `main` branch, this will trigger the GitHub Actions workflow, which automatically synchronises the changes to Taktile's decision flows by triggering the github_taktile_sync.py script.

1. Modify a script in the `scripts/` folder.
2. Commit and push the change, e.g.:
   ```bash
   git add .
   git commit -m "Update Multiply script"
   git push origin main
   ```

3. The workflow will automatically update the corresponding decision node in Taktile based on the name of the script.

4. The progress and success/error status of the Github Actions workflow and github_taktile_sync.py script can be viewed in the "Actions" tab

## Taktile API Integration

This repository integrates with the Taktile API to synchronise Python script changes with Taktile's decision graphs.

The main steps in the integration are:
1. The GitHub Actions workflow regonises and fetches changed Python scripts.
2. It identifies the corresponding decision node in Taktile based on the script name.
3. The script content is patched into the corresponding decision graph in Taktile.

The Taktile API key is stored securely in GitHub Secrets under `TAKTILE_API_KEY`, and is used to authenticate API requests to update the decision graphs.

The following API endpoints are used:
- `List Decision Flows`: Fetches the list of flows for the company.
- `Get Decision Graph`: Fetches the current decision graph for a flow.
- `Patch Decision Graph`: Updates the decision node with the new Python script content.

## GitHub Actions Workflow

The repository is set up with a GitHub Actions workflow which triggers when Python scripts in the `scripts/` folder are changed.

The workflow performs the following steps:
1. **Checkout Repository**: Clones the repository.
2. **Set up Python**: Sets up the Python environment.
3. **Install dependencies**: Installs the required Python libraries, such as `requests`.
4. **Get Changed Files**: Uses the `changed-files` action to determine which Python files were modified.
5. **Run the Python Script**: Executes `github_taktile_sync.py`, passing the changed files as arguments. This script updates the corresponding decision nodes in Taktile based on the matching script names.
