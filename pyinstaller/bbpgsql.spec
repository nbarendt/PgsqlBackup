# -*- mode: python -*-
a = Analysis([
	os.path.join(HOMEPATH,'support/_mountzlib.py'),
	os.path.join(HOMEPATH,'support/useUnicode.py'),
	'../bbpgsql/cmdline_scripts/bbpgsql'],
     pathex=['/home/nbarendt/PgsqlBackup/pyinstaller-1.5-rc1'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'bbpgsql'),
          debug=False,
          strip=True,
          upx=True,
          console=1 )
