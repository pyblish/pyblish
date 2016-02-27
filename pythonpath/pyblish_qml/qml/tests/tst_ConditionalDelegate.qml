import QtQuick 2.3

Rectangle {
    width: 400
    height: 500
    
    color: "brown"

    ListModel {
        id: model

        ListElement {
            type: "delegate1"
            message: "Item 1"
        }

        ListElement {
            type: "delegate2"
            message: "Item 2"
        }

        ListElement {
            type: "delegate1"
            message: "Item 3"
        }
    }
    
    ListView {
        anchors.fill: parent

        model: model

        delegate: delegate
    }

    Component {
        id: delegate

        Loader {
            sourceComponent: type == "delegate1" ? delegate1 :
                             type == "delegate2" ? delegate2 :
                             delegate3
        }
    }

    Component {
        id: delegate1
        
        Text {
            text: message
            color: "steelblue"
        }
    }

    Component {
        id: delegate2
        
        Text {
            text: message
            color: "blue"
        }
    }

    Component {
        id: delegate3
        
        Text {
            text: message
            color: "red"
        }
    }
}