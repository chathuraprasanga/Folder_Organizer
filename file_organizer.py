import os
import time
import magic
import threading
import itertools
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

EXTENSION_TO_FOLDER = {
    'image': ('Images', '🖼️'),
    'video': ('Videos', '🎞️'),
    'audio': ('Audio', '🎵'),
    'application/pdf': ('Documents', '📄'),
    'text/plain': ('Documents', '📄'),
    'application/vnd.ms-excel': ('Documents', '📊'),
    'application/vnd.openxmlformats-officedocument': ('Documents', '📊'),
    'application/zip': ('Archives', '🗜️'),
    'application/x-tar': ('Archives', '🗜️'),
    'application/x-bzip2': ('Archives', '🗜️'),
    'application/x-gzip': ('Archives', '🗜️'),
}


def get_category_and_symbol(mime_type):
    for key, (folder, symbol) in EXTENSION_TO_FOLDER.items():
        if mime_type.startswith(key) or key in mime_type:
            return folder, symbol
    return 'Others', '📦'


def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.2f}TB"


def copy_with_progress(src, dest, symbol):
    total_size = os.path.getsize(src)
    copied = 0
    start_time = time.time()

    with open(src, 'rb') as fsrc, open(dest, 'wb') as fdst:
        while True:
            chunk = fsrc.read(1024 * 1024)
            if not chunk:
                break
            fdst.write(chunk)
            copied += len(chunk)
            elapsed = time.time() - start_time
            speed = copied / elapsed if elapsed > 0 else 0
            percent = (copied / total_size) * 100
            print(
                f"\r[moving]  -> {symbol} {os.path.basename(src)}  {format_size(copied)}/{format_size(total_size)} ({percent:.1f}%) {format_size(speed)}/s",
                end='', flush=True)

    print(f"\r[moved]   -> {symbol} {os.path.basename(src)}  {format_size(total_size)} (100%) {format_size(speed)}/s")


def move_file_with_progress(src_path):
    mime = magic.from_file(src_path, mime=True)
    category, symbol = get_category_and_symbol(mime)

    target_dir = os.path.join(DOWNLOADS_FOLDER, category)
    os.makedirs(target_dir, exist_ok=True)

    dst_path = os.path.join(target_dir, os.path.basename(src_path))
    try:
        copy_with_progress(src_path, dst_path, symbol)
        os.remove(src_path)
    except Exception as e:
        print(f"\n❌ Error moving {src_path}: {e}")


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        time.sleep(1)
        move_file_with_progress(event.src_path)


def process_existing_files():
    print("🧹 Organizing existing files...\n")
    for filename in os.listdir(DOWNLOADS_FOLDER):
        filepath = os.path.join(DOWNLOADS_FOLDER, filename)
        if os.path.isfile(filepath):
            move_file_with_progress(filepath)


def spinner():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        print(f'\r⏳ Monitoring {DOWNLOADS_FOLDER} {c}', end='', flush=True)
        time.sleep(0.1)


if __name__ == "__main__":
    print(f"📂 Monitoring: {DOWNLOADS_FOLDER}")
    process_existing_files()

    start = input("\n🔄 Start real-time monitoring? (y/n): ").strip().lower()
    if start != 'y':
        print("🚫 Real-time monitoring skipped.")
        exit()

    observer = Observer()
    handler = FileHandler()
    observer.schedule(handler, path=DOWNLOADS_FOLDER, recursive=False)
    observer.start()

    threading.Thread(target=spinner, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
