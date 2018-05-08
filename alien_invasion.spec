# -*- mode: python -*-

block_cipher = None


a = Analysis(['alien_invasion.py'],
             pathex=['F:\\python\\pycharm-professional\\从入门到实践\\章节练习\\第十二~十四章\\alien_invasion'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='alien_invasion',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
