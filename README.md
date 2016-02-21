[![](https://img.shields.io/badge/goto-development%20project-yellowgreen.svg)](https://github.com/pyblish/pyblish-base) [![Gitter][gitter-image]](https://gitter.im/pyblish/pyblish)

[![title](https://cloud.githubusercontent.com/assets/2152766/12704096/b74e8778-c84a-11e5-94f6-adc0c3c50447.png)](https://www.youtube.com/watch?v=j5uUTW702-U)

Test-driven content creation for collaborative, creative projects.

This project contains a fixed set of sub-projects at a particular version, these are the currently supported combination of versions. This project is then packaged and distributed in other projects, such as [pyblish-win](https://github.com/pyblish/pyblish-win).

- [More information](../../wiki)
- [Tutorial](https://pyblish.gitbooks.io/pyblish-by-example/content/index.html)
- [Installation](../../wiki/installation)
- [Chatroom](https://gitter.im/pyblish/pyblish)

[gitter-image]: https://badges.gitter.im/Join%20Chat.svg

```bash
# Relationship graph

                                  +----------------+
                                  |                |
                                  |  pyblish-win   | inherits 1.3.1
                                  |                | from pyblish
                                  +----------------+
                                          |
                                          |
                                          |
                                          |
                                  +-------v--------+
                                  |                |
             +--------------------+     pyblish    +------------------------+
             |                 +--+                +---+                    |
             |                 |  +----------------+   |                    |
             |                 |        1.3.1          |                    |
             |                 |                       |                    |
             |                 |                       |                    |
             |                 |                       |                    |
    +--------v-------+   +-----v----------+   +--------v-------+   +--------v-------+
    |                |   |                |   |                |   |                |
    |  pyblish-base  |   |  pyblish-qml   |   |  pyblish-rpc   |   |  pyblish-maya  |
    |                |   |                |   |                |   |                |
    +----------------+   +----------------+   +----------------+   +----------------+
          1.3.0                 0.4.0                0.2.0                1.2.0

```
