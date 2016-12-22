# About
The python interpreter included with vanilla Battlefield 2142 is lacking a fairly large amount of functionality. Much of this involves restrictions on OS interaction, as well as the removal of threading support and the ability to load C extensions. Due to this, a large chunk of the standard library is broken as it depends on functionality that was removed.

This repository has two major sections.  The first is a library that can be used with vanilla 2142 and reimplements various functionality that was removed.  This is superseded by the second section, which is a library which contains advanced functionality that builds off of the ability to load an unrestricted python interpreter into the game.
