from . import prop, trigger, ui


def register():
    pass


def activate():
    trigger.activate()


def deactivate():
    trigger.deactivate()


def retranslate_ui():
    trigger.retranslate_ui()


def on_new_project():
    trigger.on_new_project()
