# download recent version of tidal playlists
import subprocess
import os

categories = {
    "Digital 💾": {
        # "name of dir": "link to tidal playlist"
        "Breakbeat 💾": "https://tidal.com/browse/playlist/e8e66add-5ef2-47a6-a26e-9255e27b96e8",
        "Deephouse 💾": "https://tidal.com/browse/playlist/6cba8fd3-5eeb-4604-b543-566749b862db",
        "Disco 💾": "https://tidal.com/browse/playlist/d03fcb22-edae-422b-bcf8-4bc079f999ad",
        "Groove 💾" : "https://tidal.com/browse/playlist/f2ae1081-2047-4c80-89e1-b1c1769391eb",
        "House 💾": "https://tidal.com/browse/playlist/c9f2bff2-ca06-47b0-ab0a-bef06533deed",
        "House Progressive 💾": "https://tidal.com/browse/playlist/3f42436f-985d-4b50-9292-9f046cf3c766",
        "House Italo 💾": "https://tidal.com/browse/playlist/e85b2c8f-a22c-4750-95b9-b9522b502773",
        "Lounge 💾": "https://tidal.com/browse/playlist/eb47853e-86e8-4125-9e0b-b9b28da0734c",
        "NDW 💾": "https://tidal.com/browse/playlist/3f4e8665-167c-457c-8452-9406a3310b9b",
        "Techhouse 💾": "https://tidal.com/browse/playlist/985258a4-a499-49fc-9f99-c44776f9555c",
        "Techno 💾": "https://tidal.com/browse/playlist/de78a004-b37d-4284-9725-620b21282644",
        "Techno Progressive 💾": "https://tidal.com/browse/playlist/26ba4410-b229-4bed-a9f9-2f240a3658c4"
    },
    "Vinyl 📀": {
        "Breakbeat 📀": "https://tidal.com/browse/playlist/8b8c3814-b6b1-45e6-9bb7-fc6f303b8609",
        "Deephouse 📀": "https://tidal.com/browse/playlist/e14d9320-42c5-4ed4-8ec0-8eaaa7c4edb4",
        "Disco 📀": "https://tidal.com/browse/playlist/8d44e4ce-a343-40ae-adb4-6e3b4f818f64",
        "House 📀": "https://tidal.com/browse/playlist/c0a50978-c884-49ba-8b84-2994790bbba5",
        "House Italo 📀": "https://tidal.com/browse/playlist/18a44a70-e5bd-453b-b93d-32a21fb6b4fb",
        "Techhouse 📀": "https://tidal.com/browse/playlist/9086c2ec-c645-4783-ad74-bdabbcabfa68",
        "Techno 📀": "https://tidal.com/browse/playlist/c07a3a02-23bc-48fa-96d9-5875551be98a"
    },
    "Recherche ❓": {
        "Breakbeat ❓": "https://tidal.com/browse/playlist/15d24b4b-4c7f-4426-ad7d-373ff85bb233",
        "House ❓": "https://tidal.com/browse/playlist/126dc208-300f-4029-a807-ccff0ac69398",
        "House Progressive ❓": "https://tidal.com/browse/playlist/e9a257b5-68e8-44a0-86b4-55bde8f71fb1",
        "Diverse ❓": "https://tidal.com/browse/playlist/364a7d31-7aec-489d-907b-ab5fe127f17a",
        "Techhouse ❓": "https://tidal.com/browse/playlist/9295c1f0-7c79-472f-b443-a4a475802f3a",
        "Techno ❓": "https://tidal.com/browse/playlist/ba5b4c7a-eb0a-4959-8f82-077ac834deb2",
        "Radio Moafunk ❓": "https://tidal.com/browse/playlist/8200b360-93b1-4d69-b8e6-bc87cf9782d5"
    },
    "Radio Moafunk 🎙️": {
        "Radio Moafunk - UP NEXT! 🎙️": "https://tidal.com/browse/playlist/e9f25d35-80fc-4515-9f69-18b846b7f3dc",
        "20240810 Moafunk x Die Kressis #1 🎙️": "https://tidal.com/browse/playlist/414e71ba-f517-436c-828a-1444d71235e7",
    },
    "Partys 🎉": {
        "20240112 Humbi 🎉": "https://tidal.com/browse/playlist/9e49ebd5-f88f-499f-96fe-9636310a4a21",
        "20240224 Sara & Lena 🎉": "https://tidal.com/browse/playlist/e9a05322-0a03-4e33-882f-145c69440a1c",
        "20240427 Birgit 🎉": "https://tidal.com/browse/playlist/d2676cbc-7f6c-43c0-a39b-fa0158369e2e",
        "20240614 Humbi 🎉": "https://tidal.com/browse/playlist/3fd0b4ee-7ffe-4538-b0d9-3f319834b169",
        "20240815 Anti AFD 🎉": "https://tidal.com/browse/playlist/a270da30-ea86-435c-9218-262d43e2321d"
    }
}

def download_playlists(download_format_dir, playlists):
    for [playlist_name, link] in playlists.items():
        print("Update " + playlist_name + "...")

        subprocess.run(["tidal-dl", "-l", link, "-o", download_format_dir])
        
        input_folder = os.path.join(download_format_dir, playlist_name)
        subprocess.Popen(["venv/bin/python3", "convert_music_files.py", input_folder, "m4a", "mp3"])


def main():
    download_format = "m4a"

    for category_name, category_item in categories.items():
        download_format_dir = os.path.join(download_format, category_name)

        download_playlists(download_format_dir, category_item)

main()