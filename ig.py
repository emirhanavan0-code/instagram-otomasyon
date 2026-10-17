"""@seovedijital Instagram hesabı için Composio üzerinden analiz ve yönetim aracı.

Kullanım:
  python ig.py hesaplar                 # Composio'daki Instagram bağlantılarını listele
  python ig.py araclar                  # Instagram toolkit'indeki tüm araçları (slug) listele
  python ig.py calistir SLUG '{"k": 1}' # Herhangi bir aracı JSON argümanla çalıştır
  python ig.py analiz                   # Profil + gönderileri çekip etkileşim raporu üret
"""
import json
import os
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "https://backend.composio.dev/api/v3"
ROOT = Path(__file__).parent
POST_METRICS = ["reach", "views", "saved", "shares", "total_interactions"]


def load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def api(method, path, **kwargs):
    resp = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers={"x-api-key": os.environ["COMPOSIO_API_KEY"]},
        timeout=60,
        **kwargs,
    )
    if not resp.ok:
        raise RuntimeError(f"Composio {resp.status_code}: {resp.text[:500]}")
    return resp.json()


def connected_account():
    items = api("GET", "/connected_accounts", params={"toolkit_slugs": "instagram"}).get("items", [])
    active = [a for a in items if a.get("status") == "ACTIVE"]
    if not active:
        sys.exit("Composio'da aktif Instagram bağlantısı bulunamadı.")
    return active[0]


def execute(slug, arguments=None):
    account = connected_account()
    body = {"connected_account_id": account["id"], "user_id": account.get("user_id"), "arguments": arguments or {}}
    result = api("POST", f"/tools/execute/{slug}", json=body)
    if not result.get("successful", True):
        raise RuntimeError(f"{slug} başarısız: {result.get('error')}")
    return result.get("data", result)


def profil_id():
    """Paylaşım araçlarının istediği Instagram işletme hesabı kimliği."""
    return os.environ.get("IG_USER_ID") or execute("INSTAGRAM_GET_USER_INFO")["id"]


def list_tools():
    return api("GET", "/tools", params={"toolkit_slug": "instagram", "limit": 200}).get("items", [])


def find_tool(tools, *keywords):
    for tool in tools:
        slug = tool["slug"].upper()
        if all(k in slug for k in keywords):
            return tool["slug"]
    return None


def unwrap_list(data):
    """Composio yanıtlarındaki gönderi listesini farklı sarmalama biçimlerinden çıkarır."""
    if isinstance(data, list):
        return data
    for key in ("data", "media", "items", "response_data"):
        if isinstance(data, dict) and key in data:
            return unwrap_list(data[key])
    return []


def analyze():
    tools = list_tools()
    profile_slug = find_tool(tools, "USER", "INFO") or find_tool(tools, "PROFILE")
    media_slug = find_tool(tools, "USER", "MEDIA") or find_tool(tools, "MEDIA")
    if not (profile_slug and media_slug):
        sys.exit("Profil/medya araçları bulunamadı; 'python ig.py araclar' çıktısını kontrol edin.")

    profile = execute(profile_slug)
    media = unwrap_list(execute(media_slug, {"limit": 50}))
    followers = (profile.get("data", profile) if isinstance(profile, dict) else {}).get("followers_count") or 0

    by_type = defaultdict(list)
    by_weekday = defaultdict(list)
    by_hour = defaultdict(list)
    rows = []
    for post in media:
        engagement = (post.get("like_count") or 0) + (post.get("comments_count") or 0)
        rate = engagement / followers * 100 if followers else None
        ts = datetime.fromisoformat(post["timestamp"].replace("+0000", "+00:00")) if post.get("timestamp") else None
        by_type[post.get("media_type", "?")].append(engagement)
        if ts:
            by_weekday[ts.strftime("%A")].append(engagement)
            by_hour[ts.hour].append(engagement)
        try:
            insights = execute("INSTAGRAM_GET_POST_INSIGHTS", {"ig_post_id": post["id"], "metric": POST_METRICS})
            stats = {x["name"]: x["values"][0]["value"] for x in unwrap_list(insights)}
        except RuntimeError:
            stats = {}
        rows.append({"id": post.get("id"), "tarih": post.get("timestamp"), "tur": post.get("media_type"),
                     "etkilesim": engagement, **stats, "oran_%": round(rate, 2) if rate is not None else None,
                     "baglanti": post.get("permalink"), "aciklama": (post.get("caption") or "")[:80]})

    def avg_table(groups):
        return {str(k): round(statistics.mean(v), 1) for k, v in sorted(groups.items(), key=lambda kv: -statistics.mean(kv[1]))}

    report = {
        "olusturma": datetime.now().isoformat(timespec="seconds"),
        "profil": profile,
        "gonderi_sayisi": len(rows),
        "ortalama_etkilesim": round(statistics.mean(r["etkilesim"] for r in rows), 1) if rows else 0,
        "tur_bazinda": avg_table(by_type),
        "gun_bazinda": avg_table(by_weekday),
        "saat_bazinda_utc": avg_table(by_hour),
        "en_iyi_5": sorted(rows, key=lambda r: -r["etkilesim"])[:5],
        "en_zayif_5": sorted(rows, key=lambda r: r["etkilesim"])[:5],
        "gonderiler": rows,
    }
    out = ROOT / "raporlar" / f"analiz_{datetime.now():%Y%m%d_%H%M}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "gonderiler"}, ensure_ascii=False, indent=2))
    print(f"\nRapor kaydedildi: {out}")


def main():
    load_env()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "analiz"
    if cmd == "hesaplar":
        print(json.dumps(api("GET", "/connected_accounts", params={"toolkit_slugs": "instagram"}), ensure_ascii=False, indent=2))
    elif cmd == "araclar":
        for tool in list_tools():
            print(f"{tool['slug']:45} {tool.get('description', '')[:90]}")
    elif cmd == "calistir":
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        print(json.dumps(execute(sys.argv[2], args), ensure_ascii=False, indent=2))
    elif cmd == "analiz":
        analyze()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
