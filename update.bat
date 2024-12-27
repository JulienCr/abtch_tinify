@echo off
echo "Mise à jour en cours..."
git pull
pnpm update && echo "Mise à jour terminée."
