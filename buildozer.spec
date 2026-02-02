cat > buildozer.spec << 'EOF'
[app]

# Nome do aplicativo
title = Executor Scripts

# Nome do pacote
package.name = executorscripts

# Domínio
package.domain = com.executorscripts

# Diretório fonte
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Versão
version = 1.0

# Requisitos
requirements = python3,kivy==2.2.1,pyjnius,android

# Orientação
orientation = portrait
fullscreen = 0

# Permissões
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,SYSTEM_ALERT_WINDOW

# API levels
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Arquiteturas
android.archs = arm64-v8a,armeabi-v7a

# Bootstrap
android.bootstrap = sdl2

# Wakelock
android.wakelock = True

# Meta-data
android.meta_data = surface.transparent=0

[buildozer]

# Log level
log_level = 2

# Warn on root
warn_on_root = 1
EOF
