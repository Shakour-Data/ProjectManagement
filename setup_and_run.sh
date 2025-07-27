#!/bin/bash

# Clone the repository
git clone https://github.com/Shakour-Data/ProjectManagement.git

cd ProjectManagement || exit 1

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Ensure uvicorn is installed (in case requirements.txt update is not picked up)
pip install uvicorn

# Install frontend dependencies
cd frontend || exit 1
npm install

# Start backend server in background
cd ..
source venv/bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 8000 &

# Start frontend server in background
cd frontend || exit 1
npm start &

# Function to check if a port is open (server ready)
check_server() {
  local url=$1
  if command -v curl >/dev/null 2>&1; then
    curl --silent --head --fail "$url" >/dev/null 2>&1
    return $?
  elif command -v wget >/dev/null 2>&1; then
    wget --spider --quiet "$url"
    return $?
  else
    return 1
  fi
}

# Wait for backend server
echo "Waiting for backend server to start on http://localhost:8000 ..."
until check_server http://localhost:8000; do
  sleep 2
done
echo "Backend server is up."

# Wait for frontend server
echo "Waiting for frontend server to start on http://localhost:3000 ..."
until check_server http://localhost:3000; do
  sleep 2
done
echo "Frontend server is up."

# Open frontend URL in default browser
echo "Opening frontend UI in your default browser..."
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open http://localhost:3000
elif command -v open >/dev/null 2>&1; then
  open http://localhost:3000
else
  echo "Please open your browser and go to http://localhost:3000"
fi

# Create desktop shortcut cross-platform
echo "Creating desktop shortcut..."

DESKTOP_PATH=""
SHORTCUT_NAME="ProjectManagement_UI"

case "$(uname)" in
  Linux)
    DESKTOP_PATH="$HOME/Desktop"
    SHORTCUT_FILE="$DESKTOP_PATH/$SHORTCUT_NAME.desktop"
    cat > "$SHORTCUT_FILE" <<EOL
[Desktop Entry]
Name=ProjectManagement UI
Type=Application
Exec=xdg-open http://localhost:3000
Icon=utilities-terminal
Terminal=false
EOL
    chmod +x "$SHORTCUT_FILE"
    echo "Desktop shortcut created at $SHORTCUT_FILE"
    ;;
  Darwin)
    DESKTOP_PATH="$HOME/Desktop"
    SHORTCUT_FILE="$DESKTOP_PATH/$SHORTCUT_NAME.webloc"
    cat > "$SHORTCUT_FILE" <<EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>URL</key>
  <string>http://localhost:3000</string>
</dict>
</plist>
EOL
    echo "Desktop shortcut created at $SHORTCUT_FILE"
    ;;
  CYGWIN*|MINGW32*|MSYS*|MINGW*)
    # Windows - create a .url file on Desktop as a fallback
    DESKTOP_PATH="$USERPROFILE/Desktop"
    SHORTCUT_FILE="$DESKTOP_PATH/$SHORTCUT_NAME.url"
    cat > "$SHORTCUT_FILE" <<EOL
[InternetShortcut]
URL=http://localhost:3000
EOL
    echo "Desktop shortcut created at $SHORTCUT_FILE"
    ;;
  *)
    echo "Unsupported OS for desktop shortcut creation. Please create a shortcut manually to http://localhost:3000"
    ;;
esac

echo "Setup complete. You can use the desktop shortcut or visit http://localhost:3000 to access the UI."

# Wait for background processes
wait
