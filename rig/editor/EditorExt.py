from dataclasses import dataclass
from pathlib import Path
from typing import Callable

# noinspection PyUnreachableCode
if False:
	# noinspection PyUnresolvedReferences
	from _stubs import *
	from _stubs.PopDialogExt import PopDialogExt

class Editor:
	def __init__(self, ownerComp: 'COMP'):
		self.ownerComp = ownerComp

	@property
	def _ChainAttrs(self): return self.ownerComp.op('chain_attrs')

	@property
	def _ChainHolder(self): return self.ownerComp.op('chain_holder')

	@property
	def _Chain(self): return self.ownerComp.op('chain_holder/chain')

	def LoadChain(self, chainInfo: '_ChainInfo'):
		attrs = self._ChainAttrs
		attrs.par.Name = chainInfo.name or ''
		attrs.par.Folder = chainInfo.folder or ''
		toxFile = chainInfo.tox or ''
		attrs.par.Tox = toxFile
		attrs.par.Thumb = chainInfo.thumb or ''
		holder = self._ChainHolder
		print('LoadChainTox tox: {} holder: {}'.format(toxFile, holder))
		for child in holder.ops('*'):
			child.destroy()
		chain = holder.create(baseCOMP, 'chain')
		if toxFile:
			print('loading tox file {!r}'.format(toxFile))
			# chain = holder.loadTox(toxFile, unwired=True)
			chain.par.externaltox = toxFile
			chain.par.reinitnet.pulse()
		print('loaded chain {!r}'.format(chain))

	def OnSelectedChainChange(self, dat):
		if dat.numRows < 2:
			return
		chainInfo = _ChainInfo.FromRow(dat, 1)
		self.LoadChain(chainInfo)

	def SaveChain(self, newName: str = None):
		chain = self._Chain
		if not chain:
			return
		attrs = self._ChainAttrs
		name = attrs.par.Name.eval()
		if newName == name:
			newName = None
		if newName:
			chainsDirStr = tdu.expandPath(self.ownerComp.par.Chainsdirectory.eval())
			folder = Path(chainsDirStr) / newName
			if folder.exists():
				ui.messageBox('Unable to save chain!', 'Chain directory already exists: {!r}!'.format(folder))
				return
			folder.mkdir(parents=True)
			toxFile = (folder / (newName + '.tox')).as_posix()
			thumbFile = (folder / 'thumb.png').as_posix()
			attrs.par.Name.val = newName
			attrs.par.Folder.val = tdu.collapsePath(folder.as_posix())
			attrs.par.Tox.val = tdu.collapsePath(toxFile)
			attrs.par.Thumb.val = tdu.collapsePath(thumbFile)
		else:
			toxFile = tdu.expandPath(attrs.par.Tox.eval())
			thumbFile = tdu.expandPath(attrs.par.Thumb.eval())
		print('saving chain to tox {!r}'.format(toxFile))
		chain.save(toxFile)
		print('saving thumbnail to {!r}'.format(thumbFile))
		self.ownerComp.op('new_thumb').save(thumbFile)

	def SaveChainAs(self):
		_ShowPromptDialog(
			'Save chain as',
			'New chain name',
			self._ChainAttrs.par.Name.eval(),
			textentry=True,
			oktext='Save',
			ok=lambda newName: self.SaveChain(newName),
		)

@dataclass
class _ChainInfo:
	name: str = None
	folder: str = None
	modified: str = None
	tox: str = None
	thumb: str = None
	thumbtop: str = None

	@classmethod
	def FromRow(cls, dat, row):
		return cls(
			name=dat[row, 'name'].val,
			folder=dat[row, 'folder'].val,
			modified=dat[row, 'modified'].val,
			tox=dat[row, 'tox'].val,
			thumb=dat[row, 'thumb'].val,
			thumbtop=dat[row, 'thumbtop'].val,
		)


def _ShowPromptDialog(
		title=None,
		text=None,
		default='',
		textentry=True,
		oktext='OK',
		canceltext='Cancel',
		ok: Callable = None,
		cancel: Callable = None):
	def _callback(info):
		if info['buttonNum'] == 1:
			if ok:
				if not text:
					ok()
				else:
					ok(info.get('enteredText'))
		elif info['buttonNum'] == 2:
			if cancel:
				cancel()
	dialog = op.TDResources.op('popDialog')  # type: PopDialogExt
	dialog.Open(
		title=title,
		text=text,
		textEntry=False if not textentry else (default or ''),
		buttons=[oktext, canceltext],
		enterButton=1, escButton=2, escOnClickAway=True,
		callback=_callback)
