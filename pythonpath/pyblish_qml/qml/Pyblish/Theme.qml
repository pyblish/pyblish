import QtQuick 2.0

pragma Singleton


Object {
    id: theme

    /*!
       The primary color used for the toolbar background unless a page specifies its own color.
       This can be customized via the \l ApplicationWindow::theme group property. According to the
       Material Design guidelines, this should normally be a 500 color from one of the color
       palettes at \l {http://www.google.com/design/spec/style/color.html#color-color-palette}.
     */
    property color primaryColor: "#99CEEE"

    /*!
       A darker version of the primary color used for the window titlebar (if client-side
       decorations are not used), unless a \l Page specifies its own primary and primary dark
       colors. This can be customized via the \l ApplicationWindow::theme group property. According
       to the Material Design guidelines, this should normally be the 700 color version of your
       aplication's primary color, taken from one of the color palettes at
       \l {http://www.google.com/design/spec/style/color.html#color-color-palette}.
    */
    property color primaryDarkColor: "#1976D2"

    /*!
       The accent color complements the primary color, and is used for any primary action buttons
       along with switches, sliders, and other components that do not specifically set a color.
       This can be customized via the  \l ApplicationWindow::theme group property. According
       to the Material Design guidelines, this should taken from a second color palette that
       complements the primary color palette at
       \l {http://www.google.com/design/spec/style/color.html#color-color-palette}.
    */
    property color accentColor: "#99CEEE"

    /*!
       The default background color for the application.
     */
    property color backgroundColor: Qt.rgba(0.3, 0.3, 0.3)

    /*!
       Standard colors specifically meant for light surfaces. This includes text colors along with
       a light version of the accent color.
     */
    property ThemePalette light: ThemePalette {
        light: true
    }

    /*!
       Standard colors specifically meant for dark surfaces. This includes text colors along with
       a dark version of the accent color.
    */
    property ThemePalette dark: ThemePalette {
        light: false
    }

    /*!
       A utility method for changing the alpha on colors. Returns a new object, and does not modify
       the original color at all.
     */
    function alpha(color, alpha) {
        // Make sure we have a real color object to work with (versus a string like "#ccc")
        var realColor = Qt.darker(color, 1)

        realColor.a = alpha

        return realColor
    }

    /*!
       Select a color depending on whether the background is light or dark.

       \c lightColor is the color used on a light background.

       \c darkColor is the color used on a dark background.
     */
    function lightDark(background, lightColor, darkColor) {
        var temp = Qt.darker(background, 1)

        var a = 1 - ( 0.299 * temp.r + 0.587 * temp.g + 0.114 * temp.b);

        if (temp.a === 0 || a < 0.3)
            return lightColor
        else
            return darkColor
    }

    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-Bold.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-BoldItalic.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-ExtraBold.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-ExtraBoldItalic.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-Italic.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-Light.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-LightItalic.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-Regular.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-Semibold.ttf")}
    FontLoader {source: Qt.resolvedUrl("fonts/opensans/OpenSans-SemiboldItalic.ttf")}
}