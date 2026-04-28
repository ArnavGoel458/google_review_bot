#!/bin/bash

# Exit on any internal failure
set -e

echo "======================================"
echo "      Google Business Review Bot      "
echo "======================================"
echo ""

echo "[Step 1] Checking Authentication..."
python3 login.py
echo ""

echo "[Step 2] Fetching Business Profile Information..."
python3 get_business.py
echo ""

echo "--------------------------------------"
echo "Please look at the Account Profile and Location details listed above."
echo "The bot will automatically reply to any un-replied 4-star and 5-star reviews for this specific business profile."
echo "--------------------------------------"
echo -n "Is the business profile correct, and would you like to proceed? [Y/n]: "
read -r response

# If user types nothing (hits enter) or types y/Y/yes/YES, proceed
if [[ "$response" =~ ^([yY][eE][sS]|[yY]|"")$ ]]; then
    echo ""
    echo "[Step 3] Executing Auto-Reply Script..."
    python3 reply_to_reviews.py
    echo ""
    echo "======================================"
    echo "        Bot Execution Complete!       "
    echo "======================================"
else
    echo ""
    echo "Operation aborted by user."
    exit 0
fi
