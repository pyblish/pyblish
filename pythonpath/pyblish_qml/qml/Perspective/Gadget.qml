import QtQuick 2.3
import QtQuick.Layouts 1.1
import Pyblish 0.1


View {
    height: 85

    property string title
    property string subheading
    property int amountPassed
    property int amountFailed
    property bool hasError
    property string source
    property string itemType
    property string families

    /*!
        Time in milliseconds taken to process
    */
    property real duration
    
    /*!
        Seconds since finished
    */
    property real finishedAt

    property string ago: "Not started"
    property var agoIntervals: [
        {
            "range": 86400,
            "text": "days ago.."
        },
        {
            "range": 3600,
            "text": "over an hour ago"
        },
        {
            "range": 60,
            "text": "about a minute ago"
        },
        {
            "range": 10,
            "text": "about 10 seconds ago"
        },
        {
            "range": 0,
            "text": "just now"
        }
    ]

    function updateAgo() {
        if (!finishedAt)
            return

        var t = app.time() - finishedAt
        for (var i = 0; i < agoIntervals.length; i++) {
            if (t > agoIntervals[i].range) {
                ago = agoIntervals[i].text
                return
            }
        }
    }

    color: Qt.darker(Theme.backgroundColor, 2)

    onDurationChanged: {
        ago = "Just now"
        agoTimer.start()
    }

    Timer {
        id: agoTimer

        interval: 10000
        repeat: true

        onTriggered: updateAgo()
    }

    Component.onCompleted: updateAgo()

    RowLayout {
        spacing: 10

        anchors.fill: parent
        anchors.rightMargin: 8

        /*!
             _______________________
            |//|                |   |
            |//|                |   |
            |//|________________|___|
        */
        Rectangle {
            color: finishedAt ? (hasError ? "#a73f3f" : "#3fa75f") : "#3f7aa7"
            width: 25
            height: parent.height

            AwesomeIcon {
                name: finishedAt ? (hasError ? "exclamation-circle" : "check-circle") : "circle"
                size: 20
                anchors.horizontalCenter: parent.horizontalCenter
                y: 3
            }
        }

        /*!
             _______________________
            |  |////////////////|   |
            |  |////////////////|   |
            |__|////////////////|___|
        */
        Column {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            spacing: 5

            Spacer {}

            Row {
                spacing: 5

                height: text.paintedHeight
                width: parent.width

                AwesomeIcon {
                    name: itemType == "plugin" ? "plug" : "file"
                    size: 16
                    anchors.verticalCenter: parent.verticalCenter
                }

                Label {
                    id: text
                    text: title
                    style: "subheading"
                    font.weight: Font.Bold
                    width: parent.width - parent.spacing * 4
                    elide: Text.ElideLeft
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            Label {
                text: subheading
                opacity: 0.5
                width: parent.width
                elide: Text.ElideLeft
            }
        }

        /*!
             _______________________
            |  |                |///|
            |  |                |///|
            |__|________________|///|
        */
        ColumnLayout {
            spacing: 7

            Repeater {
                model: [
                    {
                        "icon": "slack",
                        "text": "%1/%2 passed"
                            .arg(amountPassed)
                            .arg(amountFailed + amountPassed)
                    },
                    {
                        "icon": "clock-o",
                        "text": duration ? "ran for %1 ms".arg(duration)
                                         : "Not started"
                    },
                    {
                        "icon": "calendar",
                        "text": ago
                    }
                ]

                Row {
                    spacing: 10

                    AwesomeIcon {
                        name: modelData.icon
                    }

                    Label {
                        text: modelData.text
                    }
                }
            }
        }
    }
}
