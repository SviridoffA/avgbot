#!/usr/bin/python
from pyVim.connect import SmartConnectNoSSL
from pyVmomi import vim
import configparser

def action(trg):
	config = configparser.ConfigParser()
	config.read("/var/www/avgbot/bot/cases/config.txt")
	result = 0
	vm = trg.name
	org = "AVG"

	connection = SmartConnectNoSSL(**config[org])
	content = connection.content
	container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
	vmobj = [managed_object_ref for managed_object_ref in container.view if vm == managed_object_ref.name]
	for i in vmobj:
		if i.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
			i.PowerOnVM_Task()
			result = result + 2
		else:
			result += 1
	return result
