from pathlib import Path

# noinspection PyUnreachableCode
if False:
	# noinspection PyUnresolvedReferences
	from _stubs import *

class ChainHost:
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp

	def BuildChainDirInfo(self, dat: 'DAT'):
		dat.clear()
		dirRawPathStr = self.ownerComp.par.Directory.eval()
		dirPathStr = dirRawPathStr
		if dirPathStr:
			dirPathStr = tdu.expandPath(dirPathStr or '')
		dirPathInfo = tdu.PathInfo(dirPathStr)
		dirPath = Path(dirPathInfo.absPath)
		exists = bool(dirPathInfo) and dirPath.exists()
		dat.appendCol([
			'name',
			'path',
			'absPath',
			'exists',
		])
		dat.appendCol([
			dirPath.name or '',
			dirRawPathStr or '',
			dirPathInfo.absPath or '',
			int(exists),
		])

	def BuildChainFiles(self, dat: 'DAT', dirInfoDat: 'DAT', dirFilesDat: 'DAT'):
		dat.clear()
		chainName = dirInfoDat['name', 1].val
		toxName = self._GetChainToxFile(dirFilesDat, chainName)
		toxPath = ''
		if toxName:
			prefix = dirInfoDat['path', 1].val
			if prefix and not prefix.endswith('/'):
				prefix += '/'
			toxPath = prefix + dirFilesDat[toxName, 'relpath'].val
		dat.appendRow(['toxName', toxName])
		dat.appendRow(['toxPath', toxPath])

	@staticmethod
	def _GetChainToxFile(dirFilesDat: 'DAT', chainName: str):
		if not chainName:
			return None
		tox = chainName + '.tox'
		return tox if dirFilesDat[tox, 0] is not None else None
