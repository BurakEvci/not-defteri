#!/usr/bin/env bash
# wait-for-it.sh

host="$1"
shift
cmd="$@"

until nc -z "$host" 5432; do
  echo "📡 Bekleniyor: $host:5432"
  sleep 1
done

echo "✅ Veritabanı hazır: $host:5432"
exec $cmd
