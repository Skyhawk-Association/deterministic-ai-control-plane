# Device Independence

## Principle

The project must not depend on a particular Mac, Windows machine, Pixel, terminal emulator, SSH client, or local directory for its authoritative state.

## Operating model

- GitHub holds public durable DACP state.
- ChatGPT/DACP performs reasoning, orchestration, and authorized remote actions.
- Terminal/SSH/local tools are selected only when a task requires that execution surface.
- A local Git clone is a working copy, not authority merely because it exists.
- Local work becomes authoritative only through the governed Git commit/persistence/read-back path.

## Human/AI role allocation

Changing platform changes the execution adapter, not the role allocation. Gene supplies the objective and genuinely human decisions. The AI owns authorized mechanical execution, translation, recursive testing, and verification to the maximum competent extent.
