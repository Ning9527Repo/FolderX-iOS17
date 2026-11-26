# FolderX 1.5.22

Fixes the regression introduced in 1.5.21: FXMiniGrid cached only bounds and columns, so rebuilding cells with unchanged geometry could skip assigning frames. Remove that cache entirely; retain the recursive layout guard. Each valid pass lays out the current cells, including after app reorder, replacement, empty-to-populated update and column changes. Cell coordinates include bounds.origin, matching UIKit local coordinates.

The 6x2 wide-folder model and transition-clone protections predate this change. They are not newly implemented here. This release does not establish a fix for the reported native container transition drift; device runtime evidence is still needed for that issue.

CI is manual-only to prevent the duplicate push + dispatch builds that occurred for 1.5.21. Build both real arm64/rootless and arm64e/RootHide packages. No automatic device installation or SpringBoard restart.
