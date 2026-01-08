#!/bin/bash

# Code Review Agent - Manual Implementation
# This script mimics the behavior of an Augment subagent for code review

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/code-review-prompt.txt"

# Function to print colored output
print_header() {
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC}          ${BLUE}🤖 AI Code Review Agent${NC}                      ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_error() {
    echo -e "${RED}❌ Error: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [MESSAGE]

Options:
    -h, --help              Show this help message
    -a, --all               Review all changes (not just staged)
    -f, --files PATTERN     Review specific files matching pattern
    -c, --commit HASH       Review specific commit
    --focus AREA            Focus on specific area (security, performance, bugs)
    --staged                Review only staged changes (default)
    --diff                  Show diff before review

Examples:
    $(basename "$0")                                    # Review staged changes
    $(basename "$0") "Focus on security issues"         # Review with custom message
    $(basename "$0") --all                              # Review all uncommitted changes
    $(basename "$0") --commit abc123                    # Review specific commit
    $(basename "$0") --files "*.js"                     # Review only JS files
    $(basename "$0") --focus security                   # Focus on security

EOF
}

# Parse command line arguments
MODE="staged"
CUSTOM_MESSAGE=""
FILE_PATTERN=""
COMMIT_HASH=""
FOCUS_AREA=""
SHOW_DIFF=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -a|--all)
            MODE="all"
            shift
            ;;
        -f|--files)
            FILE_PATTERN="$2"
            shift 2
            ;;
        -c|--commit)
            COMMIT_HASH="$2"
            MODE="commit"
            shift 2
            ;;
        --focus)
            FOCUS_AREA="$2"
            shift 2
            ;;
        --staged)
            MODE="staged"
            shift
            ;;
        --diff)
            SHOW_DIFF=true
            shift
            ;;
        *)
            CUSTOM_MESSAGE="$1"
            shift
            ;;
    esac
done

# Check if auggie is installed - try multiple locations
AUGGIE_CMD=""
NODE_CMD=""

# Find the correct Node.js version (v20+)
if [ -f "$HOME/.nvm/versions/node/v22.21.1/bin/node" ]; then
    NODE_CMD="$HOME/.nvm/versions/node/v22.21.1/bin/node"
    AUGGIE_CMD="$HOME/.nvm/versions/node/v22.21.1/lib/node_modules/@augmentcode/auggie/augment.mjs"
elif command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 20 ]; then
        NODE_CMD="node"
        # Try to find auggie
        if command -v auggie &> /dev/null; then
            AUGGIE_CMD="auggie"
        fi
    fi
fi

# If still not found, show error
if [ -z "$NODE_CMD" ] || [ -z "$AUGGIE_CMD" ]; then
    print_error "auggie is not installed or Node.js v20+ is not available"
    echo ""
    echo "Requirements:"
    echo "  - Node.js v20 or higher"
    echo "  - auggie installed: npm install -g auggie"
    echo ""
    echo "Current Node version: $(node --version 2>/dev/null || echo 'not found')"
    echo ""
    echo "If using nvm, try:"
    echo "  nvm use 22"
    echo "  npm install -g auggie"
    exit 1
fi

print_info "Using Node: $NODE_CMD"
print_info "Using auggie: $AUGGIE_CMD"

# Check if prompt file exists
if [ ! -f "$PROMPT_FILE" ]; then
    print_error "Prompt file not found: $PROMPT_FILE"
    exit 1
fi

# Print header
print_header

# Get the changes based on mode
CHANGES=""
CHANGES_SUMMARY=""

case $MODE in
    staged)
        print_info "Reviewing staged changes..."
        STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")

        if [ -z "$STAGED_FILES" ]; then
            print_warning "No staged changes found."
            echo "Please stage files with: git add <files>"
            exit 1
        fi

        CHANGES_SUMMARY="Staged files:\n$STAGED_FILES"
        CHANGES=$(git diff --cached 2>/dev/null || echo "")
        ;;

    all)
        print_info "Reviewing all uncommitted changes..."
        ALL_FILES=$(git diff --name-only 2>/dev/null || echo "")

        if [ -z "$ALL_FILES" ]; then
            print_warning "No uncommitted changes found."
            exit 1
        fi

        CHANGES_SUMMARY="Modified files:\n$ALL_FILES"
        CHANGES=$(git diff 2>/dev/null || echo "")
        ;;

    commit)
        print_info "Reviewing commit: $COMMIT_HASH"
        CHANGES=$(git show "$COMMIT_HASH" 2>/dev/null || echo "")

        if [ -z "$CHANGES" ]; then
            print_error "Could not find commit: $COMMIT_HASH"
            exit 1
        fi

        CHANGES_SUMMARY="Commit: $COMMIT_HASH"
        ;;
esac

# Apply file pattern filter if specified
if [ -n "$FILE_PATTERN" ]; then
    print_info "Filtering files matching: $FILE_PATTERN"
    CHANGES=$(echo "$CHANGES" | grep -A 999999 "diff --git.*$FILE_PATTERN" || echo "")

    if [ -z "$CHANGES" ]; then
        print_warning "No files matching pattern: $FILE_PATTERN"
        exit 1
    fi
fi

# Show diff if requested
if [ "$SHOW_DIFF" = true ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Changes to review:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "$CHANGES"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
fi

# Check if changes are too large
CHANGES_SIZE=${#CHANGES}
if [ $CHANGES_SIZE -gt 50000 ]; then
    print_warning "Changes are very large ($CHANGES_SIZE chars). This may take a while..."
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Read the prompt template
PROMPT=$(cat "$PROMPT_FILE")

# Build the review request
REVIEW_REQUEST="$PROMPT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Changes to Review

$CHANGES_SUMMARY

\`\`\`diff
$CHANGES
\`\`\`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"

# Add focus area if specified
if [ -n "$FOCUS_AREA" ]; then
    REVIEW_REQUEST="$REVIEW_REQUEST

**SPECIAL FOCUS**: Pay extra attention to $FOCUS_AREA issues.
"
fi

# Add custom message if provided
if [ -n "$CUSTOM_MESSAGE" ]; then
    REVIEW_REQUEST="$REVIEW_REQUEST

**Additional Instructions**: $CUSTOM_MESSAGE
"
fi

# Run the review
print_info "Running AI code review..."
echo ""

# Create a temporary file for the request
TEMP_FILE=$(mktemp)
echo "$REVIEW_REQUEST" > "$TEMP_FILE"

# Call auggie with the review request
if [[ "$AUGGIE_CMD" == *.mjs ]]; then
    # Call auggie .mjs file directly with the correct Node version
    "$NODE_CMD" "$AUGGIE_CMD" "$(cat "$TEMP_FILE")"
else
    # Call auggie command directly
    "$AUGGIE_CMD" "$(cat "$TEMP_FILE")"
fi

# Clean up
rm -f "$TEMP_FILE"

echo ""
print_success "Code review complete!"
echo ""
echo -e "${BLUE}💡 Tip: Use --help to see all available options${NC}"

