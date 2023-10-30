@echo off
git pull
if not exist pnpm-lock.yaml (
  pnpm install
)
pnpm run run
