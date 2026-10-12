default:
    @just --list

build:
    docker compose -f qa3/compose.yaml build app

start cache="on":
    @test {{quote(cache)}} = on || test {{quote(cache)}} = off
    CACHE={{quote(cache)}} docker compose -f qa3/compose.yaml up -d --wait --force-recreate app

bench:
    docker compose -f qa3/compose.yaml run --rm --no-deps load

stop:
    docker compose -f qa3/compose.yaml down
