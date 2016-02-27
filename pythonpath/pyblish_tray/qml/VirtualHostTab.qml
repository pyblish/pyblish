import QtQuick 2.3
import QtQuick.Layouts 1.1
import QtGraphicalEffects 1.0

import Library 0.1


Item {
    ColumnLayout {
        anchors.fill: parent

        Button {
            text: "SHOW"
            Layout.alignment: Qt.AlignHCenter
            onClicked: hostCtrl.show()
        }
    }
}