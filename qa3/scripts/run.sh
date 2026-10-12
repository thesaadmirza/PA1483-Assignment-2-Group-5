#!/usr/bin/env bash
set -e
cd qa3

duration=${1:-60s}
id=$(docker compose ps -q app)
cache=$(docker compose exec -T app printenv CACHE)
folder="$(date -u +%Y%m%dT%H%M%SZ)-$cache"
out="data/$folder"
mkdir "$out"

git rev-parse HEAD > "$out/commit.txt"
docker compose exec -T app pip freeze > "$out/packages.txt"
printf 'cache=%s users=10 warmup=15s duration=%s\n' "$cache" "$duration" > "$out/settings.txt"

docker compose run --rm --no-deps load --headless -u 10 -r 10 -t 15s > "$out/warmup.log" 2>&1

docker stats --format '{{json .}}' "$id" > "$out/memory.log" &
monitor=$!
trap 'kill "$monitor" 2>/dev/null || true' EXIT

docker compose run --rm --no-deps load --headless -u 10 -r 10 -t "$duration" --reset-stats --csv "/data/$folder/locust" > "$out/load.log" 2>&1
docker inspect --format 'image={{.Image}} oom={{.State.OOMKilled}} restarts={{.RestartCount}}' "$id" > "$out/server.txt"
printf 'Saved in qa3/%s\n' "$out"
