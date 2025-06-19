# Downloads Folder Auto Sorter

Automatically organize your `~/Downloads` folder by file type (images, videos, documents, etc.) and keep it clean in real-time. This script moves files into subfolders based on their MIME type, shows progress, and optionally monitors the folder for new files.

---

## ✨ Features

* 📂 Automatically categorizes and moves files based on type
* 🎯 Detects MIME type using `python-magic` (accurate over just file extensions)
* 🔄 Real-time monitoring with `watchdog`
* 📦 Progress bar during large file transfers
* 📜 Organizes existing files on startup

---

## 📁 Categories

Files are automatically moved into the following folders inside `~/Downloads`:

| Category  | Folder Name | Emoji |
| --------- | ----------- | ----- |
| Images    | Images      | 🖼️   |
| Videos    | Videos      | 🎞️   |
| Audio     | Audio       | 🎵    |
| Documents | Documents   | 📄📊  |
| Archives  | Archives    | 🗜️   |
| Others    | Others      | 📦    |

---

## 🚀 Getting Started

### 1. Install Requirements

```bash
pip install python-magic watchdog
```

On macOS, you may need `libmagic`:

```bash
brew install libmagic
```

### 2. Run the Script

```bash
python main.py
```

It will:

* Organize existing files.
* Ask to start real-time monitoring (press `y` to enable).

---

## 🛠️ Customization

* Edit `EXTENSION_TO_FOLDER` dictionary in the script to add or modify MIME-based rules.

---

## 🙌 Contributions & Credits

Created by \[Your Name]

Pull requests welcome!

Special thanks to:

* [`python-magic`](https://github.com/ahupp/python-magic)
* [`watchdog`](https://github.com/gorakhargosh/watchdog)

---

## 🏷 GitHub Topics

```
python
file-management
automation
downloads
organizer
watchdog
file-sorter
real-time
python-magic
```

---
