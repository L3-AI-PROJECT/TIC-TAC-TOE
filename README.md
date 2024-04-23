# Tic-Tac-Toe Game

This project is a Python implementation of the classic game Tic-Tac-Toe with a twist. It features a unique set of rules designed to add strategic depth to the game.

## Authors

-   gugeorgy (gueigeorgy2@gmail.com)
-   bliu666666 (liubowen31415926@gmail.com)

## Game Rules

The game is played on a grid where each player places their mark, an X or an O, in an empty cell. The first player to align a certain number of their marks in a row horizontally, vertically, or diagonally wins the game.

### Objectives

The aim of the game is to be the first player to align a specified number of their marks (X or O) on the grid. The default is three, but this can be changed using command line arguments.

This game variant offers a more complex and engaging experience than the traditional three-cell tic-tac-toe. It encourages players to think several moves ahead and consider the general state of the playing area, making it an excellent exercise in critical thinking and planning.

### Move Placement

Unlike the classic game, players can only place their marks next to a cell already occupied. This rule requires more foresight and strategy, offering a more complex and engaging experience than the traditional game.

## Requirements

-   Python 3.10 or later. The project relies solely on Python's standard library and has no external dependencies.
-   If you're using an older Python release, consider using [pyenv](https://github.com/pyenv/pyenv) or [Docker](https://www.docker.com/) to manage Python versions.
-   For development, pytest 6.2.5 or later is required for running tests.

## Project Structure

The project is divided into two main parts:

1. `frontend/`: This directory contains the user interfaces for the game. Currently, there's a console-based interface in the `console/` directory.
2. `lib/`: This directory contains the core game library, which includes the main logic of the game.

## Setup

To set up the project, you need to create and activate a shared virtual environment and install the library with pip. Here's how you can do it:

```sh
python -m venv venv
source venv/bin/activate
python -m pip install --editable lib/
```

## How to Run

To run the console-based game, navigate to the `root/` directory and use the following command:

```sh
python -m frontend.console
```

### Command Line Arguments

Customize the game settings using the following command line arguments:

-   `-X`: Type of player X. Choices are "human" and "random". Default is "human".
-   `-O`: Type of player O. Choices are "human" and "random". Default is "random".
-   `--starting`: The mark of the starting player. Default is "X".
-   `--required`: The number of marks in a row required to win. Default is 3.
-   `--dimension`: The dimension of the game grid. Default is 3.

For example, to run the game with a human player X, a random player O, starting mark "O", 4 marks required for a win, and a 4x4 grid, use:

```sh
python -m frontend.console -X human -O random --starting O --required 4 --dimension 4
```
