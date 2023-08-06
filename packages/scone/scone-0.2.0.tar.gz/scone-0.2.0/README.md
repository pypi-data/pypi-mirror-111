# scone: Server CONfiguration Engine

Scone is a tool for configuring servers (or even other computers).

The idea is that you write a declarative configuration using Scone Menu Language (.scoml) files and run `scone` on it.

Scone will, ideally speaking, do whatever is necessary to bring your declarative configuration into reality.

You can track your configuration in `git`, for example, and should be able to re-apply this to your server whenever you need to recreate it (or update it!).


Scone tries to be quick, owing to the fact that iterative development is more engaging and productive.
To do this, Scone runs multiple recipes (jobs) in parallel (Scone has a fairly rich dependency tracking system to allow ordering recipes fairly intuitively to allow this). Scone also caches outcomes of recipes, so a small change to the configuration does NOT need to re-execute all recipes afterwards.


Scone is currently alpha-grade software; the author uses it to configure their servers (fully), mobile phone (mostly fully) and laptop/desktop computers (partially).

