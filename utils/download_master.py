import os
import requests
import zipfile

# Constants
url = "https://directlink.icicidirect.com/NewSecurityMaster/SecurityMaster.zip"
output_dir = os.path.join("data", "instrument", "icici")
etag_path = os.path.join(output_dir, "SecurityMaster.etag")
zip_path = os.path.join(output_dir, "SecurityMaster.zip")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Prepare headers
headers = {}
if os.path.exists(etag_path):
    with open(etag_path, "r") as f:
        headers["If-None-Match"] = f.read().strip()

print("🔍 Checking for updates...")

response = requests.get(url, headers=headers, stream=True)

if response.status_code == 304:
    print("✅ No update. Remote file has not changed.")
else:
    print("⬇️ Downloading new SecurityMaster.zip...")

    # Save new ETag if present
    etag = response.headers.get("ETag")
    if etag:
        with open(etag_path, "w") as f:
            f.write(etag)

    # Write ZIP file
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract ZIP
    print(f"📦 Extracting contents to: {output_dir}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    print("✅ Extraction complete.")
