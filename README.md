# Google Business Review Auto-Reply Bot

This project provides a suite of automated tools that interact with the Google Business Profile APIs. It securely fetches recent reviews for a designated business location and automatically posts formatted replies to positive reviews (4 or 5 stars) that have not yet received a response.

## Architecture Overview

The codebase is split into core reusable modules and simple, top-level execution scripts:
- **`auth.py`**: Handles token management, caching, and the OAuth2 browser flow via `credentials.json`.
- **`api.py`**: Wraps the Google Business API logic. It connects to the `mybusinessaccountmanagement` and `mybusinessbusinessinformation` services, and makes raw requests to fetch reviews and post replies. *(Note: The standalone v4 version of the Business Profile API Python client has been deprecated, requiring raw request handling for those specific endpoints).*
- **`config.py`**: Acts as a central hub to load environment variables, string templates, and secure logging settings.
- **`templates.yaml`**: The customizable string template used when dynamically generating replies to newly found reviews.

## Prerequisites

Before utilizing these scripts, you must configure an internal application in the Google Cloud Console and generate OAuth 2.0 credentials. 

Please refer to the official Google documentation to correctly configure your project:
🔗 **[Google Business Profile APIs: Basic Setup Guide](https://developers.google.com/my-business/content/basic-setup)**

Once you have completed the basic setup, download your OAuth client secrets file and place it in the root of this project (e.g., `credentials.json`).

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed. It is recommended to create a virtual environment, then install the necessary packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
You must create a `.env` file in the root directory containing your API identifiers. 

**Security Notice for GitHub**: Files such as `.env`, `token.json`, and `credentials.json` contain highly sensitive authentication data. A `.gitignore` file has been proactively configured in this repository to prevent these files from being accidentally pushed to your version control.

```dotenv
# .env file
ACCOUNT_ID = your_account_id_here
LOCATION_ID = your_location_id_here
CREDENTIALS_FILE = credentials.json
```

### 3. Customize Reply Templates
The automated reply sent to reviewers is driven by the configuration inside `templates.yaml`. You may use the `{reviewer_name}` string variable to dynamically substitute the customer's display name into the auto-reply text.

## Usage

### The Easy Way (Automated Runner)
We provide a fully automated wrapper script that handles the login, securely retrieves the business name (so you can verify it without leaking sensitive IDs), and then safely prompts you to proceed before executing the auto-reply process.

```bash
chmod +x run_bot.sh
./run_bot.sh
```

### The Manual Way (Step-by-Step)
You can directly invoke the underlying Python scripts if you require granular control over the execution pipeline:

1. **Initial Login & Setup**: 
   ```bash
   python scripts/login.py
   ```
   This opens your web browser to securely authenticate the bot. After logging in, a temporary `token.json` file will be generated and saved relative to the script.

2. **Test Account Access (Optional)**: 
   ```bash
   python scripts/get_business.py
   ```
   Checks your basic credential scope and visually confirms the target Account and Location names using safe, masked logging.

3. **Get Current Reviews (Optional)**: 
   ```bash
   python scripts/get_reviews.py
   ```
   A utility script to manually fetch and print the raw list of reviews for the configured location.

4. **Execute Auto-Replies**: 
   ```bash
   python scripts/reply_to_reviews.py
   ```
   This initiates the core logic: it scans all recent reviews and posts your customized message from `templates.yaml` to any un-replied 4-star and 5-star reviews. It intentionally incorporates a 1-second delay between posting replies to respect Google's API rate limits.
