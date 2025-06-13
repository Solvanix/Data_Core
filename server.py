from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

LOCAL_REPOS = [
    "/mnt/c/Users/ali/Desktop/STEAM_Nexus_Hub/Repo1",
    "/mnt/c/Users/ali/Desktop/STEAM_Nexus_Hub/Repo2",
    "/mnt/c/Users/ali/Desktop/STEAM_Nexus_Hub/Repo3"
]  # تأكد من صحة المسارات

@app.route("/sync-all", methods=["POST"])
def sync_all_repos():
    results = {}

    for repo in LOCAL_REPOS:
        if not os.path.exists(repo):
            results[repo] = "❌ خطأ: المستودع غير موجود!"
            continue

        os.chdir(repo)
        try:
            subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
            subprocess.run(["git", "commit", "-m", "مزامنة تلقائية"], check=True, capture_output=True, text=True)
            subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True, text=True)
            results[repo] = "✅ تمت مزامنته بنجاح!"
        except subprocess.CalledProcessError as e:
            results[repo] = f"❌ خطأ أثناء التنفيذ: {e.stderr}"

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)