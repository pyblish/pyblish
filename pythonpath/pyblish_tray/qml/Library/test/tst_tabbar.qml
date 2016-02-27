import QtQuick 2.3
import QtQuick.Controls 1.3
import ".."

Item {
    width: 500
    height: 100

    TabBar {
        anchors.centerIn: parent
        actions: [
            Action {
                iconName: "hand-o-up"
                onTriggered: print("Whop!")
            },

            Action {
                iconName: "close"
                onTriggered: print("Whop again!!")
            },

            Action {
                iconName: "close"
                onTriggered: print("Whop again!!")
            },

            Action {
                iconName: "close"
                onTriggered: print("Whop again!!")
            }
        ]
    }
}