"""
Network Widget module

"""

import pyVmomi
import pvc.widget.menu
import pvc.widget.form
import pvc.widget.virtualmachine

__all__ = ['NetworkWidget']


class NetworkWidget(object):
    def __init__(self, agent, dialog, obj):
        """
        Network Widget

        Args:
            agent     (VConnector): A VConnector instance
            dialog (dialog.Dialog): A Dialog instance
            obj      (vim.Network): A vim.Network managed entity

        """
        if not isinstance(obj, pyVmomi.vim.Network):
            raise TypeError('Need a vim.Network instance')

        self.agent = agent
        self.dialog = dialog
        self.obj = obj
        self.display()

    def display(self):
        items = [
            pvc.widget.menu.MenuItem(
                tag='Summary',
                description='General Information',
                on_select=self.summary
            ),
            pvc.widget.menu.MenuItem(
                tag='Virtual Machines',
                description='Virtual Machines using the network ',
                on_select=self.virtual_machine_menu,
            ),
            pvc.widget.menu.MenuItem(
                tag='Hosts',
                description='Hosts using the network',
            ),
            pvc.widget.menu.MenuItem(
                tag='Tasks',
                description='View Tasks',
            ),
            pvc.widget.menu.MenuItem(
                tag='Events',
                description='View Events'
            ),
        ]

        menu = pvc.widget.menu.Menu(
            title=self.obj.name,
            items=items,
            dialog=self.dialog
        )
        menu.display()

    def summary(self):
        """
        General information about the network

        """
        self.dialog.infobox(
            title=self.obj.name,
            text='Retrieving information ...'
        )

        elements = [
            pvc.widget.form.FormElement(
                label='Name',
                item=self.obj.name
            ),
            pvc.widget.form.FormElement(
                label='Accessible',
                item=str(self.obj.summary.accessible)
            ),
            pvc.widget.form.FormElement(
                label='IP Pool',
                item=self.obj.summary.ipPoolName
            ),
        ]

        form = pvc.widget.form.Form(
            dialog=self.dialog,
            form_elements=elements,
            title=self.obj.name
        )
        form.display()

    def virtual_machine_menu(self):
        """
        Virtual Machines using the network

        """
        self.dialog.infobox(
            title=self.obj.name,
            text='Retrieving information ...'
        )

        items = [
            pvc.widget.menu.MenuItem(
                tag=vm.name,
                description=vm.runtime.powerState,
                on_select=pvc.widget.virtualmachine.VirtualMachineWidget,
                on_select_args=(self.agent, self.dialog, vm)
            ) for vm in self.obj.vm
        ]

        menu = pvc.widget.menu.Menu(
            title=self.obj.name,
            text="Virtual Machines using '{}' network".format(self.obj.name),
            items=items,
            dialog=self.dialog
        )
        menu.display()