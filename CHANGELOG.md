# Changelog

This document records all notable changes to this project. The project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and the format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Table of Contents

-   [Unreleased](#unreleased)
-   [v1.0.1 - 2024-05-27](#v101---2024-05-27)
-   [v1.0.0 - 2024-04-23](#v100---2024-04-23)
-   [v0.1.0 - 2024-03-24](#v010---2024-03-24)

## Unreleased

### Added

-   N/A

### Changed

-   Improved the efficiency of the Minimax algorithm by implementing a more effective heuristic.
-   Updated the Command-Line Interface (CLI) to provide more detailed feedback to the user.

### Deprecated

-   The "random" player type will be deprecated in the next major version due to its unpredictable behavior.

### Removed

-   Removed redundant code in the game logic that was causing unnecessary computational overhead.

### Fixed

-   Fixed an issue where the "alpha_beta" player type was not making optimal moves in certain scenarios.

### Security

-   Patched a potential security vulnerability related to input validation in the Command-Line Interface (CLI).

## v1.0.1 - 2024-05-27

### Added

-   Minimax and Alpha-Beta algorithms for computer players.
-   Final mix of algorithms for optimal game performance.
-   Support for different player types: "human", "random", "minimax", and "alpha_beta".

### Changed

-   Improved the user interface to provide a more intuitive and user-friendly experience.
-   Updated the game logic to enhance the performance of the Minimax and Alpha-Beta algorithms.

### Fixed

-   Fixed a bug where the game would occasionally freeze when a player attempted to make a move in a full grid.
-   Resolved an issue where the "alpha_beta" player type would sometimes make non-optimal moves.

## v1.0.0 - 2024-04-23

### Added

-   Complete model implementation for Tic-Tac-Toe game domain.
-   Command-Line Interface (CLI) for interacting with the game.
-   Customizable game settings via command line arguments.
-   Support for different player types: "human", "random".
-   Option to specify the starting player, the number of marks required to win, and the dimension of the game grid.

## v0.1.0 - 2024-03-24

### Added

-   Initial project setup.
-   Basic game rules and logic.
