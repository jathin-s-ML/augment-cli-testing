#!/bin/bash

# Setup script for code review aliases
# This script helps you add convenient aliases to your shell

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_REVIEW_SCRIPT="$SCRIPT_DIR/code-review.sh"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}     Code Review Agent - Alias Setup                    ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect shell
SHELL_NAME=$(basename "$SHELL")
case "$SHELL_NAME" in
    bash)
        RC_FILE="$HOME/.bashrc"
        ;;
    zsh)
        RC_FILE="$HOME/.zshrc"
        ;;
    *)
        echo -e "${YELLOW}⚠️  Unknown shell: $SHELL_NAME${NC}"
        echo "Please manually add the aliases to your shell configuration file."
        RC_FILE=""
        ;;
esac

# Aliases to add
ALIASES="
# ═══════════════════════════════════════════════════════════
# Augment Code Review Agent Aliases
# ═══════════════════════════════════════════════════════════

# Main code review command
alias code-review='$CODE_REVIEW_SCRIPT'

# Quick shortcuts
alias cr='$CODE_REVIEW_SCRIPT'                          # Quick review
alias cr-all='$CODE_REVIEW_SCRIPT --all'                # Review all changes
alias cr-security='$CODE_REVIEW_SCRIPT --focus security' # Security focus
alias cr-perf='$CODE_REVIEW_SCRIPT --focus performance' # Performance focus
alias cr-bugs='$CODE_REVIEW_SCRIPT --focus bugs'        # Bug focus

# Review with diff preview
alias cr-diff='$CODE_REVIEW_SCRIPT --diff'

# ═══════════════════════════════════════════════════════════
"

echo "The following aliases will be added:"
echo ""
echo -e "${GREEN}$ALIASES${NC}"
echo ""

if [ -n "$RC_FILE" ]; then
    read -p "Add these aliases to $RC_FILE? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Check if aliases already exist
        if grep -q "Augment Code Review Agent Aliases" "$RC_FILE" 2>/dev/null; then
            echo -e "${YELLOW}⚠️  Aliases already exist in $RC_FILE${NC}"
            read -p "Replace existing aliases? (y/n) " -n 1 -r
            echo
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Remove old aliases
                sed -i '/# Augment Code Review Agent Aliases/,/# ═══════════════════════════════════════════════════════════$/d' "$RC_FILE"
                echo "$ALIASES" >> "$RC_FILE"
                echo -e "${GREEN}✅ Aliases updated in $RC_FILE${NC}"
            else
                echo "Skipping..."
            fi
        else
            echo "$ALIASES" >> "$RC_FILE"
            echo -e "${GREEN}✅ Aliases added to $RC_FILE${NC}"
        fi
        
        echo ""
        echo -e "${BLUE}ℹ️  To use the aliases immediately, run:${NC}"
        echo -e "   ${GREEN}source $RC_FILE${NC}"
        echo ""
        echo -e "${BLUE}Or restart your terminal.${NC}"
    else
        echo "Skipping alias setup."
    fi
else
    echo "Please manually add the aliases above to your shell configuration file."
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  Usage Examples:                                        ${BLUE}║${NC}"
echo -e "${BLUE}╠════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC}  cr                    # Review staged changes          ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  cr-all                # Review all changes             ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  cr-security           # Security-focused review        ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  cr-diff               # Show diff before review        ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  code-review --help    # Show all options               ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

