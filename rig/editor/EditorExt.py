
# noinspection PyUnreachableCode
if False:
	# noinspection PyUnresolvedReferences
	from _stubs import *

class Editor:
	def __init__(self, ownerComp: 'COMP'):
		self.ownerComp = ownerComp

	def LoadChainTox(self, toxFile):
		holder = self.ownerComp.op('chain_holder')
		print('LoadChainTox tox: {} holder: {}'.format(toxFile, holder))
		for child in holder.ops('*'):
			child.destroy()
		print("killed child COMPs")
		chain = holder.create(baseCOMP, 'chain')
		if toxFile:
			print('loading tox file {!r}'.format(toxFile))
			# chain = holder.loadTox(toxFile, unwired=True)
			chain.par.externaltox = toxFile
			chain.par.reinitnet.pulse()
		print('loaded chain {!r}'.format(chain))
