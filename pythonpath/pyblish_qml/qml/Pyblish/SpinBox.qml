import QtQuick 2.3
import QtQuick.Controls 1.3 as Control
import QtQuick.Controls.Styles 1.3
import Pyblish 0.1

Control.SpinBox {
    style: SpinBoxStyle {
        background: Item {}

        font.family: "Open Sans"

        textColor: Theme.dark.textColor
        selectionColor: Theme.accentColor
    }
}