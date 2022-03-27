from PySide6.QtWidgets import QMessageBox


def show(
    *,
    parent=None,
    title="DesignCC",
    text=None,
    buttons=QMessageBox.Ok,
    default_button=QMessageBox.NoButton,
    suffix=None,
    icon=QMessageBox.NoIcon
):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title if suffix is None else title + " - " + suffix)
    msg_box.setStandardButtons(buttons)
    msg_box.setDefaultButton(default_button)
    msg_box.setIcon(icon)
    msg_box.setText(text)
    return msg_box.exec_()


def warning(**kwargs):
    return show(icon=QMessageBox.Warning, **kwargs)


def question(**kwargs):
    return show(icon=QMessageBox.Question, **kwargs)
