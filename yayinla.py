"""Zamanı gelmiş, onaylı (main dalındaki "planlandi") içerikleri Composio üzerinden Instagram'da yayınlar.

Kullanım:
  python yayinla.py            # zamanı gelenleri yayınla
  python yayinla.py --kuru     # sadece ne yayınlanacağını göster, paylaşma
  python yayinla.py --test ID  # içeriği Instagram'a taslak olarak yükle ama yayınlama (URL/format kontrolü)
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import ig

ROOT = Path(__file__).parent
REPO = os.environ.get("GITHUB_REPOSITORY", "emirhanavan0-code/instagram-otomasyon")


def medya_url(yol, sha):
    # jsDelivr doğru içerik türüyle (image/jpeg, video/mp4) sunar; commit SHA ile adres değişmez
    return f"https://cdn.jsdelivr.net/gh/{REPO}@{sha}/{yol}"


def hazir_bekle(creation_id, deneme=40):
    for _ in range(deneme):
        durum = ig.execute("INSTAGRAM_GET_POST_STATUS", {"creation_id": creation_id})
        kod = (durum.get("status_code") or durum.get("status") or "").upper()
        if "FINISHED" in kod:
            return
        if "ERROR" in kod or "EXPIRED" in kod:
            raise RuntimeError(f"Instagram medyayı işleyemedi: {durum}")
        time.sleep(15)
    raise RuntimeError(f"{creation_id} zaman aşımı")


def kimlik(sonuc):
    return sonuc.get("id") or sonuc.get("creation_id") or (sonuc.get("data") or {}).get("id")


def taslak_olustur(icerik, ig_user_id, sha):
    urls = [medya_url(m, sha) for m in icerik["medya"]]
    aciklama = icerik["aciklama"]
    if icerik["tur"] == "reels":
        video, kapak = urls
        cid = kimlik(ig.execute("INSTAGRAM_CREATE_MEDIA_CONTAINER", {
            "ig_user_id": ig_user_id, "video_url": video, "cover_url": kapak,
            "media_type": "REELS", "content_type": "reel", "caption": aciklama}))
    elif len(urls) == 1:
        cid = kimlik(ig.execute("INSTAGRAM_CREATE_MEDIA_CONTAINER", {
            "ig_user_id": ig_user_id, "image_url": urls[0], "content_type": "photo", "caption": aciklama}))
    else:
        cocuklar = [kimlik(ig.execute("INSTAGRAM_CREATE_MEDIA_CONTAINER", {
            "ig_user_id": ig_user_id, "image_url": u, "content_type": "carousel_item", "is_carousel_item": True}))
            for u in urls[:10]]
        cid = kimlik(ig.execute("INSTAGRAM_CREATE_CAROUSEL_CONTAINER", {
            "ig_user_id": ig_user_id, "children": cocuklar, "caption": aciklama}))
    hazir_bekle(cid)
    return cid


def zamani_gelenler():
    simdi = datetime.now(timezone.utc)
    for dosya in sorted((ROOT / "icerik").glob("*.json")):
        icerik = json.loads(dosya.read_text())
        if icerik.get("durum") == "planlandi" and datetime.fromisoformat(icerik["yayin_zamani"]) <= simdi:
            yield dosya, icerik


def main():
    ig.load_env()
    sha = os.environ.get("GITHUB_SHA") or os.popen("git rev-parse HEAD").read().strip()
    ig_user_id = ig.profil_id()

    if "--test" in sys.argv:
        dosya = ROOT / "icerik" / f"{sys.argv[sys.argv.index('--test') + 1]}.json"
        cid = taslak_olustur(json.loads(dosya.read_text()), ig_user_id, sha)
        print(f"✓ Taslak hazır, yayınlanmadı (creation_id={cid})")
        return

    for dosya, icerik in zamani_gelenler():
        if "--kuru" in sys.argv:
            print(f"Yayınlanacak: {icerik['id']} ({icerik['tur']}, {icerik['yayin_zamani']})")
            continue
        try:
            cid = taslak_olustur(icerik, ig_user_id, sha)
            gonderi = ig.execute("INSTAGRAM_CREATE_POST", {"ig_user_id": ig_user_id, "creation_id": cid})
            icerik.update(durum="yayinlandi", instagram_id=kimlik(gonderi),
                          yayinlanma=datetime.now(timezone.utc).isoformat(timespec="seconds"))
            print(f"✓ Yayınlandı: {icerik['id']} → {icerik['instagram_id']}")
        except Exception as hata:  # bir içerik bozuksa diğerleri yine yayınlansın
            icerik.update(durum="hata", hata=str(hata)[:500])
            print(f"✗ {icerik['id']}: {hata}")
        dosya.write_text(json.dumps(icerik, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
