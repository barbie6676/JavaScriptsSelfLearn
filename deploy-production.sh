#!/bin/bash
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
current_branch="$(git branch | grep \* | cut -d ' ' -f2)"
echo -e "This will deploy the local contents of ${YELLOW}$current_branch${NC} to ${RED}release-production${NC}."
read -p "Proceed? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
echo "Attempting to delete branch release-production"
git branch -D release-production
git checkout -b release-production
git push origin release-production -f
git checkout $current_branch