default:
    @just --list

build:
    docker compose -f qa3/compose.yaml build app

start cache="on":
    @test {{quote(cache)}} = on || test {{quote(cache)}} = off
    CACHE={{quote(cache)}} docker compose -f qa3/compose.yaml up -d --wait --force-recreate app

bench duration="60s":
    bash qa3/scripts/run.sh {{quote(duration)}}

stop:
    docker compose -f qa3/compose.yaml down
