from PySide6.QtWidgets import QMessageBox


def show_msg(
    *,
    parent=None,
    text=None,
    info_text=None,
    details=None,
    buttons=QMessageBox.Ok,
    default_button=QMessageBox.NoButton,
    suffix=None,
    icon=None
):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setInformativeText(info_text)
    msg.setStandardButtons(buttons)
    msg.setDefaultButton(default_button)
    msg.setDetailedText(details)
    msg.setIcon(icon)
    return msg.exec_()


def warning_msg(**kwargs):
    return show_msg(icon=QMessageBox.Warning, **kwargs)


def question_msg(**kwargs):
    return show_msg(icon=QMessageBox.Question, **kwargs)


def critical_msg(**kwargs):
    return show_msg(icon=QMessageBox.Critical, **kwargs)


def information_msg(**kwargs):
    return show_msg(icon=QMessageBox.Information, **kwargs)
