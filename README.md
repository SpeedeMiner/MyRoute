# MyRoute — маршрутизация Happ для RU / DIRECT / PROXY / BLOCK

Готовый профиль **Happ** на основе базы адресов [Geoip-ru-server](https://github.com/SpeedeMiner/Geoip-ru-server) и доменных категорий [Geosite-ru-light](https://github.com/SpeedeMiner/Geosite-ru-light). Профиль содержит правила `block-proxy-direct`, а сами базы Happ загружает из ветки `release` двух исходных репозиториев.

## Быстрый импорт в Happ

<!-- BEGIN_HAPP_LINK -->
**Последнее обновление (Unix UTC):** `1795872407`

[**Быстрый импорт маршрутизации в Happ**](happ://routing/add/eyJOYW1lIjoiUm9zY29tVlBOIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiUm91dGVPcmRlciI6ImJsb2NrLXByb3h5LWRpcmVjdCIsIlJlbW90ZUROU1R5cGUiOiJEb1UiLCJSZW1vdGVETlNEb21haW4iOiIiLCJSZW1vdGVETlNJUCI6IjEuMS4xLjEiLCJEb21lc3RpY0ROU1R5cGUiOiJEb1UiLCJEb21lc3RpY0ROU0RvbWFpbiI6IjEuMS4xLjEiLCJEb21lc3RpY0ROU0lQIjoiMS4xLjEuMSIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL1NwZWVkZU1pbmVyL0dlb2lwLXJ1LXNlcnZlckByZWxlYXNlL2dlb2lwX1JVLmRhdD92PTE3OTU4NzI0MDciLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL1NwZWVkZU1pbmVyL0dlb3NpdGUtcnUtbGlnaHRAcmVsZWFzZS9nZW9zaXRlX1JVLmRhdD92PTE3OTU4NzI0MDciLCJMYXN0VXBkYXRlZCI6IjE3OTU4NzI0MDciLCJsYXN0VXBkYXRlZERhdGUiOiIxNzk1ODcyNDA3IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIkRpcmVjdFNpdGVzIjpbImdlb3NpdGU6cnUiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOnR3aXRjaCIsImdlb3NpdGU6cGludGVyZXN0IiwiZ2Vvc2l0ZTpmYWNlaXQiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOnJ1Il0sIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTpnb29nbGUtZGVlcG1pbmQiLCJnZW9zaXRlOnRlbGVncmFtIiwiZGlzY29yZC1hdHRhY2htZW50cy11cGxvYWRzLXByZC5zdG9yYWdlLmdvb2dsZWFwaXMuY29tIiwiNHBkYS50byJdLCJQcm94eUlwIjpbXSwiQmxvY2tTaXRlcyI6WyJnZW9zaXRlOndpbi1zcHkiLCJkb21haW46eWFuZGV4LnJ1IiwiZ2Vvc2l0ZTpibG9jayJdLCJCbG9ja0lwIjpbXSwiRG9tYWluU3RyYXRlZ3kiOiJJUElmTm9uTWF0Y2giLCJGYWtlRE5TIjoiZmFsc2UiLCJVc2VDaHVua0ZpbGVzIjoidHJ1ZSJ9)

[Открыть deeplink текстом](happ/happ-routing-link.txt) · [JSON-профиль](happ/MyRoute.json)
<!-- END_HAPP_LINK -->

Если deeplink не открывается из браузера, скопируйте его из [happ/happ-routing-link.txt](happ/happ-routing-link.txt) и импортируйте вручную.

## JSON-профиль

- **Основной JSON:** [raw.githubusercontent.com](https://raw.githubusercontent.com/SpeedeMiner/MyRoute/main/happ/MyRoute.json) · [cdn.jsdelivr.net](https://cdn.jsdelivr.net/gh/SpeedeMiner/MyRoute@main/happ/MyRoute.json)
- **Ссылка на импорт:** [raw.githubusercontent.com](https://raw.githubusercontent.com/SpeedeMiner/MyRoute/main/happ/happ-routing-link.txt) · [cdn.jsdelivr.net](https://cdn.jsdelivr.net/gh/SpeedeMiner/MyRoute@main/happ/happ-routing-link.txt)

## Правила маршрутизации

Приоритет правил — `BLOCK → PROXY → DIRECT`. Точные правила и категории определяет [шаблон](happ/MyRoute.template.json):

| Действие | Примеры |
| --- | --- |
| DIRECT | `geosite:ru`, `geosite:microsoft`, `geosite:apple`, `geosite:steam`, `geoip:private`, `geoip:ru` |
| PROXY | `geosite:youtube`, `geosite:telegram`, `geosite:google-play`, `geosite:github`, точный домен `discord-attachments-uploads-prd.storage.googleapis.com`, `4pda.to` |
| BLOCK | `geosite:win-spy`, `domain:yandex.ru`, `geosite:block` |

Параметры DNS, `DomainStrategy=IPIfNonMatch`, `FakeDNS=false` и `UseChunkFiles=true` сохранены из эталонного профиля. Значения `true` / `false` в профиле представлены **строками** в соответствии с эталоном.

## Обновление и проверка

1. В **04:30 UTC каждый день** или при `workflow_dispatch` workflow `update-happ-timestamp.yml` получает один Unix timestamp, заменяет четыре значения в профиле, обновляет Base64 deeplink, README, коммитит `happ/MyRoute.json`, deeplink и README в `main`.
2. `validate.yml` на каждом PR и push в `main` запускает `pytest` и `python3 scripts/update_happ_profile.py --check`, проверяя соответствие JSON эталону, все четыре метки, Base64, блок README и отсутствие устаревшего дубликата.
3. После успешного push, а также после ежедневной публикации выполняется **best-effort** очистка кеша jsDelivr для `happ/MyRoute.json` и deeplink. Ошибка purge фиксируется как предупреждение и не отменяет успешный коммит. CDN может обновляться не мгновенно; ссылка `raw.githubusercontent.com` обходит ожидание jsDelivr.

```bash
python3 scripts/update_happ_profile.py
python3 scripts/update_happ_profile.py --check
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

Изменять правила следует в `happ/MyRoute.template.json`, после чего **обязательно** запускать генератор и включать все сгенерированные файлы в один коммит. `--check` не меняет файлы и завершается с ненулевым кодом при расхождении.

> Важно: ежедневная смена `?v=<timestamp>` обновляет URL загрузки баз, но не гарантирует, что исходные репозитории уже выпустили новые `release`-файлы. Ветка `main` должна разрешать запись `GITHUB_TOKEN` для автоматического коммита.