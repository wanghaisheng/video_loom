# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['app.py'],
             pathex=[],
             binaries=[],
             datas=[
              ("E:\\software\\Python\\Python311\\Lib\\site-packages\\av.libs\\*.dll", 'av.libs'),
              ("..\\changelog.md", '.'),
              ("..\\img\\app_logo.ico", '.')
            ],
             hiddenimports=['av', 'chardet'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [('v', None, 'OPTION')],
          name='video_loom',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon="E:\\dev\\github\\video_loom\\img\\app_logo.ico",
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None
        )
