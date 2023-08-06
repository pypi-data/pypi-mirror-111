Chain Reaction
==============

.. image:: https://img.shields.io/pypi/v/simplebot_chain_reaction.svg
   :target: https://pypi.org/project/simplebot_chain_reaction

.. image:: https://img.shields.io/pypi/pyversions/simplebot_chain_reaction.svg
   :target: https://pypi.org/project/simplebot_chain_reaction

.. image:: https://pepy.tech/badge/simplebot_chain_reaction
   :target: https://pepy.tech/project/simplebot_chain_reaction

.. image:: https://img.shields.io/pypi/l/simplebot_chain_reaction.svg
   :target: https://pypi.org/project/simplebot_chain_reaction

.. image:: https://github.com/simplebot-org/simplebot_chain_reaction/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/simplebot-org/simplebot_chain_reaction/actions/workflows/python-ci.yml

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

A Chain Reaction game plugin for `SimpleBot`_.
To move send messages with coordinates: **a1**, **b3**, etc. to place orbs in the corresponding cell.

The objetive of Chain Reaction is to take control of the board by eliminating your oponents orbs.

Players take it turns to place their orbs in a cell. Once a cell has reached critical mass the orbs explode into the surrounding cells adding an extra orb and claiming the cell for the player. A player may only place their orbs in a blank cell or a cell that contains orbs of their own colour. As soon as player looses all their orbs they are out of the game.

To learn about Chain Reaction and the game rules read: https://brilliant.org/wiki/chain-reaction-game/

Install
-------

To install run::

  pip install simplebot-chain-reaction


.. _SimpleBot: https://github.com/simplebot-org/simplebot
