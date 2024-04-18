# Tic-Tac-Toe Game

This is a Python implementation of the classic game Tic-Tac-Toe.

## Game Rules

The classic tic-tac-toe is played on a grid of cells where each player places their mark, an X or an O, in an empty cell. The first player to place three of their marks in a row horizontally, vertically, or diagonally wins the game.

The tic-tac-toe variant pictured here features a unique set of rules designed to add strategic depth to this classic game.

Objectives: The aim of the game is to be the first player to align five of their marks (X or O) on the grid.

Move placement: A peculiarity of the classic game is that players can only place their marks next to a cell already occupied. This means that each move must be made next to another mark, which requires more foresight and strategy.

The aim of this game variant is to offer a more complex and engaging experience than the traditional three-cell tic-tac-toe. It encourages players to think several moves ahead and consider the general state of the playing area, making it an excellent exercise in critical thinking and planning.

## Requirements

This project requires Python 3.10 or later. It relies solely on Python's standard library and has no external dependencies.

If you're using an older Python release, you can install and manage multiple Python versions with [pyenv](https://github.com/pyenv/pyenv) or try the latest Python release in [Docker](https://www.docker.com/).

## Project Structure

The project is divided into two main parts:

1. `frontend/`: This directory contains the user interfaces for the game. Currently, there's a console-based interface in the `console/` directory.

2. `lib/`: This directory contains the core game library, which includes the main logic of the game.

### Frontend

The `console/` directory in `frontend/` is a runnable Python package. You can run the console-based game from the command line using Python's `-m` option.

### Library

The `lib/` directory contains the core game library. The `src/tic_tac_toe/` directory contains two subdirectories: `game/` and `logic/`, which contain the game state and game logic respectively.

## Setup

To set up the project, you need to create and activate a shared virtual environment and install the library with pip. Here's how you can do it:

```sh
python -m venv venv
source venv/bin/activate
python -m pip install --editable lib/
```

## How to Run

To run the console-based game, navigate to the `console/` directory in `frontend/` and use the following command:

```sh
python -m console
```
