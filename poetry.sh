#!/usr/bin/env bash

curl -sSL https://install.python-poetry.org | python3 -

{
  echo "PATH=$HOME/.local/bin:$PATH"
  echo "export PATH"
} >> ~/.bashrc

echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."