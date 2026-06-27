Output demos/demo.gif
Set Shell "bash"
Set FontSize 20
Set Width 1280
Set Height 720
Set Theme "Catppuccin Mocha"
Set TypingSpeed 50ms

Type "# graphtheory.xyz · static cyberpunk landing" Enter
Sleep 600ms
Type "grep -m1 '<title>' index.html" Enter
Sleep 2s
Type "ls assets" Enter
Sleep 3s

Hide
Type "python3 -m http.server 4173 >/tmp/gt-demo-http.log 2>&1 &" Enter
Sleep 1s
Type "curl -s http://127.0.0.1:4173/ | head -20" Enter
Sleep 5s
Type "pkill -f 'http.server 4173' || true" Enter
Sleep 1s
Show

Type "# Zero build step · python3 -m http.server 4173" Enter
Sleep 3s
Type "open https://graphtheory.xyz/" Enter
Sleep 3s