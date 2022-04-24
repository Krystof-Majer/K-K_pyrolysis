from PySide6.QtWidgets import QMessageBox


def show_msg(
    *,
    parent=None,
    text=None,
    info_text=None,
    buttons=QMessageBox.Ok,
    default_button=QMessageBox.NoButton,
    suffix=None,
    icon=QMessageBox.NoIcon
):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setInformativeText(info_text)
    msg.setStandardButtons(buttons)
    msg.setDefaultButton(default_button)
    return msg.exec_()


def warning(**kwargs):
    return show_msg(icon=QMessageBox.Warning, **kwargs)


def question(**kwargs):
    return show_msg(icon=QMessageBox.Question, **kwargs)


def critical(**kwargs):
    return show_msg(icon=QMessageBox.Critical, **kwargs)


def information(**kwargs):
    return show_msg(icon=QMessageBox.Information, **kwargs)
